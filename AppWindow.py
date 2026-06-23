import tkinter as tk
from tkinter import ttk, BooleanVar, Text, messagebox
from data import (
    main_depts,
    vendor_list,
    web_behavior,
    color_filter,
    brand_filter,
    gift_depts,
    gm_depts,
    clothing_depts,
    dept_cat_map,
    color_options,
    size_options,
    logo_options,
    namedrop_options,
)
from functions import (
    web_submit_click,
    create_df,
    create_standalone,
    create_parent,
    create_children,
    next_child,
    create_matrix_df,
    go_back,
)
from CustomWidgets import TwoDecimalEntry


class LoneItemWindow(tk.Toplevel):
    def __init__(self, parent, offset=30, items_df=None):
        super(LoneItemWindow, self).__init__(parent)
        self.lift()
        self.focus_force()

        self.parent = parent
        self.items_df = items_df

        self.resizable(False, False)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, weight=1)

        self.selected_shop_id = None
        self.selected_dept_id = None
        self.selected_prod_cat_id = None
        self.selected_dept = None
        self.selected_prod_cat = None

        self.dept_list = list(main_depts.keys())
        self.vendor_list = list(vendor_list.keys())

        ttk.Label(self, text="Item Name").grid(
            column=0, row=1, columnspan=2, padx=10, pady=10
        )

        self.item_name_entry = tk.Entry(self)
        self.item_name_entry.grid(column=3, row=1, columnspan=3, padx=10, pady=10)

        ttk.Label(self, text="UPC").grid(
            column=0, row=2, columnspan=2, padx=10, pady=10
        )
        self.item_upc_entry = tk.Entry(self)
        self.item_upc_entry.grid(column=3, row=2, columnspan=3, padx=10, pady=10)

        self.shop = tk.StringVar(self)
        ttk.Label(self, text="Department").grid(
            column=0, row=3, columnspan=2, padx=10, pady=10
        )
        self.item_shop_dropdown = ttk.Combobox(
            self,
            values=self.dept_list,
            textvariable=self.shop,
            state="readonly",
            width=30,
            justify="center",
        )
        self.item_shop_dropdown.grid(column=3, row=3, columnspan=3, padx=10, pady=10)

        self.item_shop_dropdown.bind("<<ComboboxSelected>>", self.on_shop_selected)

        ttk.Label(self, text="Category").grid(
            column=0, row=4, columnspan=2, padx=10, pady=10
        )
        self.cat_label = ttk.Label(
            self, borderwidth=1, relief="sunken", width=30, justify="center"
        )
        self.cat_label.grid(column=3, row=4, columnspan=3, padx=10, pady=10)

        ttk.Label(self, text="Purchase Price").grid(
            column=0, row=5, columnspan=2, padx=10, pady=10
        )
        self.item_cost_entry = TwoDecimalEntry(self)

        self.vendor = tk.StringVar(self)
        ttk.Label(self, text="Vendor").grid(
            column=0, row=6, columnspan=2, padx=10, pady=10
        )
        self.vendor_dropdown = ttk.Combobox(
            self,
            values=self.vendor_list,
            textvariable=self.vendor,
            state="readonly",
            width=30,
            justify="center",
        )

        ttk.Label(self, text="Vendor Code").grid(
            column=0, row=7, columnspan=2, padx=10, pady=10
        )
        self.vendor_code_entry = tk.Entry(self)

        self.pref_vendor_check = BooleanVar(self)
        self.vendor_check = ttk.Checkbutton(
            self,
            text="Preferred Vendor?",
            variable=self.pref_vendor_check,
            onvalue="True",
            offvalue="False",
        )

        self.base_price = tk.StringVar(self)
        ttk.Label(self, text="Base Price").grid(
            column=0, row=9, columnspan=2, padx=10, pady=10
        )
        self.base_price_entry = TwoDecimalEntry(self, textvariable=self.base_price)
        self.dept_price = tk.StringVar(self)
        ttk.Label(self, text="Department Price (-20%)").grid(
            column=0, row=10, columnspan=2, padx=10, pady=10
        )
        self.dept_price_entry = TwoDecimalEntry(self, textvariable=self.dept_price)
        self.base_price.trace_add("write", self.dept_price_calc)

        self.oos_message = tk.StringVar(self)
        ttk.Label(self, text="Web Out of Stock Behavior").grid(
            column=0, row=12, columnspan=5, padx=10, pady=10
        )
        self.oos_message_dropdown = ttk.Combobox(
            self,
            values=list(web_behavior.keys()),
            textvariable=self.oos_message,
            state="readonly",
            width=40,
        )

        self.item_cost_entry.grid(column=3, row=5, columnspan=3, padx=10, pady=10)
        self.vendor_dropdown.grid(column=3, row=6, columnspan=3, padx=10, pady=10)
        self.vendor_code_entry.grid(column=3, row=7, columnspan=3, padx=10, pady=10)
        self.vendor_check.grid(column=0, row=8, columnspan=5, padx=10, pady=10)
        self.base_price_entry.grid(column=3, row=9, columnspan=3, padx=10, pady=10)
        self.dept_price_entry.grid(column=3, row=10, columnspan=3, padx=10, pady=10)
        self.oos_message_dropdown.grid(column=0, row=13, columnspan=5, padx=10, pady=10)

        back_btn = ttk.Button(self, text="Back", command=lambda: go_back(self))
        back_btn.grid(column=0, row=50, columnspan=2, padx=10, pady=10)

        next_step_btn = ttk.Button(
            self, text="Next", command=lambda: self.submit_item()
        )
        next_step_btn.grid(column=3, row=50, columnspan=3, padx=10, pady=10)

        self.update_idletasks()

        width = self.winfo_width()
        height = self.winfo_height()

        if parent and isinstance(parent, tk.Toplevel) or isinstance(parent, tk.Tk):
            x = parent.winfo_x() + offset
            y = parent.winfo_y() + offset
        else:
            x, y = 100, 100

        self.geometry(f"{width}x{height}+{x}+{y}")

    def submit_item(self):
        item = create_standalone(
            self,  # lambda ensures context is captured at load and executes when clicked
            self.item_name_entry.get(),
            self.item_upc_entry.get(),
            self.selected_shop_id,
            self.selected_dept,
            self.selected_prod_cat,
            self.selected_dept_id,
            self.selected_prod_cat_id,
            self.item_cost_entry.get(),
            self.vendor.get(),
            self.vendor_code_entry.get(),
            self.pref_vendor_check.get(),
            self.base_price_entry.get(),
            self.dept_price_entry.get(),
            self.oos_message.get(),
        )
        if not item:
            return
        elif not item.check_upc():
            return
        else:
            add_web = messagebox.askyesno(message="Enter Web Fields?", icon="question")
            if add_web is True:
                WebFieldWindow(self, item, offset=40, item_type="standalone")
            else:
                create_df(item, self)

    def dept_price_calc(self, event, *args):
        self.dept_price_entry.delete(0, "end")
        base_price = self.base_price.get()
        if base_price != "":
            base_price = float(base_price)
            disc_price = float(base_price * 0.8)
            rounded_disc_price = round(disc_price, 2)
            print(rounded_disc_price)
            self.dept_price_entry.insert(0, rounded_disc_price)

    def on_shop_selected(self, event):
        selected_shop = self.shop.get()
        shop_id = main_depts.get(selected_shop)
        print(selected_shop, shop_id)
        DeptCatWindow(self, selected_shop, shop_id)


class MatrixParentWindow(tk.Toplevel):
    def __init__(self, parent, offset=30, items_df=None):
        super(MatrixParentWindow, self).__init__(parent)
        self.lift()
        self.focus_force()

        self.parent = parent
        self.items_df = items_df

        self.resizable(False, False)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, weight=1)

        self.selected_shop_id = None
        self.selected_dept_id = None
        self.selected_prod_cat_id = None
        self.selected_dept = None
        self.selected_prod_cat = None

        self.dept_list = list(main_depts.keys())
        self.vendor_list = list(vendor_list.keys())

        ttk.Label(self, text="Item Name").grid(
            column=0, row=1, columnspan=2, padx=10, pady=10
        )

        self.item_name_entry = tk.Entry(self)
        self.item_name_entry.grid(column=3, row=1, columnspan=3, padx=10, pady=10)

        self.shop = tk.StringVar(self)
        ttk.Label(self, text="Department").grid(
            column=0, row=3, columnspan=2, padx=10, pady=10
        )
        self.item_shop_dropdown = ttk.Combobox(
            self,
            values=self.dept_list,
            textvariable=self.shop,
            state="readonly",
            width=30,
            justify="center",
        )
        self.item_shop_dropdown.grid(column=3, row=3, columnspan=3, padx=10, pady=10)

        self.item_shop_dropdown.bind("<<ComboboxSelected>>", self.on_shop_selected)

        ttk.Label(self, text="Category").grid(
            column=0, row=4, columnspan=2, padx=10, pady=10
        )
        self.cat_label = ttk.Label(
            self, borderwidth=1, relief="sunken", width=30, justify="center"
        )
        self.cat_label.grid(column=3, row=4, columnspan=3, padx=10, pady=10)

        self.vendor = tk.StringVar(self)
        ttk.Label(self, text="Vendor").grid(
            column=0, row=6, columnspan=2, padx=10, pady=10
        )
        self.vendor_dropdown = ttk.Combobox(
            self,
            values=self.vendor_list,
            textvariable=self.vendor,
            state="readonly",
            width=30,
            justify="center",
        )
        self.vendor_dropdown.grid(column=3, row=6, columnspan=3, padx=10, pady=10)

        self.pref_vendor_check = BooleanVar(self)
        self.vendor_check = ttk.Checkbutton(
            self,
            text="Preferred Vendor?",
            variable=self.pref_vendor_check,
            onvalue="True",
            offvalue="False",
        )
        self.vendor_check.grid(column=0, row=8, columnspan=5, padx=10, pady=10)

        back_btn = ttk.Button(self, text="Back", command=lambda: go_back(self))
        back_btn.grid(column=0, row=50, columnspan=2, padx=10, pady=10)

        option_select_btn = ttk.Button(
            self, text="Select Options", command=lambda: self.option_select()
        )
        option_select_btn.grid(column=3, row=50, columnspan=3, padx=10, pady=10)

        self.update_idletasks()

        width = self.winfo_width()
        height = self.winfo_height()

        if parent and isinstance(parent, tk.Toplevel) or isinstance(parent, tk.Tk):
            x = parent.winfo_x() + offset
            y = parent.winfo_y() + offset
        else:
            x, y = 100, 100

        self.geometry(f"{width}x{height}+{x}+{y}")

    def option_select(self):
        item_vendor = self.vendor.get()
        if not item_vendor:
            messagebox.showerror("Error", "Vendor cannot be empty")
            return
        else:
            parent_item = create_parent(
                self,
                self.item_name_entry.get(),
                self.selected_shop_id,
                self.selected_dept,
                self.selected_prod_cat,
                self.selected_dept_id,
                self.selected_prod_cat_id,
                self.vendor.get(),
                self.pref_vendor_check.get(),
            )
            ItemOptionsWindow(self, parent_item, offset=40)

    def on_shop_selected(self, event):
        selected_shop = self.shop.get()
        shop_id = main_depts.get(selected_shop)
        print(selected_shop, shop_id)
        DeptCatWindow(self, selected_shop, shop_id)


class ItemOptionsWindow(tk.Toplevel):
    def __init__(self, parent, item, offset=30):
        super(ItemOptionsWindow, self).__init__(parent)

        self.parent = parent
        self.item = item

        self.columnconfigure(0, weight=1)

        # color options
        self.use_color = BooleanVar(value=False)
        self.color_check = ttk.Checkbutton(
            self,
            text="Color",
            variable=self.use_color,
            command=lambda: self._toggle_widget(
                self.color_listbox, self.use_color, "normal"
            ),
        )
        self.color_check.grid(column=0, row=1, columnspan=2, padx=10, pady=10)
        self.color_list = tk.StringVar(value=list(color_options.keys()))
        self.color_listbox = tk.Listbox(
            self, listvariable=self.color_list, state="disabled", selectmode="extended"
        )
        self.color_listbox.grid(column=0, row=2, columnspan=1, padx=10, pady=10)

        # size options
        self.use_size = BooleanVar(value=False)
        self.size_check = ttk.Checkbutton(
            self,
            text="Size",
            variable=self.use_size,
            command=lambda: self._toggle_widget(
                self.size_listbox, self.use_size, "normal"
            ),
        )
        self.size_check.grid(column=0, row=3, columnspan=2, padx=10, pady=10)
        self.size_list = tk.StringVar(value=list(size_options.keys()))
        self.size_listbox = tk.Listbox(
            self,
            listvariable=self.size_list,
            exportselection=False,
            state="disabled",
            selectmode="extended",
        )
        self.size_listbox.grid(column=0, row=4, columnspan=1, padx=10, pady=10)

        # logo options
        self.use_logo = BooleanVar(value=False)
        self.logo_check = ttk.Checkbutton(
            self,
            text="Logo",
            variable=self.use_logo,
            command=lambda: self._toggle_widget(
                self.logo_listbox, self.use_logo, "normal"
            ),
        )
        self.logo_check.grid(column=6, row=1, columnspan=2, padx=10, pady=10)
        self.logo_list = tk.StringVar(value=list(logo_options.keys()))
        self.logo_listbox = tk.Listbox(
            self,
            listvariable=self.logo_list,
            exportselection=False,
            state="disabled",
            selectmode="extended",
        )
        self.logo_listbox.grid(column=6, row=2, columnspan=1, padx=10, pady=10)

        # namedrop options
        self.use_namedrop = BooleanVar(value=False)
        self.namedrop_check = ttk.Checkbutton(
            self,
            text="Namedrop",
            variable=self.use_namedrop,
            command=lambda: self._toggle_widget(
                self.namedrop_listbox, self.use_namedrop, "normal"
            ),
        )
        self.namedrop_check.grid(column=6, row=3, columnspan=2, padx=10, pady=10)
        self.namedrop_list = tk.StringVar(value=list(namedrop_options.keys()))
        self.namedrop_listbox = tk.Listbox(
            self,
            listvariable=self.namedrop_list,
            exportselection=False,
            state="disabled",
            selectmode="extended",
        )
        self.namedrop_listbox.grid(column=6, row=4, columnspan=1, padx=10, pady=10)

        next_btn = ttk.Button(
            self, text="Next", command=lambda: self.validate_children()
        )
        next_btn.grid(column=3, row=50, padx=10, pady=10)

        self.update_idletasks()

        width = self.winfo_width()
        height = self.winfo_height()

        if parent and isinstance(parent, tk.Toplevel) or isinstance(parent, tk.Tk):
            x = parent.winfo_x() + offset
            y = parent.winfo_y() + offset
        else:
            x, y = 100, 100

        self.geometry(f"{width}x{height}+{x}+{y}")

    def validate_children(self):
        matrix_item = create_children(
            self,
            self.item,
            self.color_listbox,
            self.size_listbox,
            self.logo_listbox,
            self.namedrop_listbox,
        )
        for i in range(len(matrix_item.values())):
            for parent, children in matrix_item.items():
                for child in children:
                    single_child = ChildItemWindow(
                        self, item=child, children=children, offset=40
                    )
                    self.wait_window(single_child)
                    i + 1
        add_web = messagebox.askyesno(message="Enter Web Fields?", icon="question")
        if add_web is True:
            WebFieldWindow(self, matrix_item, offset=40, item_type="matrix")
        else:
            create_matrix_df(self, matrix_item)

    def _toggle_widget(self, widget, var, active_state):
        state = active_state if var.get() else "disabled"
        widget.config(state=state)


class ChildItemWindow(tk.Toplevel):
    def __init__(self, parent, item, children, offset=30):
        super(ChildItemWindow, self).__init__(parent)
        self.parent = parent
        self.item = item
        self.window = self

        self.window.resizable(False, False)
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(3, weight=1)

        ttk.Label(self.window, text="Item").grid(
            column=0, row=2, columnspan=2, padx=10, pady=10
        )
        self.item_name = ttk.Label(
            self,
            borderwidth=1,
            text=f"{item.name}",
            relief="sunken",
            width=30,
            justify="center",
        )
        self.item_name.grid(column=3, row=2, columnspan=3, padx=10, pady=10)

        ttk.Label(self, text="UPC").grid(
            column=0, row=4, columnspan=2, padx=10, pady=10
        )
        self.item_upc_entry = tk.Entry(self)
        self.item_upc_entry.grid(column=3, row=4, columnspan=3, padx=10, pady=10)

        ttk.Label(self, text="Purchase Price").grid(
            column=0, row=6, columnspan=2, padx=10, pady=10
        )
        self.item_cost_entry = TwoDecimalEntry(self)
        self.item_cost_entry.grid(column=3, row=6, columnspan=3, padx=10, pady=10)

        ttk.Label(self, text="Vendor Code").grid(
            column=0, row=8, columnspan=2, padx=10, pady=10
        )
        self.vendor_code_entry = tk.Entry(self)
        self.vendor_code_entry.grid(column=3, row=8, columnspan=3, padx=10, pady=10)

        self.base_price = tk.StringVar(self)
        ttk.Label(self, text="Base Price").grid(
            column=0, row=10, columnspan=2, padx=10, pady=10
        )
        self.base_price_entry = TwoDecimalEntry(self, textvariable=self.base_price)
        self.base_price_entry.grid(column=3, row=10, columnspan=3, padx=10, pady=10)

        self.dept_price = tk.StringVar(self)
        ttk.Label(self, text="Department Price (-20%)").grid(
            column=0, row=12, columnspan=2, padx=10, pady=10
        )
        self.dept_price_entry = TwoDecimalEntry(self, textvariable=self.dept_price)
        self.base_price.trace_add("write", self.dept_price_calc)
        self.dept_price_entry.grid(column=3, row=12, columnspan=3, padx=10, pady=10)

        self.oos_message = tk.StringVar(self.window)
        ttk.Label(self.window, text="Web Out of Stock Behavior").grid(
            column=0, row=14, columnspan=5, padx=10, pady=10
        )
        self.oos_message_dropdown = ttk.Combobox(
            self.window,
            values=list(web_behavior.keys()),
            textvariable=self.oos_message,
            state="readonly",
            width=40,
        )
        self.oos_message_dropdown.grid(column=0, row=15, columnspan=5, padx=10, pady=10)

        self.filtered_color = tk.StringVar(self.window)
        ttk.Label(self.window, text="Filter Color").grid(
            column=0, row=17, columnspan=2, padx=10, pady=10
        )
        self.color_filter_dropdown = ttk.Combobox(
            self.window,
            values=list(color_filter.keys()),
            textvariable=self.filtered_color,
            width=30,
            state="readonly",
        )
        self.color_filter_dropdown.grid(
            column=3, row=17, columnspan=3, padx=10, pady=10
        )

        delete_itm_btn = ttk.Button(
            self, text="Delete Item", command=lambda: self.delete_child(item, children)
        )
        delete_itm_btn.grid(column=0, row=50, columnspan=2, padx=10, pady=10)

        next_itm_btn = ttk.Button(
            self,
            text="Next Child",
            command=lambda: next_child(
                self,
                children,
                item,
                self.item_upc_entry.get(),
                self.item_cost_entry.get(),
                self.vendor_code_entry.get(),
                self.base_price_entry.get(),
                self.dept_price_entry.get(),
                self.filtered_color.get(),
                self.oos_message.get(),
            ),
        )
        next_itm_btn.grid(column=2, row=50, columnspan=2, padx=10, pady=10)

        self.update_idletasks()

        width = self.winfo_width()
        height = self.winfo_height()

        if parent and isinstance(parent, tk.Toplevel) or isinstance(parent, tk.Tk):
            x = parent.winfo_x() + offset
            y = parent.winfo_y() + offset
        else:
            x, y = 100, 100

        self.geometry(f"{width}x{height}+{x}+{y}")

    def delete_child(self, item, children):
        # delete child item, destroy window, launch next window
        delete_ques = messagebox.askyesno(
            "Delete?", "Do you want to delete this child item?"
        )
        if delete_ques:
            children.remove(item)
            return children, next_child(self, children)
        else:
            return

    def dept_price_calc(self, event, *args):
        self.dept_price_entry.delete(0, "end")
        base_price = self.base_price.get()
        if base_price != "":
            base_price = float(base_price)
            disc_price = float(base_price * 0.8)
            rounded_disc_price = round(disc_price, 2)
            print(rounded_disc_price)
            self.dept_price_entry.insert(0, rounded_disc_price)


class WebFieldWindow(tk.Toplevel):
    def __init__(self, parent, item, item_type, offset=30):
        super(WebFieldWindow, self).__init__(parent)
        self.atp_qty = None
        self.chosen_color = None
        self.chosen_filter = None

        self.parent = parent
        self.item = item
        self.window = self

        self.window.resizable(False, False)
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(3, weight=1)

        ttk.Label(self.window, text="Web Display Name").grid(
            column=0, row=11, columnspan=2, padx=10, pady=10
        )
        self.web_name_entry = tk.Entry(self.window)
        ttk.Label(self.window, text="Web Description").grid(
            column=0, row=12, columnspan=5, padx=10, pady=10
        )
        self.web_desc_box = Text(
            self.window,
            width=60,
            height=10,
            wrap="word",
            relief="sunken",
            borderwidth=2,
        )

        ttk.Separator(self.window, orient="horizontal").grid(
            row=16, columnspan=5, padx=10, pady=10, sticky="ew"
        )

        self.add_atp = BooleanVar(value=False)
        self.atp_check = ttk.Checkbutton(
            self.window,
            text="Set ATP Reserve?",
            variable=self.add_atp,
            command=lambda: self._toggle_widget(
                self.atp_qty_entry, self.add_atp, "normal"
            ),
        )
        self.atp_check.grid(column=0, row=16, columnspan=5, padx=10, pady=10)
        ttk.Label(self.window, text="ATP Reserve Quantity").grid(
            column=0, row=17, columnspan=2, padx=10, pady=10
        )
        self.atp_qty_entry = tk.Entry(self.window, state="disabled")

        ttk.Separator(self.window, orient="horizontal").grid(
            row=18, columnspan=5, padx=10, pady=10, sticky="ew"
        )

        self.filter_color = BooleanVar(value=False)
        self.color_check = ttk.Checkbutton(
            self.window,
            text="Add Color Filter?",
            variable=self.filter_color,
            command=lambda: self._toggle_widget(
                self.color_filter_dropdown, self.filter_color, "readonly"
            ),
        )
        self.filtered_color = tk.StringVar(self.window)
        self.filter_color_lbl = ttk.Label(self.window, text="Filter Color")
        self.color_filter_dropdown = ttk.Combobox(
            self.window,
            values=list(color_filter.keys()),
            textvariable=self.filtered_color,
            width=30,
            state="disabled",
        )

        if item_type == "matrix":
            self.color_check.grid_remove()
            self.color_filter_dropdown.grid_remove()
            self.filter_color_lbl.grid_remove()
        else:
            self.color_check.grid(column=0, row=18, columnspan=5, padx=10, pady=10)
            self.filter_color_lbl.grid(column=0, row=19, columnspan=2, padx=10, pady=10)
            self.color_filter_dropdown.grid(
                column=3, row=19, columnspan=3, padx=10, pady=10
            )

            ttk.Separator(self.window, orient="horizontal").grid(
                row=20, columnspan=5, padx=10, pady=10, sticky="ew"
            )

        self.filter_brand = BooleanVar(value=False)
        self.brand_check = ttk.Checkbutton(
            self.window,
            text="Add Brand Filter?",
            variable=self.filter_brand,
            command=lambda: self._toggle_widget(
                self.brand_filter_dropdown, self.filter_brand, "readonly"
            ),
        )
        self.filtered_brand = tk.StringVar(self.window)
        self.brand_check.grid(column=0, row=20, columnspan=5, padx=10, pady=10)
        ttk.Label(self.window, text="Brand Filter").grid(
            column=0, row=21, columnspan=2, padx=10, pady=10
        )
        self.brand_filter_dropdown = ttk.Combobox(
            self.window,
            values=list(brand_filter.keys()),
            textvariable=self.filtered_brand,
            width=30,
            state="disabled",
        )

        self.web_name_entry.grid(column=3, row=11, columnspan=3, padx=10, pady=10)
        self.web_desc_box.grid(column=0, row=13, columnspan=5, padx=10, pady=10)
        self.atp_qty_entry.grid(column=3, row=17, columnspan=3, padx=10, pady=10)

        self.brand_filter_dropdown.grid(
            column=3, row=21, columnspan=3, padx=10, pady=10
        )

        submit_btn = ttk.Button(
            self.window, text="Submit", command=lambda: web_submit_click(self, item)
        )
        submit_btn.grid(column=0, row=50, columnspan=5, padx=10, pady=10)

        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()

        if parent and isinstance(parent, tk.Toplevel) or isinstance(parent, tk.Tk):
            x = parent.winfo_x() + offset
            y = parent.winfo_y() + offset
        else:
            x, y = 100, 100

        self.geometry(f"{width}x{height}+{x}+{y}")

    def _toggle_widget(self, widget, var, active_state):
        state = active_state if var.get() else "disabled"
        widget.config(state=state)


class DeptCatWindow(ttk.Frame):
    def __init__(self, parent, shop, shop_id):
        super(DeptCatWindow, self).__init__()

        self.parent = parent
        self.selected_shop = shop
        self.shop_id = shop_id

        self.dept_map = {"239": clothing_depts, "245": gift_depts, "250": gm_depts}
        self.active_dept_dict = self.dept_map.get(shop_id, dept_cat_map)

        category_win = tk.Toplevel(self)
        category_win.title("Select Product Category")
        category_win.geometry("600x600+500+300")
        category_win.resizable(False, False)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

        category_win.grid_columnconfigure(0, weight=1)
        category_win.grid_columnconfigure(4, weight=1)

        ttk.Label(
            category_win,
            text="Select and verify item department and product category.",
            justify="center",
            width=40,
            wraplength=380,
        ).grid(column=0, row=1, columnspan=5, padx=10, pady=10)

        self.dept_filter = tk.StringVar(self)

        self.cloth_fit_list = list(clothing_depts.keys())
        self.gift_dept_list = list(gift_depts.keys())
        self.gm_dept_list = list(gm_depts.keys())

        ########################### department dropdown
        ttk.Label(
            category_win,
            text="Select Department",
            justify="center",
            width=40,
            wraplength=380,
        ).grid(column=0, row=7, columnspan=1, padx=10, pady=10)
        self.dept_dropdown = ttk.Combobox(
            category_win, textvariable=self.dept_filter, state="readonly", width=40
        )
        self.dept_dropdown.grid(column=2, row=7, columnspan=4, padx=10, pady=10)

        ########################### if-else branch: clothing vs non-clothing
        if shop_id == "239":
            self.cloth_fit = tk.StringVar(self)

            # select mens, womens, youth
            ttk.Label(
                category_win,
                text="Select Mens/Unisex, Womens, or Youth",
                justify="center",
                width=40,
                wraplength=380,
            ).grid(column=0, row=6, columnspan=1, padx=10, pady=10)
            self.cloth_fit_dropdown = ttk.Combobox(
                category_win,
                values=self.cloth_fit_list,
                textvariable=self.cloth_fit,
                state="readonly",
                width=40,
            )
            self.cloth_fit_dropdown.grid(
                column=2, row=6, columnspan=4, padx=10, pady=10
            )

            self.selected_fit = self.cloth_fit.get()

            self.cloth_fit_dropdown.bind(
                "<<ComboboxSelected>>", self.on_combobox_change
            )
        elif shop_id == "245":
            self.dept_dropdown["values"] = self.gift_dept_list
        elif shop_id == "250":
            self.dept_dropdown["values"] = self.gm_dept_list

        self.selected_dept = self.dept_filter.get()
        print(self.selected_dept)

        self.dept_dropdown.bind("<<ComboboxSelected>>", self.on_combobox_change)

        ########################### category dropdown
        self.cat_filter = tk.StringVar(self)

        ttk.Label(
            category_win,
            text="Select Parent Category",
            justify="center",
            width=40,
            wraplength=380,
        ).grid(column=0, row=8, columnspan=1, padx=10, pady=10)
        self.cat_dropdown = ttk.Combobox(
            category_win, textvariable=self.cat_filter, state="readonly", width=40
        )
        self.cat_dropdown.grid(column=2, row=8, columnspan=4, padx=10, pady=10)

        self.cat_dropdown.bind("<<ComboboxSelected>>", self.on_combobox_change)

        ########################### product category dropdown
        self.prod_cat = tk.StringVar(self)

        ttk.Label(
            category_win,
            text="Select Product Category",
            justify="center",
            width=40,
            wraplength=380,
        ).grid(column=0, row=9, columnspan=1, padx=10, pady=10)
        self.prod_cat_dropdown = ttk.Combobox(
            category_win, textvariable=self.prod_cat, state="readonly", width=40
        )
        self.prod_cat_dropdown.grid(column=2, row=9, columnspan=4, padx=10, pady=10)

        self.submit_selections = ttk.Button(
            category_win, text="Submit", command=self.validate_and_submit
        )
        self.submit_selections.grid(column=0, row=10, columnspan=5, padx=10, pady=10)

    def on_combobox_change(self, event):
        triggered_widget = event.widget
        selected_value = triggered_widget.get()

        if (
            hasattr(self, "cloth_fit_dropdown")
            and triggered_widget == self.cloth_fit_dropdown
        ):
            print(selected_value)
            self.active_nested_dict = clothing_depts[selected_value]
            print(self.active_nested_dict)
            self.dept_dropdown["values"] = list(self.active_nested_dict.keys())
            self.cat_dropdown["values"] = []
            self.prod_cat_dropdown["values"] = []
            self.cat_dropdown.set("")
            self.prod_cat_dropdown.set("")
        elif triggered_widget == self.dept_dropdown:
            if self.shop_id == "239":
                print(selected_value)
                self.dept_id = self.active_nested_dict.get(selected_value)
            else:
                self.dept_id = self.active_dept_dict.get(selected_value)

            self.cat_dropdown["values"] = list(dept_cat_map[self.dept_id].keys())
            self.prod_cat_dropdown.set("")
            self.prod_cat_dropdown["values"] = []
        elif triggered_widget == self.cat_dropdown:
            print(selected_value)
            nested_values = dept_cat_map[self.dept_id].get(selected_value, {})
            self.prod_cat_dropdown["values"] = list(nested_values.keys())

    def validate_and_submit(self, event=None):
        self.item_dept = self.dept_filter.get()
        self.item_cat = self.cat_filter.get()
        self.item_prod_cat = self.prod_cat.get()

        if not self.item_dept:
            messagebox.showerror("Error", "Please select a Department")
            return

        if not self.item_cat:
            messagebox.showerror("Error", "Please select a Category")
            return

        if not self.item_prod_cat:
            messagebox.showerror("Error", "Please select a Product Category")
            return

        self.item_prod_cat_id = dept_cat_map[self.dept_id][self.item_cat][
            self.item_prod_cat
        ]
        print(
            f"{self.selected_shop} : {self.item_dept} ; {self.item_cat} : {self.item_prod_cat}"
        )
        print(self.item_prod_cat_id)

        self.parent.selected_shop_id = self.shop_id
        self.parent.selected_dept_id = self.dept_id
        self.parent.selected_prod_cat_id = self.item_prod_cat_id
        self.parent.selected_dept = self.item_dept
        self.parent.selected_prod_cat = self.item_prod_cat

        self.parent.cat_label.config(text=self.item_prod_cat)

        self.destroy()

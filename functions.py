from NewItem import NewItem, MatrixParent, MatrixChild
import pandas as pd
from tkinter import messagebox, filedialog
import threading
import queue
from datetime import datetime
import os
from pathlib import Path
from data import tax_status
import sys

items_df = None
result_queue = queue.Queue()
worker_thread = None
atp_qty = None
chosen_color = None
chosen_brand = None

current_date = datetime.now()
date_string = current_date.strftime("%m%d%y")


def create_standalone(
    item_window,
    item_name,
    item_upc,
    item_shop_id,
    item_dept,
    item_cat,
    item_dept_id,
    item_prod_cat_id,
    item_cost,
    item_vendor,
    vendor_code,
    pref_vendor,
    base_price,
    dept_price,
    oos_message,
):

    if all(
        v is None
        for v in (
            item_name,
            item_upc,
            item_shop_id,
            item_dept,
            item_cat,
            item_dept_id,
            item_prod_cat_id,
            item_cost,
            item_vendor,
            vendor_code,
            base_price,
            dept_price,
            oos_message,
        )
    ):
        new_standalone = NewItem(
            item_name,
            item_upc,
            item_dept,
            item_cat,
            item_dept_id,
            item_prod_cat_id,
            item_cost,
            item_vendor,
            vendor_code,
            pref_vendor,
            base_price,
            dept_price,
            oos_message,
        )

        new_standalone.tax = set_tax_status(item_shop_id, item_prod_cat_id)
        new_standalone.income_account, new_standalone.income_acct_id = set_income_acct(
            item_shop_id, item_dept_id
        )

        return new_standalone
    else:
        messagebox.showerror("Error", "Please fill all fields.")
        return False


def create_parent(
    item_window,
    item_name,
    item_shop_id,
    item_dept,
    item_cat,
    item_dept_id,
    item_prod_cat_id,
    item_vendor,
    pref_vendor,
):
    parent_item = MatrixParent(
        item_name,
        item_dept,
        item_cat,
        item_dept_id,
        item_prod_cat_id,
        item_vendor,
        pref_vendor,
    )
    parent_item.tax = set_tax_status(item_shop_id, item_prod_cat_id)
    parent_item.income_account, parent_item.income_acct_id = set_income_acct(
        item_shop_id, item_dept_id
    )
    return parent_item


def set_tax_status(shop_id, prod_cat_id):
    if shop_id == "239":
        tax_schedule = "Not Taxable"
    else:
        if prod_cat_id in tax_status["Taxable RI"]:
            tax_schedule = "Taxable RI"
        elif prod_cat_id in tax_status["Not Taxable"]:
            tax_schedule = "Not Taxable"
        else:
            raise ValueError
    return tax_schedule


def set_income_acct(shop_id, dept_id):
    if shop_id == "239":
        if dept_id in ["244", "243", "240", "242", "241"]:
            income_account = "Apparel-Mens & Unisex (0354)"
            income_acct_id = "1129"
        elif dept_id in ["353", "354", "355", "356", "357"]:
            income_account = "Apparel-Womens (0354)"
            income_acct_id = "1132"
        elif dept_id in ["359", "360", "361", "362", "363"]:
            income_account = "Apparel-Youth (0354)"
            income_acct_id = "1133"
    elif shop_id == "245":
        income_account = "BUBS Campus Gift & Memorabilia (0365)"
        income_acct_id = "1335"
    elif shop_id == "250":
        if dept_id in ["253", "256", "252", "251"]:
            income_account = "BUBS General Merchandise (0355)"
            income_acct_id = "1435"
        elif dept_id == "365":
            income_account = "BUBS General Food/Beverage (0359)"
            income_acct_id = "1635"
        elif dept_id == "254":
            income_account = "BUBS General HBA (0359)"
            income_acct_id = "1551"
    return income_account, income_acct_id


def thread_wrapper(
    new_item,
    web_field_window,
    web_name,
    web_desc,
    oos_message,
    add_atp,
    filter_color,
    filter_brand,
    result_queue,
):

    try:
        check_optionals(web_field_window, add_atp, filter_color, filter_brand)
        pass_web_fields(
            new_item,
            web_name,
            web_desc,
            oos_message,
            atp_qty,
            chosen_color,
            chosen_brand,
        )
        result_queue.put(True)
    except Exception as e:
        result_queue.put(False, str(e))


def web_submit_click(self, new_item):
    global worker_thread

    web_field_window = self
    app = self.parent
    web_name = self.web_name_entry.get()
    web_desc = self.web_desc_box.get("1.0", "end")
    oos_message = self.oos_message.get()
    add_atp = self.add_atp.get()
    filter_color = self.filter_color.get()
    filter_brand = self.filter_brand.get()

    worker_thread = threading.Thread(
        target=thread_wrapper,
        args=(
            new_item,
            web_field_window,
            web_name,
            web_desc,
            oos_message,
            add_atp,
            filter_color,
            filter_brand,
            result_queue,
        ),
        daemon=True,
    )
    worker_thread.start()

    check_thread_status(new_item, self, app)


def check_thread_status(new_item, self, app):
    global worker_thread

    if worker_thread and worker_thread.is_alive():
        self.after(100, lambda: check_thread_status(new_item, self, app))
        return

    if isinstance(new_item, dict):
        create_matrix_df(app, new_item)
    else:
        create_df(new_item, app)


def generate_children(
    matrix, **kwargs
):  # kwargs are colors, sizes, logos, and namedrops
    try:
        matrix_parent = next(iter(matrix))
    except StopIteration:
        print("Error: The dictionary has been deleted or is empty")
        return

    child_items = matrix[matrix_parent]

    for key, value in kwargs.items():  # for value in color[values]
        if child_items:
            updated_matrix = []
            for child in matrix[matrix_parent]:  # for child item in matrix
                new_children = child.add_options(
                    **{key: value}
                )  # run through add_options
                updated_matrix.extend(
                    new_children
                )  # add list of new children to empty matrix

            matrix[matrix_parent] = (
                updated_matrix  # update main matrix dict with new values
            )
        else:
            matrix[matrix_parent] = MatrixChild(
                matrix_parent, matrix_parent.name
            ).add_options(**{key: value})
    return matrix[matrix_parent]


def create_children(options_window, parent_item, colors, sizes, logos, namedrops):
    matrix_item = {parent_item: []}
    print(parent_item.name)

    selected_color_indices = colors.curselection()
    selected_colors = [colors.get(c) for c in selected_color_indices]
    print(selected_colors)
    if selected_colors:
        parent_item.item_options.append("Color")
        matrix_item[parent_item] = generate_children(matrix_item, color=selected_colors)

    print([item.name for child_items in matrix_item.values() for item in child_items])

    selected_size_indices = sizes.curselection()
    selected_sizes = [sizes.get(s) for s in selected_size_indices]
    print(selected_sizes)
    if selected_sizes:
        parent_item.item_options.append("Size")
        matrix_item[parent_item] = generate_children(matrix_item, size=selected_sizes)

    print([item.name for child_items in matrix_item.values() for item in child_items])

    selected_logo_indices = logos.curselection()
    selected_logos = [logos.get(l) for l in selected_logo_indices]
    print(selected_logos)
    if selected_logos:
        parent_item.item_options.append("Logo")
        matrix_item[parent_item] = generate_children(matrix_item, logo=selected_logos)

    print([item.name for child_items in matrix_item.values() for item in child_items])

    selected_namedrop_indices = namedrops.curselection()
    selected_namedrops = [namedrops.get(n) for n in selected_namedrop_indices]
    print(selected_namedrops)
    if selected_namedrops:
        parent_item.item_options.append("Namedrop")
        matrix_item[parent_item] = generate_children(
            matrix_item, namedrop=selected_namedrops
        )

    print([item.name for child_items in matrix_item.values() for item in child_items])

    return matrix_item


def next_child(
    self,
    children,
    item=None,
    upc=None,
    cost=None,
    vendor_code=None,
    base_price=None,
    dept_price=None,
    color_filter=None,
    oos_message=None,
):
    updated_children = []
    if item:
        child_detail = MatrixChild.child_fields(
            item,
            upc,
            cost,
            vendor_code,
            base_price,
            dept_price,
            color_filter,
            oos_message,
        )
        if not MatrixChild.check_child_fields(item):
            return
        else:
            print(child_detail)
            updated_children.append(item)
            print([child.name for child in children])
            self.destroy()
    else:
        pass
    return updated_children


def pass_web_fields(
    new_item,
    web_name,
    web_desc,
    oos_message,
    atp_qty,
    color_filter,
    brand_filter,
):
    if isinstance(new_item, dict):
        for parent, children in new_item.items():
            parent.web_data(web_name, web_desc, oos_message, atp_qty, brand_filter)
            for child in children:
                child.update_attributes()
    else:
        new_item.web_data(
            web_name, web_desc, oos_message, atp_qty, color_filter, brand_filter
        )


def create_df(new_item, app):
    global items_df

    print(new_item)

    new_df = pd.DataFrame([vars(new_item)])
    new_df = new_df[
        [
            "name",
            "upc",
            "department",
            "dept_id",
            "category",
            "cat_id",
            "vendor",
            "vendor_id",
            "pref_vendor",
            "vendor_code",
            "cost",
            "tax",
            "cogs_account",
            "cogs_acct_id",
            "asset_account",
            "asset_acct_id",
            "income_account",
            "income_acct_id",
            "base_price",
            "dept_price",
            "oos_message",
            "oos_message_id",
            "atp_qty",
            "web_name",
            "web_desc",
            "filter_color",
            "filter_color_id",
            "filter_brand",
            "filter_brand_id",
            "page_title",
            "meta_tag",
            "url_component",
            "web_image_name",
        ]
    ]

    if items_df is None:
        items_df = new_df
    else:
        items_df = pd.concat([items_df, new_df], ignore_index=True)

    print(items_df)
    app.destroy()

    create_another = messagebox.askyesno(
        title="Item Created", message="Create another item?"
    )

    if create_another:
        from AppWindow import LoneItemWindow

        LoneItemWindow(app.parent)
    else:
        success, message = save_and_export(items_df)
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showinfo("Error", f"Failed to save import sheet: {message}.")

        sys.exit()


def create_matrix_df(app, matrix_item):
    global items_df

    item = []
    for parent, children in matrix_item.items():
        item.append(parent)
        if isinstance(children, list):
            item.extend(children)
        else:
            item.append(children)

    print(list(item))

    new_df = pd.DataFrame([vars(i) for i in item])
    new_df["item_options"] = new_df["item_options"].apply(", ".join)
    new_df = new_df.drop(["parent"], axis=1)
    new_df[
        [
            "name",
            "upc",
            "department",
            "dept_id",
            "category",
            "cat_id",
            "vendor",
            "vendor_id",
            "pref_vendor",
            "vendor_code",
            "cost",
            "tax",
            "matrix_type",
            "cogs_account",
            "cogs_acct_id",
            "asset_account",
            "asset_acct_id",
            "income_account",
            "income_acct_id",
            "item_options",
            "parent_name",
            "base_price",
            "dept_price",
            "oos_message",
            "oos_message_id",
            "atp_qty",
            "web_name",
            "web_desc",
            "filter_color",
            "filter_color_id",
            "filter_brand",
            "filter_brand_id",
            "page_title",
            "meta_tag",
            "url_component",
            "web_image_name",
            "color",
            "color_id",
            "size",
            "size_id",
            "logo",
            "logo_id",
            "namedrop",
            "namedrop_id",
        ]
    ]  # incorporate remaining internal ids for vendor, cogs, asset, tax(?), color filter, brand filter, color, size, logo, namedrop, oos message

    if items_df is None:
        items_df = new_df
    else:
        items_df = pd.concat([items_df, new_df], ignore_index=True)

    print(items_df.to_dict())
    app.destroy()

    create_another = messagebox.askyesno(
        title="Item Created", message="Create another item?"
    )

    if create_another:
        from AppWindow import MatrixParentWindow

        MatrixParentWindow(app.parent)
    else:
        success, message = save_and_export(items_df)
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showinfo("Error", f"Failed to save import sheet: {message}.")

        sys.exit()


def check_optionals(self, *args):
    global atp_qty, chosen_color, chosen_brand

    atp_yes = self.add_atp.get()
    color_yes = self.filter_color.get()
    brand_yes = self.filter_brand.get()

    if atp_yes == True:
        atp_qty = self.atp_qty_entry.get()
    else:
        atp_qty = ""

    if color_yes == True:
        chosen_color = self.filtered_color.get()
    else:
        chosen_color = ""

    if brand_yes == True:
        chosen_brand = self.filtered_brand.get()
    else:
        chosen_brand = ""


def save_and_export(items_df):
    initialdir = os.getcwd()

    save_directory = filedialog.asksaveasfilename(
        initialdir=initialdir, initialfile=f"NewItems-{date_string}.xlsx"
    )

    try:
        with pd.ExcelWriter(save_directory, engine="openpyxl") as writer:
            items_df.to_excel(writer, sheet_name="NewItems", index=False)
        message = "Excel ready for import to NetSuite."
        return True, message
    except Exception as e:
        return False, str(e)


def go_back(self):
    from main import SplashWindow

    self.destroy()
    SplashWindow(self.parent)

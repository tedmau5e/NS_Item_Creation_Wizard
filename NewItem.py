from tkinter import messagebox
from data import (
    vendor_list,
    web_behavior,
    color_filter,
    brand_filter,
    color_options,
    size_options,
    logo_options,
    namedrop_options,
)


class NewItem:
    base_fields = [
        "name",
        "upc",
        "department",
        "category",
        "cost",
        "vendor",
        "vendor_id",
        "vendor_code",
        "base_price",
        "dept_price",
        "oos_message",
        "oos_message_id",
    ]

    def __init__(
        self,
        name,
        upc_code,
        department,
        category,
        dept_id,
        cat_id,
        cost,
        vendor,
        vendor_code,
        pref_vendor,
        base_price,
        dept_price,
        oos_message,
    ):
        self.name = name
        self.upc = upc_code
        self.department = department
        self.category = category
        self.dept_id = dept_id
        self.cat_id = cat_id
        self.tax = None
        self.cost = cost
        self.vendor = vendor
        if self.vendor:
            self.vendor_id = vendor_list[self.vendor]
        else:
            self.vendor_id = None
        self.vendor_code = vendor_code
        self.pref_vendor = pref_vendor
        self.base_price = base_price
        self.dept_price = dept_price
        self.cogs_account = "COGS Merchandise (3710)"
        self.cogs_acct_id = "219"
        self.asset_account = "Inventory - Merchandise (1400)"
        self.asset_acct_id = "218"
        self.income_account = "Default Sales"
        self.income_acct_id = "54"
        self.oos_message = oos_message
        if self.oos_message:
            self.oos_message_id = web_behavior[self.oos_message]
        else:
            self.oos_message_id = None
        self.web_name = None
        self.web_desc = None
        self.oos_message = None
        self.oos_message = None
        self.oos_message = None
        self.atp_qty = None
        self.filter_color = None
        self.filter_color_id = None
        self.filter_brand = None
        self.filter_brand_id = None
        self.page_title = None
        self.meta_tag = None
        self.url_component = None
        self.web_image_name = None

    def web_data(self, web_name, web_desc, atp_qty, filtered_color, filtered_brand):
        self.web_name = web_name
        display_name = self.web_name
        self.page_title = f"{display_name} | Brown Bookstore"
        self.meta_tag = f"<meta name='description' content='{display_name} available at the Brown Bookstore.'>"

        self.web_desc = web_desc
        self.atp_qty = atp_qty
        self.filter_color = filtered_color
        if self.filter_color:
            self.filter_color_id = color_filter[self.filter_color]
        else:
            self.filter_color_id = None
        self.filter_brand = filtered_brand
        if self.filter_brand:
            self.filter_brand_id = brand_filter[self.filter_brand]
        else:
            self.filter_brand_id = None

        self.url_component = display_name.replace(
            " ", "-"
        )  # substitute display_name with "-" between words
        self.web_image_name = self.name.replace(
            " ", "-"
        )  # substitute name with "-" between words

    def check_upc(self):
        for attr_name, value in self.__dict__.items():
            print(attr_name, value)
            if attr_name == "upc":
                if len(value) != 12:
                    messagebox.showerror("Error", f"{attr_name} must be 12 digits")
                    return False
            else:
                pass
        return True


class MatrixParent:
    def __init__(
        self, name, department, category, dept_id, cat_id, vendor, pref_vendor
    ):
        self.name = name
        self.department = department
        self.category = category
        self.dept_id = dept_id
        self.cat_id = cat_id
        self.vendor = vendor
        self.vendor_id = vendor_list[vendor]
        self.pref_vendor = pref_vendor
        self.item_options = []
        self.cogs_account = "COGS Merchandise (3710)"
        self.cogs_acct_id = "219"
        self.asset_account = "Inventory - Merchandise (1400)"
        self.asset_acct_id = "218"
        self.income_account = "Default Sales"
        self.income_acct_id = "54"
        self.tax = None
        self.matrix_type = "Parent Matrix Item"
        self.web_name = None
        self.web_desc = None
        self.oos_message = None
        self.oos_message_id = None
        self.atp_qty = None
        self.filter_color = None
        self.filter_color_id = None
        self.filter_brand = None
        self.filter_brand_id = None
        self.page_title = None
        self.meta_tag = None
        self.url_component = None
        self.web_image_name = None

    def web_data(self, web_name, web_desc, oos_message, atp_qty, filtered_brand):
        self.web_name = web_name
        display_name = self.web_name
        self.page_title = f"{display_name} | Brown Bookstore"
        self.meta_tag = f"<meta name='description' content='{display_name} available at the Brown Bookstore.'>"

        self.web_desc = web_desc
        self.oos_message = oos_message
        self.oos_message_id = web_behavior[self.oos_message]
        self.atp_qty = atp_qty
        self.filter_brand = filtered_brand
        if self.filter_brand:
            self.filter_brand_id = brand_filter[self.filter_brand]
        else:
            self.filter_brand_id = None

        self.url_component = display_name.replace(
            " ", "-"
        )  # substitute display_name with "-" between words
        self.web_image_name = self.name.replace(
            " ", "-"
        )  # substitute name with "-" between words

    def check_base_fields(self):
        for attr_name, value in self.__dict__.items():
            print(attr_name, value)
            if attr_name in self.base_fields:
                if attr_name == "upc":
                    if len(value) != 12:
                        messagebox.showerror("Error", f"{attr_name} must be 12 digits")
                        return False
                if not value:
                    messagebox.showerror("Error", f"{attr_name} cannot be empty")
                    return False
            else:
                pass
        return True


class MatrixChild:
    child_excl_fields = [
        "upc",
        "cost",
        "vendor_code",
        "base_price",
        "dept_price",
        "oos_message",
    ]

    def __init__(
        self,
        parent_item,
        name,
        color=None,
        color_id=None,
        size=None,
        size_id=None,
        logo=None,
        logo_id=None,
        namedrop=None,
        namedrop_id=None,
    ):
        self.parent = parent_item
        self.parent_name = self.parent.name
        self.department = self.parent.department
        self.category = self.parent.category
        self.dept_id = self.parent.dept_id
        self.cat_id = self.parent.cat_id
        self.vendor = self.parent.vendor
        self.vendor_id = self.parent.vendor_id
        self.pref_vendor = self.parent.pref_vendor
        self.item_options = self.parent.item_options
        self.tax = self.parent.tax
        self.matrix_type = "Child Matrix Item"
        self.cogs_account = self.parent.cogs_account
        self.cogs_acct_id = self.parent.cogs_acct_id
        self.asset_account = self.parent.asset_account
        self.asset_acct_id = self.parent.asset_acct_id
        self.income_account = self.parent.income_account
        self.income_acct_id = self.parent.income_acct_id
        self.atp_qty = None
        self.filter_brand = None
        self.filter_brand_id = None
        self.filter_color = None
        self.filter_color_id = None
        self.oos_message = None
        self.oos_message_id = None
        self.name = name
        self.color = color
        self.color_id = color_id
        self.size = size
        self.size_id = size_id
        self.logo = logo
        self.logo_id = logo_id
        self.namedrop = namedrop
        self.namedrop_id = namedrop_id
        self.upc = None
        self.cost = None
        self.vendor_code = None
        self.base_price = None
        self.dept_price = None

    def add_options(self, **kwargs):
        for key, value in kwargs.items():
            new_items = []
            if key == "color":
                for v in range(len(value)):
                    new_child = MatrixChild(
                        parent_item=self.parent,
                        name=f"{self.name}|{value[v]}",
                        color=value[v],
                        color_id=color_options[value[v]],
                    )
                    new_items.append(new_child)
                return new_items
            if key == "size":
                for v in range(len(value)):
                    new_child = MatrixChild(
                        parent_item=self.parent,
                        name=f"{self.name}|{value[v]}",
                        color=self.color,
                        color_id=self.color_id,
                        size=value[v],
                        size_id=size_options[value[v]],
                    )
                    new_items.append(new_child)
                return new_items
            if key == "logo":
                for v in range(len(value)):
                    new_child = MatrixChild(
                        parent_item=self.parent,
                        name=f"{self.name}|{value[v]}",
                        color=self.color,
                        color_id=self.color_id,
                        size=self.size,
                        size_id=self.size_id,
                        logo=value,
                        logo_id=logo_options[value[v]],
                    )
                    new_items.append(new_child)
                return new_items
            if key == "namedrop":
                for v in range(len(value)):
                    new_child = MatrixChild(
                        parent_item=self.parent,
                        name=f"{self.name}|{value[v]}",
                        color=self.color,
                        color_id=self.color_id,
                        size=self.size,
                        size_id=self.size_id,
                        logo=self.logo,
                        logo_id=self.logo_id,
                        namedrop=value,
                        namedrop_id=namedrop_options[value[v]],
                    )
                    new_items.append(new_child)
                return new_items

    def child_fields(
        self,
        upc,
        cost,
        vendor_code,
        base_price,
        dept_price,
        filtered_color,
        oos_message,
    ):
        self.upc = upc
        self.cost = cost
        self.vendor_code = vendor_code
        self.base_price = base_price
        self.dept_price = dept_price
        self.filter_color = filtered_color
        if self.filter_color:
            self.filter_color_id = color_filter[self.filter_color]
        else:
            self.filter_color_id = None
        self.oos_message = oos_message
        if self.oos_message:
            self.oos_message_id = web_behavior[oos_message]
        else:
            self.oos_message_id = None
        return self

    def update_attributes(self):
        self.atp_qty = self.parent.atp_qty
        self.filter_brand = self.parent.filter_brand
        self.filter_brand_id = self.parent.filter_brand_id

    def check_child_fields(item):
        for attr_name, value in item.__dict__.items():
            print(attr_name, value)
            if attr_name in MatrixChild.child_excl_fields:
                if attr_name == "upc":
                    if len(value) != 12:
                        messagebox.showerror("Error", f"{attr_name} must be 12 digits")
                        return False
                if not value:
                    messagebox.showerror("Error", f"{attr_name} cannot be empty")
                    return False
        return True

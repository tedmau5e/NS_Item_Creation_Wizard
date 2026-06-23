import tkinter as tk


class TwoDecimalEntry(tk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        vcmd = (self.register(self.validate_input), "%P")

        self.config(validate="key", validatecommand=vcmd)

    def validate_input(self, proposed_text):
        if proposed_text == "":
            return True

        if proposed_text.count(".") > 1:
            return False

        if proposed_text in ["-", ".", "-."]:
            return True

        try:
            float(proposed_text)

            if "." in proposed_text:
                decimal_part = proposed_text.split(".")[1]
                if len(decimal_part) > 2:
                    return False
            return True
        except ValueError:
            return False

from tkinter import ttk, messagebox
from models import Material
from .widgets import make_tree, labeled_entry, selected_id, fmt_money


class MaterialsTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app, self.store = app, app.store

        form = ttk.LabelFrame(self, text="مشخصات مصالح")
        form.pack(fill="x", padx=8, pady=8)
        self.v_name = labeled_entry(form, "نام:", 0)
        self.v_unit = labeled_entry(form, "واحد:", 0, col=2, width=10)
        self.v_price = labeled_entry(form, "قیمت واحد:", 0, col=4, width=14)

        btns = ttk.Frame(form)
        btns.grid(row=1, column=0, columnspan=6, pady=4)
        ttk.Button(btns, text="افزودن", command=self.add).pack(side="left", padx=4)
        ttk.Button(btns, text="ویرایش", command=self.update).pack(side="left", padx=4)
        ttk.Button(btns, text="حذف", command=self.delete).pack(side="left", padx=4)

        frame, self.tree = make_tree(self, [("name", "نام", 200), ("unit", "واحد", 80),
                                            ("price", "قیمت واحد", 130), ("used", "تعداد پروژه‌ها", 110)])
        frame.pack(fill="both", expand=True, padx=8, pady=8)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for m in self.store.materials:
            self.tree.insert("", "end", iid=m.id, values=(
                m.name, m.unit, fmt_money(m.unit_price), len(self.store.projects_using(m.id))))

    def on_select(self, _=None):
        m = self.store.get_material(selected_id(self.tree))
        if m:
            self.v_name.set(m.name)
            self.v_unit.set(m.unit)
            self.v_price.set(f"{m.unit_price:g}")

    def clear(self):
        for v in (self.v_name, self.v_unit, self.v_price):
            v.set("")

    def add(self):
        try:
            self.store.add_material(Material(self.v_name.get(), self.v_unit.get(), self.v_price.get()))
        except ValueError as e:
            return messagebox.showerror("خطا", str(e))
        self.clear()
        self.app.commit()

    def update(self):
        m = self.store.get_material(selected_id(self.tree))
        if not m:
            return messagebox.showinfo("توجه", "ابتدا یک ماده را انتخاب کنید.")
        try:
            m.name, m.unit, m.unit_price = self.v_name.get(), self.v_unit.get(), self.v_price.get()
        except ValueError as e:
            return messagebox.showerror("خطا", str(e))
        self.app.commit()

    def delete(self):
        id = selected_id(self.tree)
        if not id:
            return
        try:
            self.store.remove_material(id)
        except ValueError as e:
            return messagebox.showerror("خطا", str(e))
        self.clear()
        self.app.commit()

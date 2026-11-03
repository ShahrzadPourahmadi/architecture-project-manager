from tkinter import ttk, messagebox
from models import Architect
from .widgets import make_tree, labeled_entry, selected_id


class ArchitectsTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app, self.store = app, app.store

        form = ttk.LabelFrame(self, text="مشخصات معمار")
        form.pack(fill="x", padx=8, pady=8)
        self.v_name = labeled_entry(form, "نام:", 0)
        self.v_spec = labeled_entry(form, "تخصص:", 0, col=2)
        self.v_phone = labeled_entry(form, "تلفن:", 0, col=4)

        btns = ttk.Frame(form)
        btns.grid(row=1, column=0, columnspan=6, pady=4)
        ttk.Button(btns, text="افزودن", command=self.add).pack(side="left", padx=4)
        ttk.Button(btns, text="ویرایش", command=self.update).pack(side="left", padx=4)
        ttk.Button(btns, text="حذف", command=self.delete).pack(side="left", padx=4)

        frame, self.tree = make_tree(self, [("name", "نام", 200), ("spec", "تخصص", 160),
                                            ("phone", "تلفن", 140), ("count", "تعداد پروژه", 90)])
        frame.pack(fill="both", expand=True, padx=8, pady=8)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for a in self.store.architects:
            self.tree.insert("", "end", iid=a.id, values=(
                a.name, a.specialty, a.phone, len(self.store.projects_of(a.id))))

    def on_select(self, _=None):
        a = self.store.get_architect(selected_id(self.tree))
        if a:
            self.v_name.set(a.name)
            self.v_spec.set(a.specialty)
            self.v_phone.set(a.phone)

    def clear(self):
        for v in (self.v_name, self.v_spec, self.v_phone):
            v.set("")

    def add(self):
        try:
            self.store.add_architect(Architect(self.v_name.get(), self.v_spec.get(), self.v_phone.get()))
        except ValueError as e:
            return messagebox.showerror("خطا", str(e))
        self.clear()
        self.app.commit()

    def update(self):
        a = self.store.get_architect(selected_id(self.tree))
        if not a:
            return messagebox.showinfo("توجه", "ابتدا یک معمار را انتخاب کنید.")
        try:
            a.name, a.specialty, a.phone = self.v_name.get(), self.v_spec.get(), self.v_phone.get()
        except ValueError as e:
            return messagebox.showerror("خطا", str(e))
        self.app.commit()

    def delete(self):
        id = selected_id(self.tree)
        if not id:
            return
        try:
            self.store.remove_architect(id)
        except ValueError as e:
            return messagebox.showerror("خطا", str(e))
        self.clear()
        self.app.commit()

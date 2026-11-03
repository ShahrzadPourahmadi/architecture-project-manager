import tkinter as tk
from tkinter import ttk, messagebox
from models import Project
from .widgets import make_tree, labeled_entry, selected_id, fmt_money


class ProjectsTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app, self.store, self.reports = app, app.store, app.reports
        self._architect_ids = []
        self._material_ids = []
        self.current = None  # پروژه انتخاب‌شده

        self._build_project_section()
        details = ttk.Frame(self)
        details.pack(fill="both", expand=True, padx=8, pady=4)
        self._build_phase_section(details)
        self._build_material_section(details)

    # ================= پروژه‌ها =================
    def _build_project_section(self):
        form = ttk.LabelFrame(self, text="پروژه")
        form.pack(fill="x", padx=8, pady=6)
        self.v_name = labeled_entry(form, "نام پروژه:", 0)
        ttk.Label(form, text="معمار:").grid(row=0, column=2, padx=4, sticky="e")
        self.cb_arch = ttk.Combobox(form, state="readonly", width=20)
        self.cb_arch.grid(row=0, column=3, padx=4)
        self.v_budget = labeled_entry(form, "بودجه:", 0, col=4, width=16)

        btns = ttk.Frame(form)
        btns.grid(row=1, column=0, columnspan=6, pady=4)
        ttk.Button(btns, text="افزودن", command=self.add_project).pack(side="left", padx=4)
        ttk.Button(btns, text="ویرایش", command=self.update_project).pack(side="left", padx=4)
        ttk.Button(btns, text="حذف", command=self.delete_project).pack(side="left", padx=4)

        frame, self.tree = make_tree(self, [("name", "پروژه", 180), ("arch", "معمار", 150),
                                            ("budget", "بودجه", 120), ("prog", "میانگین پیشرفت", 110)],
                                     height=5)
        frame.pack(fill="x", padx=8)
        self.tree.bind("<<TreeviewSelect>>", self.on_project_select)

    def add_project(self):
        i = self.cb_arch.current()
        if i < 0:
            return messagebox.showerror("خطا", "ابتدا یک معمار انتخاب کنید (در تب معماران بسازید).")
        try:
            self.store.add_project(Project(self.v_name.get(), self._architect_ids[i], self.v_budget.get()))
        except ValueError as e:
            return messagebox.showerror("خطا", str(e))
        self.v_name.set("")
        self.v_budget.set("")
        self.app.commit()

    def update_project(self):
        if not self.current:
            return messagebox.showinfo("توجه", "ابتدا یک پروژه را انتخاب کنید.")
        i = self.cb_arch.current()
        try:
            self.current.name = self.v_name.get()
            self.current.budget = self.v_budget.get()
            if i >= 0:
                self.current.architect_id = self._architect_ids[i]
        except ValueError as e:
            return messagebox.showerror("خطا", str(e))
        self.app.commit()

    def delete_project(self):
        if not self.current:
            return
        if messagebox.askyesno("تأیید", f"پروژه «{self.current.name}» حذف شود؟"):
            self.store.remove_project(self.current.id)
            self.current = None
            self.app.commit()

    def on_project_select(self, _=None):
        self.current = self.store.get_project(selected_id(self.tree))
        if not self.current:
            return
        self.v_name.set(self.current.name)
        self.v_budget.set(f"{self.current.budget:g}")
        if self.current.architect_id in self._architect_ids:
            self.cb_arch.current(self._architect_ids.index(self.current.architect_id))
        self.refresh_details()

    # ================= فازها =================
    def _build_phase_section(self, parent):
        box = ttk.LabelFrame(parent, text="فازها و پیشرفت")
        box.pack(side="left", fill="both", expand=True, padx=(0, 4))
        row = ttk.Frame(box)
        row.pack(fill="x", pady=4)
        self.v_phase = tk.StringVar()
        ttk.Entry(row, textvariable=self.v_phase, width=16).pack(side="left", padx=3)
        self.v_progress = tk.DoubleVar(value=0)
        ttk.Scale(row, from_=0, to=100, variable=self.v_progress,
                  command=lambda v: self.lbl_prog.config(text=f"{float(v):.0f}%")
                  ).pack(side="left", padx=3, fill="x", expand=True)
        self.lbl_prog = ttk.Label(row, text="0%", width=5)
        self.lbl_prog.pack(side="left")

        row2 = ttk.Frame(box)
        row2.pack(pady=2)
        ttk.Button(row2, text="افزودن فاز", command=self.add_phase).pack(side="left", padx=3)
        ttk.Button(row2, text="ثبت پیشرفت", command=self.update_phase).pack(side="left", padx=3)
        ttk.Button(row2, text="حذف", command=self.delete_phase).pack(side="left", padx=3)

        frame, self.phase_tree = make_tree(box, [("name", "فاز", 140), ("prog", "پیشرفت", 80)], height=6)
        frame.pack(fill="both", expand=True, padx=4, pady=4)
        self.phase_tree.bind("<<TreeviewSelect>>", self.on_phase_select)
        self.lbl_avg = ttk.Label(box, text="میانگین پیشرفت: ۰٪")
        self.lbl_avg.pack(pady=2)

    def _need_project(self):
        if not self.current:
            messagebox.showinfo("توجه", "ابتدا یک پروژه را انتخاب کنید.")
            return False
        return True

    def _phase_index(self):
        sel = self.phase_tree.selection()
        return int(sel[0]) if sel else None

    def add_phase(self):
        if not self._need_project():
            return
        try:
            self.current.add_phase(self.v_phase.get(), self.v_progress.get())
        except ValueError as e:
            return messagebox.showerror("خطا", str(e))
        self.v_phase.set("")
        self.app.commit()

    def update_phase(self):
        if not self._need_project():
            return
        i = self._phase_index()
        if i is None:
            return messagebox.showinfo("توجه", "ابتدا یک فاز را انتخاب کنید.")
        try:
            phase = self.current.phases[i]
            phase.name = self.v_phase.get()
            phase.progress = self.v_progress.get()
        except ValueError as e:
            return messagebox.showerror("خطا", str(e))
        self.app.commit()

    def delete_phase(self):
        i = self._phase_index()
        if self.current and i is not None:
            self.current.remove_phase(i)
            self.app.commit()

    def on_phase_select(self, _=None):
        i = self._phase_index()
        if self.current and i is not None:
            p = self.current.phases[i]
            self.v_phase.set(p.name)
            self.v_progress.set(p.progress)
            self.lbl_prog.config(text=f"{p.progress:.0f}%")

    # ================= مصالح =================
    def _build_material_section(self, parent):
        box = ttk.LabelFrame(parent, text="مصالح پروژه و هزینه")
        box.pack(side="left", fill="both", expand=True, padx=(4, 0))
        row = ttk.Frame(box)
        row.pack(fill="x", pady=4)
        self.cb_mat = ttk.Combobox(row, state="readonly", width=18)
        self.cb_mat.pack(side="left", padx=3)
        ttk.Label(row, text="مقدار:").pack(side="left")
        self.v_qty = tk.StringVar()
        ttk.Entry(row, textvariable=self.v_qty, width=8).pack(side="left", padx=3)

        row2 = ttk.Frame(box)
        row2.pack(pady=2)
        ttk.Button(row2, text="افزودن / تغییر مقدار", command=self.set_material).pack(side="left", padx=3)
        ttk.Button(row2, text="حذف", command=self.remove_material).pack(side="left", padx=3)

        frame, self.mat_tree = make_tree(box, [("name", "ماده", 110), ("qty", "مقدار", 60),
                                               ("price", "قیمت واحد", 80), ("total", "جمع", 100)], height=6)
        frame.pack(fill="both", expand=True, padx=4, pady=4)
        self.mat_tree.bind("<<TreeviewSelect>>", self.on_mat_select)
        self.lbl_cost = ttk.Label(box, text="هزینه مصالح: ۰")
        self.lbl_cost.pack(pady=2)

    def set_material(self):
        if not self._need_project():
            return
        i = self.cb_mat.current()
        if i < 0:
            return messagebox.showerror("خطا", "یک ماده انتخاب کنید.")
        try:
            self.current.set_material(self._material_ids[i], self.v_qty.get())
        except ValueError as e:
            return messagebox.showerror("خطا", str(e))
        self.app.commit()

    def remove_material(self):
        id = selected_id(self.mat_tree)
        if self.current and id:
            self.current.remove_material(id)
            self.app.commit()

    def on_mat_select(self, _=None):
        id = selected_id(self.mat_tree)
        if self.current and id and id in self._material_ids:
            self.cb_mat.current(self._material_ids.index(id))
            self.v_qty.set(f"{self.current.get_usage(id).quantity:g}")

    # ================= نمایش =================
    def refresh(self):
        # لیست‌های انتخابی
        self._architect_ids = [a.id for a in self.store.architects]
        self.cb_arch["values"] = [a.name for a in self.store.architects]
        self._material_ids = [m.id for m in self.store.materials]
        self.cb_mat["values"] = [str(m) for m in self.store.materials]

        # جدول پروژه‌ها
        self.tree.delete(*self.tree.get_children())
        for p in self.store.projects:
            a = self.store.get_architect(p.architect_id)
            self.tree.insert("", "end", iid=p.id, values=(
                p.name, a.name if a else "-", fmt_money(p.budget), f"{p.average_progress:.1f}%"))
        if self.current and self.store.get_project(self.current.id):
            self.tree.selection_set(self.current.id)
        else:
            self.current = None
        self.refresh_details()

    def refresh_details(self):
        self.phase_tree.delete(*self.phase_tree.get_children())
        self.mat_tree.delete(*self.mat_tree.get_children())
        if not self.current:
            self.lbl_avg.config(text="میانگین پیشرفت: ۰٪")
            self.lbl_cost.config(text="هزینه مصالح: ۰")
            return
        for i, p in enumerate(self.current.phases):
            self.phase_tree.insert("", "end", iid=str(i), values=(p.name, f"{p.progress:.0f}%"))
        for m, qty, total in self.reports.material_lines(self.current):
            self.mat_tree.insert("", "end", iid=m.id, values=(
                m.name, f"{qty:g} {m.unit}", fmt_money(m.unit_price), fmt_money(total)))
        self.lbl_avg.config(text=f"میانگین پیشرفت: {self.current.average_progress:.1f}%")
        self.lbl_cost.config(text=f"هزینه مصالح: {fmt_money(self.reports.material_cost(self.current))}")

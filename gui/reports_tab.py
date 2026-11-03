import tkinter as tk
from tkinter import ttk
from .widgets import make_tree, fmt_money


class ReportsTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app, self.store, self.reports = app, app.store, app.reports

        top = ttk.Frame(self)
        top.pack(fill="x", padx=8, pady=6)
        self.lbl_overall = ttk.Label(top, text="", font=("TkDefaultFont", 11, "bold"))
        self.lbl_overall.pack(side="left")
        ttk.Button(top, text="به‌روزرسانی", command=self.refresh).pack(side="right")

        box = ttk.LabelFrame(self, text="گزارش بودجه پروژه‌ها")
        box.pack(fill="both", expand=True, padx=8, pady=4)
        frame, self.tree = make_tree(box, [
            ("project", "پروژه", 140), ("arch", "معمار", 110), ("budget", "بودجه", 100),
            ("cost", "هزینه مصالح", 100), ("remain", "باقی‌مانده", 100),
            ("used", "درصد مصرف", 80), ("prog", "پیشرفت", 70), ("status", "وضعیت", 90)], height=7)
        frame.pack(fill="both", expand=True, padx=4, pady=4)
        self.tree.tag_configure("over", foreground="#c0392b")

        box2 = ttk.LabelFrame(self, text="خلاصه معماران")
        box2.pack(fill="x", padx=8, pady=4)
        frame2, self.tree2 = make_tree(box2, [
            ("name", "معمار", 140), ("count", "پروژه‌ها", 70), ("budget", "جمع بودجه", 110),
            ("cost", "جمع هزینه", 110), ("prog", "میانگین پیشرفت", 110)], height=4)
        frame2.pack(fill="x", padx=4, pady=4)

        box3 = ttk.LabelFrame(self, text="نمودار میانگین پیشرفت پروژه‌ها")
        box3.pack(fill="x", padx=8, pady=4)
        self.canvas = tk.Canvas(box3, height=140, bg="white", highlightthickness=0)
        self.canvas.pack(fill="x", padx=4, pady=4)
        self.canvas.bind("<Configure>", lambda e: self.draw_chart())

    def refresh(self):
        self.lbl_overall.config(
            text=f"میانگین پیشرفت کل پروژه‌ها: {self.reports.overall_average_progress():.1f}%")

        self.tree.delete(*self.tree.get_children())
        for p in self.store.projects:
            r = self.reports.budget_report(p)
            a = self.store.get_architect(p.architect_id)
            self.tree.insert("", "end", tags=("over",) if r["over_budget"] else (), values=(
                p.name, a.name if a else "-", fmt_money(r["budget"]), fmt_money(r["cost"]),
                fmt_money(r["remaining"]), f"{r['percent_used']:.0f}%",
                f"{p.average_progress:.0f}%", "بیش از بودجه" if r["over_budget"] else "در محدوده"))

        self.tree2.delete(*self.tree2.get_children())
        for a in self.store.architects:
            s = self.reports.architect_summary(a)
            self.tree2.insert("", "end", values=(
                a.name, s["projects"], fmt_money(s["budget"]), fmt_money(s["cost"]),
                f"{s['avg_progress']:.1f}%"))
        self.draw_chart()

    def draw_chart(self):
        c = self.canvas
        c.delete("all")
        projects = self.store.projects
        if not projects:
            c.create_text(10, 20, anchor="w", text="پروژه‌ای ثبت نشده است.", fill="gray")
            return
        w, h = c.winfo_width(), c.winfo_height()
        bar_w = max(20, min(70, (w - 40) // len(projects) - 10))
        x = 30
        for p in projects:
            val = p.average_progress
            bar_h = (h - 40) * val / 100
            c.create_rectangle(x, h - 20 - bar_h, x + bar_w, h - 20, fill="#2e86c1", outline="")
            c.create_text(x + bar_w / 2, h - 24 - bar_h, text=f"{val:.0f}%", font=("TkDefaultFont", 8))
            c.create_text(x + bar_w / 2, h - 8, text=p.name[:10], font=("TkDefaultFont", 8))
            x += bar_w + 10

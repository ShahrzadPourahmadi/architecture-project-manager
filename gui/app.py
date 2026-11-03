import tkinter as tk
from tkinter import ttk
from storage import DataStore
from services import ReportService
from .architects_tab import ArchitectsTab
from .materials_tab import MaterialsTab
from .projects_tab import ProjectsTab
from .reports_tab import ReportsTab


class App(tk.Tk):
    def __init__(self, data_path="data.json"):
        super().__init__()
        self.title("مدیریت پروژه‌های معماری")
        self.geometry("980x700")
        self.store = DataStore(data_path)
        self.reports = ReportService(self.store)

        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        self.tabs = [
            (ArchitectsTab(self.notebook, self), "معماران"),
            (MaterialsTab(self.notebook, self), "مصالح"),
            (ProjectsTab(self.notebook, self), "پروژه‌ها"),
            (ReportsTab(self.notebook, self), "گزارش‌ها"),
        ]
        for tab, title in self.tabs:
            self.notebook.add(tab, text=title)
        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self.refresh_all())
        self.refresh_all()

    def refresh_all(self):
        for tab, _ in self.tabs:
            tab.refresh()

    def commit(self):
        """ذخیره داده‌ها و به‌روزرسانی همه تب‌ها"""
        self.store.save()
        self.refresh_all()

import json
import os
from models import Architect, Material, Project


class DataStore:
    """نگهداری داده‌ها در حافظه و ذخیره در فایل JSON"""

    def __init__(self, path="data.json"):
        self._path = path
        self._architects = []
        self._materials = []
        self._projects = []
        self.load()

    # ---- getters ----
    @property
    def architects(self):
        return self._architects

    @property
    def materials(self):
        return self._materials

    @property
    def projects(self):
        return self._projects

    def get_architect(self, id):
        return next((a for a in self._architects if a.id == id), None)

    def get_material(self, id):
        return next((m for m in self._materials if m.id == id), None)

    def get_project(self, id):
        return next((p for p in self._projects if p.id == id), None)

    def projects_of(self, architect_id):
        return [p for p in self._projects if p.architect_id == architect_id]

    def projects_using(self, material_id):
        return [p for p in self._projects if p.get_usage(material_id)]

    # ---- add / remove ----
    def add_architect(self, a):
        self._architects.append(a)

    def remove_architect(self, id):
        if self.projects_of(id):
            raise ValueError("این معمار پروژه فعال دارد؛ ابتدا پروژه‌هایش را حذف کنید.")
        self._architects = [a for a in self._architects if a.id != id]

    def add_material(self, m):
        self._materials.append(m)

    def remove_material(self, id):
        if self.projects_using(id):
            raise ValueError("این مصالح در پروژه‌ها استفاده شده است.")
        self._materials = [m for m in self._materials if m.id != id]

    def add_project(self, p):
        if not self.get_architect(p.architect_id):
            raise ValueError("معمار انتخاب‌شده وجود ندارد.")
        self._projects.append(p)

    def remove_project(self, id):
        self._projects = [p for p in self._projects if p.id != id]

    # ---- persistence ----
    def save(self):
        data = {"architects": [a.to_dict() for a in self._architects],
                "materials": [m.to_dict() for m in self._materials],
                "projects": [p.to_dict() for p in self._projects]}
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self):
        if not os.path.exists(self._path):
            return
        with open(self._path, encoding="utf-8") as f:
            data = json.load(f)
        self._architects = [Architect.from_dict(d) for d in data.get("architects", [])]
        self._materials = [Material.from_dict(d) for d in data.get("materials", [])]
        self._projects = [Project.from_dict(d) for d in data.get("projects", [])]

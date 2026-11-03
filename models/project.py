import uuid
from .phase import Phase


class MaterialUsage:
    """مصرف یک ماده در یک پروژه (رابطه چند‌به‌چند)"""

    def __init__(self, material_id, quantity):
        self._material_id = material_id
        self.quantity = quantity

    @property
    def material_id(self):
        return self._material_id

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError("مقدار باید عدد باشد.")
        if value <= 0:
            raise ValueError("مقدار باید بزرگ‌تر از صفر باشد.")
        self._quantity = value

    def to_dict(self):
        return {"material_id": self.material_id, "quantity": self.quantity}

    @classmethod
    def from_dict(cls, d):
        return cls(d["material_id"], d["quantity"])


class Project:
    """پروژه معماری: یک معمار، چند فاز، چند مصالح"""

    def __init__(self, name, architect_id, budget, phases=None, usages=None, id=None):
        self._id = id or uuid.uuid4().hex[:8]
        self.name = name
        self.architect_id = architect_id
        self.budget = budget
        self._phases = list(phases or [])
        self._usages = list(usages or [])

    # ---- getters / setters ----
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        value = str(value).strip()
        if not value:
            raise ValueError("نام پروژه نمی‌تواند خالی باشد.")
        self._name = value

    @property
    def architect_id(self):
        return self._architect_id

    @architect_id.setter
    def architect_id(self, value):
        if not value:
            raise ValueError("برای پروژه باید یک معمار انتخاب شود.")
        self._architect_id = value

    @property
    def budget(self):
        return self._budget

    @budget.setter
    def budget(self, value):
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError("بودجه باید عدد باشد.")
        if value < 0:
            raise ValueError("بودجه نمی‌تواند منفی باشد.")
        self._budget = value

    @property
    def phases(self):
        return self._phases

    @property
    def usages(self):
        return self._usages

    @property
    def average_progress(self):
        if not self._phases:
            return 0.0
        return sum(p.progress for p in self._phases) / len(self._phases)

    # ---- phases ----
    def add_phase(self, name, progress=0):
        self._phases.append(Phase(name, progress))

    def remove_phase(self, index):
        del self._phases[index]

    # ---- materials ----
    def get_usage(self, material_id):
        return next((u for u in self._usages if u.material_id == material_id), None)

    def set_material(self, material_id, quantity):
        """افزودن ماده یا به‌روزرسانی مقدار آن"""
        usage = self.get_usage(material_id)
        if usage:
            usage.quantity = quantity
        else:
            self._usages.append(MaterialUsage(material_id, quantity))

    def remove_material(self, material_id):
        self._usages = [u for u in self._usages if u.material_id != material_id]

    # ---- serialization ----
    def to_dict(self):
        return {"id": self.id, "name": self.name,
                "architect_id": self.architect_id, "budget": self.budget,
                "phases": [p.to_dict() for p in self._phases],
                "usages": [u.to_dict() for u in self._usages]}

    @classmethod
    def from_dict(cls, d):
        return cls(d["name"], d["architect_id"], d["budget"],
                   [Phase.from_dict(p) for p in d.get("phases", [])],
                   [MaterialUsage.from_dict(u) for u in d.get("usages", [])],
                   d["id"])

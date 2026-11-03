import uuid


class Material:
    """مصالح (قابل استفاده در هر تعداد پروژه)"""

    def __init__(self, name, unit, unit_price, id=None):
        self._id = id or uuid.uuid4().hex[:8]
        self.name = name
        self.unit = unit
        self.unit_price = unit_price

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
            raise ValueError("نام مصالح نمی‌تواند خالی باشد.")
        self._name = value

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        value = str(value).strip()
        if not value:
            raise ValueError("واحد مصالح نمی‌تواند خالی باشد.")
        self._unit = value

    @property
    def unit_price(self):
        return self._unit_price

    @unit_price.setter
    def unit_price(self, value):
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError("قیمت واحد باید عدد باشد.")
        if value < 0:
            raise ValueError("قیمت واحد نمی‌تواند منفی باشد.")
        self._unit_price = value

    def to_dict(self):
        return {"id": self.id, "name": self.name,
                "unit": self.unit, "unit_price": self.unit_price}

    @classmethod
    def from_dict(cls, d):
        return cls(d["name"], d["unit"], d["unit_price"], d["id"])

    def __str__(self):
        return f"{self.name} ({self.unit})"

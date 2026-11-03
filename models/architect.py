import uuid


class Architect:
    """معمار"""

    def __init__(self, name, specialty="", phone="", id=None):
        self._id = id or uuid.uuid4().hex[:8]
        self.name = name
        self.specialty = specialty
        self.phone = phone

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
            raise ValueError("نام معمار نمی‌تواند خالی باشد.")
        self._name = value

    @property
    def specialty(self):
        return self._specialty

    @specialty.setter
    def specialty(self, value):
        self._specialty = str(value).strip()

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = str(value).strip()

    # ---- serialization ----
    def to_dict(self):
        return {"id": self.id, "name": self.name,
                "specialty": self.specialty, "phone": self.phone}

    @classmethod
    def from_dict(cls, d):
        return cls(d["name"], d.get("specialty", ""), d.get("phone", ""), d["id"])

    def __str__(self):
        return self.name

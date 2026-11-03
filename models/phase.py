class Phase:
    """فاز پروژه همراه با درصد پیشرفت"""

    def __init__(self, name, progress=0):
        self.name = name
        self.progress = progress

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        value = str(value).strip()
        if not value:
            raise ValueError("نام فاز نمی‌تواند خالی باشد.")
        self._name = value

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError("پیشرفت باید عدد باشد.")
        if not 0 <= value <= 100:
            raise ValueError("پیشرفت باید بین ۰ تا ۱۰۰ باشد.")
        self._progress = value

    def to_dict(self):
        return {"name": self.name, "progress": self.progress}

    @classmethod
    def from_dict(cls, d):
        return cls(d["name"], d.get("progress", 0))

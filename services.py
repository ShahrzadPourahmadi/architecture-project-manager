class ReportService:
    """محاسبه هزینه مصالح، گزارش بودجه و میانگین پیشرفت"""

    def __init__(self, store):
        self._store = store

    def material_lines(self, project):
        """لیست (ماده، مقدار، قیمت کل) برای یک پروژه"""
        lines = []
        for u in project.usages:
            m = self._store.get_material(u.material_id)
            if m:
                lines.append((m, u.quantity, m.unit_price * u.quantity))
        return lines

    def material_cost(self, project):
        return sum(total for _, _, total in self.material_lines(project))

    def budget_report(self, project):
        cost = self.material_cost(project)
        remaining = project.budget - cost
        percent = (cost / project.budget * 100) if project.budget else 0.0
        return {"budget": project.budget, "cost": cost,
                "remaining": remaining, "percent_used": percent,
                "over_budget": remaining < 0}

    def architect_summary(self, architect):
        projects = self._store.projects_of(architect.id)
        avg = (sum(p.average_progress for p in projects) / len(projects)) if projects else 0.0
        return {"projects": len(projects),
                "budget": sum(p.budget for p in projects),
                "cost": sum(self.material_cost(p) for p in projects),
                "avg_progress": avg}

    def overall_average_progress(self):
        ps = self._store.projects
        return sum(p.average_progress for p in ps) / len(ps) if ps else 0.0

from datlich.models import Department

class DepartmentService:
    def get_all_departments(self):
        return Department.objects.all()

    def get_department_by_id(self, department_id):
        try:
            return Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            return None

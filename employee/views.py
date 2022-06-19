from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render
from .models import Employee
# Create your views here.


@staff_member_required
def employee_work_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    total = 0
    for i in employee.employeework_set.all():
        total += i.qty * i.fees
    return render(
        request, 
        "admin/employee/employee/detail.html",
        {"employee" : employee, "total" : total}
    )
from django.urls import path
from . import views

app_name = "employee"

urlpatterns = [
    path("admin/employee/<int:employee_id>/", views.employee_work_detail, name="employee_work_detail")
]
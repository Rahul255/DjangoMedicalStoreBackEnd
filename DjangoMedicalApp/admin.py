from django.contrib import admin
from DjangoMedicalApp.models import Company,Medicine,MedicalDetails,Employee,Customer,Bill,EmployeeSalary,EmployeeBank,BillDetails,CustomerRequest
from DjangoMedicalApp.models import CompanyAccount,CompanyBank

# Register your models here.
admin.site.register(Company)
admin.site.register(Medicine)
admin.site.register(MedicalDetails)
admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Bill)
admin.site.register(EmployeeSalary)
admin.site.register(EmployeeBank)
admin.site.register(BillDetails)
admin.site.register(CustomerRequest)
admin.site.register(CompanyAccount)
admin.site.register(CompanyBank)


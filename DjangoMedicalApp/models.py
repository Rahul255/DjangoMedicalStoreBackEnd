from django.db import models

# Create your models here.

class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    licence_no = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    added_on = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Medicine(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    medical_typ = models.CharField(max_length=255)
    buy_price = models.CharField(max_length=255)
    sell_price = models.CharField(max_length=255)
    c_gst = models.CharField(max_length=255)
    s_gst = models.CharField(max_length=255)
    batch_no = models.CharField(max_length=255)
    shelf_no = models.CharField(max_length=255)
    expire_date = models.DateField()
    mfg_date = models.DateField()
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    in_stock_total = models.IntegerField()
    qty_in_strip = models.IntegerField()
    added_on = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class MedicalDetails(models.Model):
    id = models.AutoField(primary_key=True)
    medicine_id = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    salt_name = models.CharField(max_length=200)
    salt_qty = models.CharField(max_length=200)
    salt_qty_type = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    added_on = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    joinig_date = models.DateField()
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    added_on = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    added_on = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Bill(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class EmployeeSalary(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employee,on_delete=models.CASCADE)
    salary_date = models.DateField()
    salary_amount = models.CharField(max_length=200)
    added_on = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class BillDetails(models.Model):
    id = models.AutoField(primary_key=True)
    bill_id = models.ForeignKey(Bill,on_delete=models.CASCADE)
    medicine_id = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    qty = models.IntegerField()
    added_on = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class CustomerRequest(models.Model):
    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    medicine_details = models.CharField(max_length=200)
    customer_name = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class CompanyAccount(models.Model):
    choices = ((1, 'Debit'),(2, 'Credit'),)
    id = models.AutoField(primary_key=True)
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE)
    transaction_type = models.CharField(choices=choices,max_length=200)
    transaction_amt = models.CharField(max_length=200)
    transaction_date = models.DateField()
    payment_mode = models.CharField(max_length=200)
    added_on = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class CompanyBank(models.Model):
    id = models.AutoField(primary_key=True)
    bank_account_no = models.CharField(max_length=200)
    ifsc_no = models.CharField(max_length=200)
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class EmployeeBank(models.Model):
    id = models.AutoField(primary_key=True)
    bank_account_no = models.CharField(max_length=200)
    ifsc_no = models.CharField(max_length=200)
    employee_id = models.ForeignKey(Employee,on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from DjangoMedicalApp.models import Company,CompanyBank, Medicine, MedicalDetails, CompanyAccount, Employee
from DjangoMedicalApp.models import EmployeeBank, EmployeeSalary, CustomerRequest, Bill, BillDetails

from DjangoMedicalApp.serializers import CompanySerializer,CompanyBankSerializer,MedicineSerializer
from DjangoMedicalApp.serializers import MedicalDetailsSerializer, CompanyAccountSerializer, EmployeeSerializer
from DjangoMedicalApp.serializers import EmployeeBankSerializer, EmployeeSalarySerializer, CustomerSerializer, BillSerializer, BillDetailsSerializer
from DjangoMedicalApp.serializers import CustomerRequestSerializer,MedicalDetailsSerializerSimple



# Create your views here.
# company view 
class ComapnyViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # list,create,update company data
    def list(self,request):
        company = Company.objects.all()
        serializer = CompanySerializer(company,many=True,context={"request":request})
        response_dict= {"error":False,"message":"All Company List Data","data":serializer.data}
        return Response(response_dict)
    def create(self,request):
        try:
            serializer = CompanySerializer(data = request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_dict= {"error":False,"message":"Company data save successfully"}
        except:
            response_dict= {"error":True,"message":"Error during saving company data"}
        return Response(response_dict)

    def retrieve(self, request, pk=None):
        queryset = Company.objects.all()
        company = get_object_or_404(queryset, pk=pk)
        serializer = CompanySerializer(company, context={"request": request})

        serializer_data = serializer.data
        # Accessing All the Medicine Details of Current Medicine ID
        company_bank_details = CompanyBank.objects.filter(company_id=serializer_data["id"])
        companybank_details_serializers = CompanyBankSerializer(company_bank_details, many=True)
        serializer_data["company_bank"] = companybank_details_serializers.data

        return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})

    def update(self,request,pk=None):
        try:
            queryset =  Company.objects.all()
            company = get_object_or_404(queryset,pk=pk)
            serializer = CompanySerializer(company,data = request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_dict= {"error":True,"message":"Successfully updated company data"}
        except:
            response_dict= {"error":True,"message":"Error during updating company data"}

        return Response(response_dict)

#companybank 
class CompanyBankViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self,request):
        try:
            serializer = CompanyBankSerializer(data = request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_dict= {"error":False,"message":"Company bank data save successfully"}
        except:
            response_dict= {"error":True,"message":"Error during saving company bank data"}
        return Response(response_dict)

    def list(self,request):
        companybank = CompanyBank.objects.all()
        serializer = CompanyBankSerializer(companybank,many=True,context={"request":request})
        response_dict= {"error":False,"message":"All Company Bank List Data","data":serializer.data}
        return Response(response_dict)

    def retrieve(self,request,pk=None):
        queryset = CompanyBank.objects.all()
        companybank = get_object_or_404(queryset,pk=pk)
        serializer = CompanyBankSerializer(companybank, context={"request":request})
        return Response({"error":False,"message":"Single Data Fetch","data":serializer.data})

    def update(self,request,pk=None):
        try:
            queryset =  CompanyBank.objects.all()
            companybank = get_object_or_404(queryset,pk=pk)
            serializer = CompanyBankSerializer(companybank,data = request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_dict= {"error":True,"message":"Successfully updated company bank data"}
        except:
            response_dict= {"error":True,"message":"Error during updating company bank data"}

        return Response(response_dict)
#Company name custom view set
class CompanyNameViewSet(generics.ListAPIView):
    serializer_class = CompanySerializer

    def get_queryset(self):
        name = self.kwargs["name"]
        return Company.objects.filter(name=name)
#custom company only view set 
class CompanyOnlyViewSet(generics.ListAPIView):
    serializer_class = CompanySerializer

    def get_queryset(self):
        return Company.objects.all()

class MedicineViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self,request):
        try:
            serializer=MedicineSerliazer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            medicine_id=serializer.data['id']
            #Access The Serializer Id Which JUSt SAVE in OUR DATABASE TABLE
            #print(medicine_id)

            #Adding and Saving Id into Medicine Details Table
            medicine_details_list=[]
            for medicine_detail in request.data["medicine_details"]:
                print(medicine_detail)
                #Adding medicine id which will work for medicine details serializer
                medicine_detail["medicine_id"]=medicine_id
                medicine_details_list.append(medicine_detail)
                print(medicine_detail)

            serializer2=MedicalDetailsSerializer(data=medicine_details_list,many=True,context={"request":request})
            serializer2.is_valid()
            serializer2.save()

            dict_response={"error":False,"message":"Medicine Data Save Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Saving Medicine Data"}
        return Response(dict_response)

    def list(self,request):
        medicine = Medicine.objects.all()
        serializer = MedicineSerializer(medicine,many=True,context={"request":request})

        medicine_data = serializer.data
        newmedicinelist =[]
         #Adding Extra Key for Medicine Details in Medicine
        for medicine in medicine_data:
            #Accessing All the Medicine Details of Current Medicine ID
            medicine_details = MedicalDetails.objects.filter(medicine_id=medicine["id"])
            medicine_details_serializers=MedicalDetailsSerializerSimple(medicine_details,many=True)
            medicine["medicine_details"]=medicine_details_serializers.data
            newmedicinelist.append(medicine)


        response_dict= {"error":False,"message":"All Medicine List Data","data":newmedicinelist}
        return Response(response_dict)

    def retrieve(self,request,pk=None):
        queryset = Medicine.objects.all()
        medicine = get_object_or_404(queryset,pk=pk)
        serializer = MedicineSerializer(medicine, context={"request":request})

        serializer_data=serializer.data
        # Accessing All the Medicine Details of Current Medicine ID
        medicine_details = MedicalDetails.objects.filter(medicine_id=serializer_data["id"])
        medicine_details_serializers = MedicalDetailsSerializerSimple(medicine_details, many=True)
        serializer_data["medicine_details"] = medicine_details_serializers.data


        return Response({"error":False,"message":"Single Data Fetch","data":serializer.data})

    def update(self,request,pk=None):
            queryset =  Medicine.objects.all()
            medicine = get_object_or_404(queryset,pk=pk)
            serializer = MedicineSerializer(medicine,data = request.data,context={"request":request})
            serializer.is_valid()
            serializer.save()
            #print(request.data["medicine_details"])
            for salt_detail in request.data["medicine_details"]:
                if salt_detail["id"] == 0:
                    #for insert new salt details
                    del salt_detail["id"]
                    salt_detail["medicine_id"] = serializer.data["id"]
                    serializer2=MedicalDetailsSerializer(data=salt_detail,context={"request":request})
                    serializer2.is_valid()
                    serializer2.save()
                else:
                    #for update salt details
                    queryset2 = MedicalDetails.objects.all()
                    medicine_salt = get_object_or_404(queryset2,pk=salt_detail["id"])
                    del salt_detail["id"]
                    serializer3=MedicalDetailsSerializer(medicine_salt,data=salt_detail,context={"request":request})
                    serializer3.is_valid()
                    serializer3.save()
            return Response({"error":False,"message":"Data has been upddated"})


#company account view set
class CompanyAccountViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self,request):
        try:
            serializer = CompanyAccountSerializer(data = request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_dict= {"error":False,"message":"Company account data save successfully"}
        except:
            response_dict= {"error":True,"message":"Error during saving company account data"}
        return Response(response_dict)

    def list(self,request):
        companyaccount = CompanyAccount.objects.all()
        serializer = CompanyAccountSerializer(companyaccount,many=True,context={"request":request})
        response_dict= {"error":False,"message":"All Company Account List Data","data":serializer.data}
        return Response(response_dict)

    def retrieve(self,request,pk=None):
        queryset = CompanyAccount.objects.all()
        companyaccount = get_object_or_404(queryset,pk=pk)
        serializer = CompanyAccountSerializer(companyaccount, context={"request":request})
        return Response({"error":False,"message":"Single Data Fetch","data":serializer.data})

    def update(self,request,pk=None):
            queryset =  CompanyAccount.objects.all()
            companyaccount = get_object_or_404(queryset,pk=pk)
            serializer = CompanyAccountSerializer(companyaccount,data = request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"error":False,"message":"Data has been upddated"})

#employee view set
class EmployeeViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self,request):
        try:
            serializer = EmployeeSerializer(data = request.data,context={"request":request})
            serializer.is_valid()
            serializer.save()
            response_dict= {"error":False,"message":"Employee data save successfully"}
        except:
            response_dict= {"error":True,"message":"Error during saving employee data"}
        return Response(response_dict)

    def list(self,request):
        employee = Employee.objects.all()
        serializer = EmployeeSerializer(employee,many=True,context={"request":request})
        response_dict= {"error":False,"message":"All Employee List Data","data":serializer.data}
        return Response(response_dict)

    def retrieve(self,request,pk=None):
        queryset = Employee.objects.all()
        employee = get_object_or_404(queryset,pk=pk)
        serializer = EmployeeSerializer(employee, context={"request":request})
        return Response({"error":False,"message":"Single Data Fetch","data":serializer.data})

    def update(self,request,pk=None):
            queryset =  Employee.objects.all()
            employee = get_object_or_404(queryset,pk=pk)
            serializer = EmployeeSerializer(employee,data = request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"error":False,"message":"Data has been upddated"})

#employee bank view set
class EmployeeBankViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self,request):
        try:
            serializer = EmployeeBankSerializer(data = request.data,context={"request":request})
            serializer.is_valid()
            serializer.save()
            response_dict= {"error":False,"message":"Employee bank data save successfully"}
        except:
            response_dict= {"error":True,"message":"Error during saving employee bank data"}
        return Response(response_dict)

    def list(self,request):
        employee = EmployeeBank.objects.all()
        serializer = EmployeeBankSerializer(employee,many=True,context={"request":request})
        response_dict= {"error":False,"message":"All Employee Bank List Data","data":serializer.data}
        return Response(response_dict)

    def retrieve(self,request,pk=None):
        queryset = Employee.objects.all()
        employeebank = get_object_or_404(queryset,pk=pk)
        serializer = EmployeeBankSerializer(employeebank, context={"request":request})
        return Response({"error":False,"message":"Single Data Fetch","data":serializer.data})

    def update(self,request,pk=None):
            queryset =  EmployeeBank.objects.all()
            employeebank = get_object_or_404(queryset,pk=pk)
            serializer = EmployeeBankSerializer(employeebank,data = request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"error":False,"message":"Data has been upddated"})

#company employee salaryview set
class EmployeeSalaryViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self,request):
        try:
            serializer = EmployeeSalarySerializer(data = request.data,context={"request":request})
            serializer.is_valid()
            serializer.save()
            response_dict= {"error":False,"message":"Employee salary save successfully"}
        except:
            response_dict= {"error":True,"message":"Error during saving employee salary"}
        return Response(response_dict)

    def list(self,request):
        employeesalary = EmployeeSalary.objects.all()
        serializer = EmployeeSalarySerializer(employeesalary,many=True,context={"request":request})
        response_dict= {"error":False,"message":"All Employee Salary List Data","data":serializer.data}
        return Response(response_dict)

    def retrieve(self,request,pk=None):
        queryset = EmployeeBank.objects.all()
        employeesalary = get_object_or_404(queryset,pk=pk)
        serializer = EmployeeSalarySerializer(employeesalary, context={"request":request})
        return Response({"error":False,"message":"Single Data Fetch","data":serializer.data})

    def update(self,request,pk=None):
            queryset =  EmployeeSalary.objects.all()
            employeesalary = get_object_or_404(queryset,pk=pk)
            serializer = EmployeeSalarySerializer(employeesalary,data = request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"error":False,"message":"Data has been upddated"})

#custom view set for accessing the data of salary and employee bank account using employee id
class EmployeeSalaryByEIDViewSet(generics.ListAPIView):
    serializer_class = EmployeeSalarySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        employee_id=self.kwargs["employee_id"]
        return EmployeeSalary.objects.filter(employee_id=employee_id)

class EmployeeBankByEIDViewSet(generics.ListAPIView):
    serializer_class = EmployeeBankSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        employee_id = self.kwargs["employee_id"]
        return EmployeeBank.objects.filter(employee_id=employee_id)

#medicine view set
class MedicineByNameViewSet(generics.ListAPIView):
    serializer_class = MedicineSerializer

    def get_queryset(self):
        name = self.kwargs["name"]
        return Medicine.objects.filter(name__contains=name)


class GenerateBillViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        #try:
            #First #Save Customer Data
        serializer = CustomerSerializer(data=request.data, context={"request": request})
        serializer.is_valid()
        serializer.save()

        customer_id = serializer.data['id']

        #Save Bill Data
        billdata={}
        billdata["customer_id"]=customer_id

        serializer2 = BillSerializer(data=billdata, context={"request": request})
        serializer2.is_valid()
        serializer2.save()
        bill_id = serializer2.data['id']

        # Adding and Saving Id into Medicine Details Table
        medicine_details_list = []
        for medicine_detail in request.data["medicine_details"]:
            print(medicine_detail)
            medicine_detail1={}
            medicine_detail1["medicine_id"] = medicine_detail["id"]
            medicine_detail1["bill_id"] = bill_id
            medicine_detail1["qty"] = medicine_detail["qty"]

            medicine_details_list.append(medicine_detail1)
            #print(medicine_detail)

        serializer3 = BillDetailsSerializer(data=medicine_details_list, many=True,
                                               context={"request": request})
        serializer3.is_valid()
        serializer3.save()

        dict_response = {"error": False, "message": "Bill Generate Successfully"}
        #except:
            #dict_response = {"error": True, "message": "Error During Generating BIll"}
        return Response(dict_response)

class CustomerRequestViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # list,create,update company data
    def list(self,request):
        customer_request = CustomerRequest.objects.all()
        serializer = CustomerRequestSerializer(customer_request,many=True,context={"request":request})
        response_dict= {"error":False,"message":"All Customer Request Data","data":serializer.data}
        return Response(response_dict)
    def create(self,request):
        try:
            serializer = CustomerRequestSerializer(data = request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_dict= {"error":False,"message":"Customer Request data save successfully"}
        except:
            response_dict= {"error":True,"message":"Error during saving Customer Request data"}
        return Response(response_dict)

    def retrieve(self, request, pk=None):
        queryset = CustomerRequest.objects.all()
        customer_request = get_object_or_404(queryset, pk=pk)
        serializer = CustomerRequestSerializer(customer_request, context={"request": request})

        serializer_data = serializer.data
        # Accessing All the Medicine Details of Current Medicine ID
        

        return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})

    def update(self,request,pk=None):
        try:
            queryset =  CustomerRequest.objects.all()
            customer_request = get_object_or_404(queryset,pk=pk)
            serializer = CustomerRequestSerializer(customer_request,data = request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_dict= {"error":True,"message":"Successfully updated customer data"}
        except:
            response_dict= {"error":True,"message":"Error during updating customer data"}

        return Response(response_dict)


    
company_list = ComapnyViewSet.as_view({"get":"list"})
company_create = ComapnyViewSet.as_view({"post":"create"})
company_update = ComapnyViewSet.as_view({"put":"update"})
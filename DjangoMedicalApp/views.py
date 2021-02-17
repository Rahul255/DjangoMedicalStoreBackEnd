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
#Company name
class CompanyNameViewSet(generics.ListAPIView):
    serializer_class = CompanySerializer

    def get_queryset(self):
        name = self.kwargs["name"]
        return Company.objects.filter(name=name)

class MedicineViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self,request):
        try:
            serializer = MedicineSerializer(data = request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            medicine_id = serializer.data['id']
            #adding and saving id into medicine table
            medicine_details_list = []
            for medicine_details in request.data["medicine_details"]:
                print(medicine_detail)
                #Adding medicine id which will work for medicine details serializer
                medicine_detail["medicine_id"]=medicine_id
                medicine_details_list.append(medicine_detail)
                print(medicine_detail)

            serializer2 = MedicalDetailsSerializer(data=medicine_details_list,many=True,context={"request":request})
            serializer2.is_valid()
            serializer2.save()

            response_dict= {"error":False,"message":"Medicine data save successfully"}
        except:
            response_dict= {"error":True,"message":"Error during saving Medicine data"}
        return Response(response_dict)

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
        try:
            queryset =  Medicine.objects.all()
            medicine = get_object_or_404(queryset,pk=pk)
            serializer = MedicineSerializer(medicine,data = request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_dict= {"error":True,"message":"Successfully updated medicine data"}
        except:
            response_dict= {"error":True,"message":"Error during updating medicine data"}

        return Response(response_dict)
    
company_list = ComapnyViewSet.as_view({"get":"list"})
company_create = ComapnyViewSet.as_view({"post":"create"})
company_update = ComapnyViewSet.as_view({"put":"update"})
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from DjangoMedicalApp.models import Company
from DjangoMedicalApp.serializers import ComapnySerializer


# Create your views here.
class ComapnyViewSet(viewsets.ViewSet):
    
    def list(self,request):
        company = Company.objects.all()
        serializer = ComapnySerializer(company,many=True,context={"request":request})
        response_dict= {"error":False,"message":"All Company List Data","data":serializer.data}
        return Response(response_dict)
    
company_list = ComapnyViewSet.as_view({"get":"list"})
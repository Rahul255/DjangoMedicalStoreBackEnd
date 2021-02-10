from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from rest_framework.response import Response
from DjangoMedicalApp.models import Company
from DjangoMedicalApp.serializers import ComapnySerializer


# Create your views here.
# company view 
class ComapnyViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # list,create,update company data
    def list(self,request):
        company = Company.objects.all()
        serializer = ComapnySerializer(company,many=True,context={"request":request})
        response_dict= {"error":False,"message":"All Company List Data","data":serializer.data}
        return Response(response_dict)
    def create(self,request):
        try:
            serializer = ComapnySerializer(data = request.data,context={"request":request})
            serializer.is_valid()
            serializer.save()
            response_dict= {"error":False,"message":"Company data save successfully"}
        except:
            response_dict= {"error":True,"message":"Error during saving company data"}
        return Response(response_dict)

    def update(self,request,pk=None):
        try:
            queryset =  Company.objects.all()
            company = get_object_or_404(queryset,pk=pk)
            serializer = ComapnySerializer(company,data = request.data,context={"request":request})
            serializer.is_valid()
            serializer.save()
            response_dict= {"error":True,"message":"Successfully updated company data"}
        except:
            response_dict= {"error":True,"message":"Error during updating company data"}

        return Response(response_dict)

    
company_list = ComapnyViewSet.as_view({"get":"list"})
company_create = ComapnyViewSet.as_view({"post":"create"})
company_update = ComapnyViewSet.as_view({"put":"update"})
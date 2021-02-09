from rest_framework import serializers
from DjangoMedicalApp.models import Company


class ComapnySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ["name","licence_no","address","contact","email","description"]
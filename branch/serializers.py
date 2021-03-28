from rest_framework import serializers,fields
from .models import BranchProfile,Truck,Trip
class BranchProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchProfile
        fields =['name','id']

class TruckSerializer(serializers.ModelSerializer):
    branch = BranchProfileSerializer(read_only = True)
    class Meta:
        model = Truck
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    source      =  BranchProfileSerializer(read_only = True)
    destination = BranchProfileSerializer(read_only = True)
    truck       = TruckSerializer(read_only = True)
    class Meta:
        model = Trip
        exclude = ['id']
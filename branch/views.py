from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from .models import BranchProfile,Truck,Trip
from .serializers import BranchProfileSerializer,TruckSerializer,TripSerializer
from accounts.models import MyUser
class Branches_view(APIView):
    def get(self,request):
        if request.user.user_type == 'admin':
            branches = BranchProfile.objects.all()
            serializer = BranchProfileSerializer(branches,many=True)
            return Response(serializer.data)
        else:
            return Response({'message':'Dont have permission'})
    def post(self,request):
        user_obj = MyUser.objects.create(email=request.data['email'],user_type="employee")
        user_obj.set_password(request.data['password'])
        user_obj.save()
        branch_obj = BranchProfile.objects.create(user = user_obj , name= request.data['name'])
        branch_obj.save()
        return Response({'message':'created Succesfully'})
 
class Branch_detailView(APIView):
    def delete(self,request,pk):
        branch_obj = BranchProfile.objects.get(id=pk)
        branch_obj.delete()
        return Response({'message':'Removed Succesfully'})

class Truck_view(APIView):
    def get(self,request):
        if request.user.user_type == 'admin':
            branches = Truck.objects.all()
            serializer = TruckSerializer(branches,many=True)
            return Response(serializer.data)
        else:
            return Response({'message':'Dont have permission'})
    def post(self,request):
        branch_obj = BranchProfile.objects.get(id=request.data['id'])
        truck_obj = Truck.objects.create(branch = branch_obj , name = request.data['name'],in_use=False)
        truck_obj.save()
        return Response({'message':'created Succesfully'})
 
class Truck_detailView(APIView):
    def delete(self,request,pk):
        truck_obj = Truck.objects.get(id=pk)
        truck_obj.delete()
        return Response({'message':'Removed Succesfully'})

class branch_trucks(APIView):
    def get(self,request):
        branch_obj = request.user.profile
        trucks = branch_obj.trucks.all()
        serializer = TruckSerializer(trucks,many=True)
        return Response(serializer.data)

class OtherBranches(APIView):
    def get(self,request):
        branch_obj = request.user.profile
        other_branches = BranchProfile.objects.exclude(id = branch_obj.id)
        serializer = BranchProfileSerializer(other_branches,many=True)
        return Response(serializer.data)

class BranchWork(APIView):
    def post(self,request):
        source_obj = request.user.profile
        destination_obj = BranchProfile.objects.get(id = request.data['id'])
        weight = int(request.data['weight'])
        trips = Trip.objects.filter(source = source_obj).filter(destination = destination_obj).filter(status = "Pending")
        if(trips):
            trip = trips[0]
            if (weight + trip.space > 500):
                return Response({'message':'Weight is more than 500kg...Add '+str(500 - trip.space)+ "kg Now..."+str(weight-(500 - trip.space))+"kg Next Time"})
            elif (weight + trip.space == 500):
                trip.status = "Completed"
                trip.space = trip.space + weight
                trip.save()
                truck = trip.truck
                truck.in_use = False
                truck.save()
                return Response({'message':'Your Items Shipped take'+str(weight*10)+' rupess... and Truck is moving..','id':trip.id})
            else:
                trip.space = trip.space + weight
                trip.save()
                return Response({'message':'Your Items Shipped ...take '+str(weight*10)+' rupess..'+str(500 - (trip.space))+'kg needed to start Truck...','id':trip.id})
        else:
            trucks = source_obj.trucks.all().filter(in_use = False )
            if(trucks):
                truck = trucks[0]
                truck.in_use = True
                truck.save()
                trip = Trip.objects.create(source = source_obj , destination = destination_obj,truck = truck,space=weight,status = "Pending")
                trip.save()
                return Response({'message':'Your Items Shipped ... '+str(500 - (trip.space))+'kg needed to start Truck...','id':trip.id})
            else:
                return Response({'message':'No Truck Available ..Ask Manager to Assign truck'})
        return Response({'message':'something Went Wrong'})
class TrackInfo(APIView):
    authentication_classes  = []
    permission_classes      = []
    def get(self,request,pk):
        trip_obj = Trip.objects.get(id = pk)
        serializer = TripSerializer(trip_obj)
        return Response(serializer.data)
class getTripsInfo(APIView):
    def get(self,request):
        branch_profile = request.user.profile
        trips = branch_profile.trips_from.all().order_by('-time')
        serializer = TripSerializer(trips,many=True)
        return Response(serializer.data)


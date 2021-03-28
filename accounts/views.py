from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
class getInfo(APIView):
    def get(self,request):
        user = request.user
        return Response({'user_type':user.user_type})

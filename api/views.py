from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from api.serializers import ReferralSerializer, UserSerializer, ProfileSerializer
from api.models import Profile,Referral
from api.utils import generate_random_string

from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
    
class UserRegistration(APIView):
    def post(self,request,*args, **kwargs):
        referral_code = request.data.get("referral_code",None)
        
        if referral_code :
            referrer = get_object_or_404(Profile,referral_code=referral_code)
           
            serl = UserSerializer(data=request.data)
            if serl.is_valid():
                serl.save()
                
                referrer.referral_count+=1
                referrer.save()
                
            else:
                return Response(serl.errors,status=status.HTTP_400_BAD_REQUEST)
            
            user = get_object_or_404(User,username=serl.data["username"])
            
            data = {
                "referrer" : referrer.id,
                "referred" : user.id,
                "refferal_code": referral_code
            }
            
            referral_serl = ReferralSerializer(data=data)
            if referral_serl.is_valid():
                referral_serl.save()
                
            else:
                user.delete()
                return Response(referral_serl.errors,status=status.HTTP_400_BAD_REQUEST)
            profile_data = {
                "user" : user.id,
                "referral_code" : generate_random_string(),                
            }
            profile_serializer = ProfileSerializer(data=profile_data)
            if profile_serializer.is_valid():
                profile_serializer.save()
                return Response({"Message": "Successfully Registered !", "user_id": serl.data["id"]},status=status.HTTP_201_CREATED)
            return Response(profile_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        else :
            serl = UserSerializer(data=request.data)
            if serl.is_valid():
                serl.save()
                # serl.data.pop("password")
                user = get_object_or_404(User,username=serl.data["username"])
                profile_data = {
                "user" : user.id,
                "referral_code" : generate_random_string(),                
                }
                profile_serializer = ProfileSerializer(data=profile_data)
                if profile_serializer.is_valid():
                    profile_serializer.save()
                    return Response({"Message": "Successfully Registered !", "user_id": serl.data["id"]},status=status.HTTP_201_CREATED)
                else :
                    return Response(profile_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            return Response(serl.errors,status=status.HTTP_400_BAD_REQUEST)
        

class UserDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request,*args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        data = {
            "username" : request.user.username,
            "email"   : request.user.email,
            "referral_code" : profile.referral_code,
            "created_at" : profile.created
        }
        return Response(data,status=status.HTTP_200_OK)

class ReferredUsers(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    
    def get(self,request,*args, **kwargs):
        data = Referral.objects.filter(referrer=request.user)
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(data, request)
        
        serl = ReferralSerializer(result_page, many=True)
        
        return paginator.get_paginated_response(serl.data)
    
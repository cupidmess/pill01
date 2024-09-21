from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from django.db.models import Subquery, OuterRef, Q 
from .serializers import UserRegisterSerializer, LoginSerializer,PasswordResetRequestSerializer, SetNewPasswordSerializer,LogoutUserSerializer, VerifyUserEmailSerializer,JobPostSerializer, DashboardSerializer, ExperienceSerializer,EducationSerializer,AddonsSerializer, MoreSerializer,FeedbackSerializer, BiddingSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from .utility import send_code_to_user
from .models import OneTimePassword, User, JobPost, Dashboard, Experience, Education, Addons, More, Bidding, Feedback
from rest_framework.permissions import IsAuthenticated , AllowAny
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import messages

class RegisterUserView(GenericAPIView):
    serializer_class=UserRegisterSerializer
    permission_classes = [AllowAny]
    def post(self,request):
        user_data=request.data
        serializer=self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user=serializer.data
            send_code_to_user(user['email'])
            return Response({'data':user, 'message':f"hi {user['name']} thanks for sigining up a passcode has been sent to verify your email"},status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyUserEmail(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyUserEmailSerializer
    def post(self,request):
        otpcode=request.data.get('otp')
        try:
            user_code_obj=OneTimePassword.objects.get(code=otpcode)
            user = user_code_obj.user
            if not user.is_verified:
                user.is_verified=True
                user.save()
                return Response({'message':'account email verified successfully'},status=status.HTTP_200_OK)
            return Response({'message':'code is invalid, user already verified'}, status=status.HTTP_204_NO_CONTENT)
          
        except OneTimePassword.DoesNotExist:
            return Response({'message':'invalid otp'},status=status.HTTP_404_NOT_FOUND)
        

class LoginUserView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class=LoginSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class PasswordResetRequestView(GenericAPIView):
    permission_classes = [AllowAny]

    serializer_class=PasswordResetRequestSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'message': "A link has been sent to your email to reset your password"},status=status.HTTP_200_OK)
    

class PasswordResetConfirm(GenericAPIView):
    permission_classes = [AllowAny]

    def get(self,request,uidb64,token):
        try:
            user_id=smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response({'message':'token is invalid or expired'},status=status.HTTP_401_UNAUTHORIZED)
            return Response({'message':"credentials are valid", 'success':True,'uidb64':uidb64,'token':token },status=status.HTTP_200_OK)  
        
        except DjangoUnicodeDecodeError as identifier:
            return Response ({'message':'token is invalid or expired'},status=status.HTTP_401_UNAUTHORIZED)
        

class SetNewPassword(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class=SetNewPasswordSerializer
    def patch(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'password reset successful'},status=status.HTTP_200_OK)



class LogoutUserView(GenericAPIView):
        serializer_class=LogoutUserSerializer  
        permission_classes=[IsAuthenticated]    
        def post(self,request) :
            serializer=self.serializer_class(data=request.data)  
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)


class JobPostCreateList (generics.ListCreateAPIView):
  permission_classes = [AllowAny]
  queryset= JobPost.objects.all().order_by('-created_at')
  serializer_class = JobPostSerializer
  def delete(self, request, *args, **kwargs):
    JobPost.objects.all().delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class JobPostRetrieveUpdateDestory(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    lookup_field = "pk"

class DashboardListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer
    def delete(self, request, *args, **kwargs):
        Dashboard.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Retrieve, Update, and Delete Views for Dashboard
class DashboardDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer
    lookup_field = "pk"   

class ExperienceListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    def delete(self, request, *args, **kwargs):
        Experience.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EducationListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    def delete(self, request, *args, **kwargs):
        Education.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)     

class MoreCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = More.objects.all()
    serializer_class = MoreSerializer
    def delete(self, request, *args, **kwargs):
        More.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)     

class AddonsDetailView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Addons.objects.all()
    serializer_class = AddonsSerializer
    def delete(self, request, *args, **kwargs):
        Addons.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
class FeedbackView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset= Feedback.objects.all()
    serializer_class = FeedbackSerializer
    def delete(self, request, *args, **kwargs):
       Feedback.objects.all().delete()
       return Response(status=status.HTTP_204_NO_CONTENT)
    
class BiddingView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset= Bidding.objects.all()
    serializer_class = BiddingSerializer
    def delete(self, request, *args, **kwargs):
       Bidding.objects.all().delete()
       return Response(status=status.HTTP_204_NO_CONTENT)










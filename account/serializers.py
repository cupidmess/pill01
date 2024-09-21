
from rest_framework import serializers
from .models import User, JobPost, Experience, Education, Addons, Dashboard, More, Feedback, Bidding
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, smart_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utility import send_email
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class VerifyUserEmailSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)

    class Meta:
        fields = ['otp']


class UserRegisterSerializer(serializers.ModelSerializer):
    password= serializers.CharField(max_length=68, min_length=6, write_only= True)
    password2=serializers.CharField(max_length=68, min_length=6, write_only= True)

    class Meta:
        model=User
        fields=['email','name','username','password','password2']

    def validate(self, attrs):
        password=attrs.get('password','')
        password2=attrs.get('password2','')
        if password != password2:
            raise serializers.ValidationError("Passwords did not match")
        return attrs   
    
    def create(self, validated_data):
        user=User.objects.create_user(
        email=validated_data['email'],
        name=validated_data.get('name'),
        username=validated_data.get('username'),
        password=validated_data.get('password')
        )
        return user
    
class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    password=serializers.CharField(max_length=68,write_only=True)
    name=serializers.CharField(max_length=255,read_only=True)
    username=serializers.CharField(max_length=255,read_only=True)
    access_token=serializers.CharField(max_length=255,read_only=True)
    refresh_token=serializers.CharField(max_length=255,read_only=True)

    class Meta:
        model=User
        fields=['email','password','name','username','access_token','refresh_token']


    def validate(self,attrs):
         email=attrs.get('email') 
         password=attrs.get('password')
         request=self.context.get('request')
         user=authenticate(request,email=email,password=password)
         if not user:
             raise AuthenticationFailed("invalid credentials try again")
         user_tokens=user.tokens()

         return {
             'email':user.email,
             'name': user.get_name,
             'username': user.get_username,
              'access_token':str(user_tokens.get('access')),
              'refresh_token':str(user_tokens.get('refresh'))
         }
    
class PasswordResetRequestSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)

    class Meta:
        fields=['email']

    def validate(self,attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            request=self.context.get('request')
            site_domain=get_current_site(request).domain
            relative_link=reverse('password-reset-confirm',kwargs={'uidb64':uidb64 , 'token':token})
            abslink=f"http://{site_domain}{relative_link}"
            email_body=f"Hi use the link below to reset your password:\n {abslink}"
            data={
                   'email_body':email_body,
                    'email_subject':"Reset your password",
                    'to_email':user.email
            }
            send_email(data)

        return super().validate(attrs)
        
    
class SetNewPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=100, min_length=6, write_only=True)
    confirm_password=serializers.CharField(max_length=100, min_length=6, write_only=True)
    uidb64=serializers.CharField(write_only=True)
    token=serializers.CharField(write_only=True)

    class Meta:
        fields=['password','confirm_password','uidb64','token']

    def validate(self,attrs):
        try: 
             token=attrs.get('token')
             uidb64=attrs.get('uidb64')
             password=attrs.get('password')
             confirm_password=attrs.get('confirm_password')
             user_id=force_str(urlsafe_base64_decode(uidb64))
             user=User.objects.get(id=user_id)
             if not PasswordResetTokenGenerator().check_token(user,token):
                 return AuthenticationFailed("reset link is invalid or has expired",401)
             
             if password!=confirm_password:
                 raise AuthenticationFailed("Password did not match")
             user.set_password(password) 
             user.save()
             return user
        except Exception as e:
            return AuthenticationFailed("link is invalid or expired")
        

class LogoutUserSerializer(serializers.Serializer):
    refresh_token=serializers.CharField()

    default_error_messages={
        'bad_token':('token is invalid or has expired')
    }

    def validate(self,attrs):
        self.token=attrs.get('refresh_token')
        return attrs
    
    def save(self,**kwargs):
        try:
          token=RefreshToken(self.token)
          token.blacklist()
        except TokenError:   
            return self.fail('bad_token') 

class JobPostSerializer (serializers.ModelSerializer):
  class Meta : 
    model = JobPost
    fields = ['user','name','job_title','experience','desc','link','skill_1','skill_2','skill_3','payment','created_at']

class ExperienceSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(input_formats=['%Y-%m-%d'])
    end_date = serializers.DateField(input_formats=['%Y-%m-%d'])
    class Meta:
        model = Experience
        fields = '__all__'

class EducationSerializer(serializers.ModelSerializer):
    education_start = serializers.DateField(input_formats=['%Y-%m-%d'])
    education_end = serializers.DateField(input_formats=['%Y-%m-%d'])
    class Meta:
        model = Education
        fields = '__all__'

class AddonsSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(input_formats=['%Y-%m-%d'])
    class Meta:
        model = Addons
        fields = '__all__'        

class DashboardSerializer(serializers.ModelSerializer):
    experiences = ExperienceSerializer(many=True, read_only=True)
    educations = EducationSerializer(many=True, read_only=True)
    addons = AddonsSerializer(read_only=True)

    class Meta:
        model = Dashboard
        fields = '__all__'
class MoreSerializer(serializers.ModelSerializer):
    class Meta: 
        model = More 
        fields = "__all__"

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
      model = Feedback
      fields = '__all__'

class BiddingSerializer(serializers.ModelSerializer):
    class Meta:
        model= Bidding
        fields= '__all__'     

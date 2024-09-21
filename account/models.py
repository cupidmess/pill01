from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .manager import UserManager
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.

class User(AbstractBaseUser,PermissionsMixin):
    id = models.BigAutoField(primary_key=True, editable=False) 
    email=models.EmailField(max_length=255, unique=True, verbose_name=_("Email Address"))
    name=models.CharField(max_length=255, verbose_name=_("Name"))
    username=models.CharField(max_length=100,unique=True, verbose_name=_("Username"))
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD="email"

    REQUIRED_FIELDS=["name","username"]

    objects=UserManager()

    def __str__(self):
        return (self.email)
    @property
    def get_name(self):
        return (self.name)
    @property
    def get_username(self): 
        return (self.username)
    
    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return {
            'refresh':str(refresh),
            'access':str(refresh.access_token)

        }
    
        

class OneTimePassword(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    code=models.CharField(max_length=6, unique=True)

    def __str__(self):
        return f"{self.user.name}-passcode"

class JobPost (models.Model):
  user=models.ForeignKey(User,related_name='jobpost',on_delete=models.CASCADE)
  name = models.CharField(_("name"), max_length=50)
  job_title = models.CharField(_("job_title"), max_length=100)
  experience = models.IntegerField(_("experience"))
  desc = models.CharField(_("desc"), max_length=500)
  link = models.URLField(_("link"), max_length=200)
  skill_1 = models.CharField(_("skill_1"), max_length=50)
  skill_2 = models.CharField(_("skill_2"), max_length=50)
  skill_3 = models.CharField(_("skill_3"), max_length=50)
  payment = models.IntegerField(_("payment"))
  created_at = models.DateTimeField(auto_now_add=True)
  def __str__ (self):
    return self.name
  
class Dashboard(models.Model):
    user=models.ForeignKey(User,related_name='dashboard',on_delete=models.CASCADE)
    skills_1 = models.CharField(_("skills_1"), max_length=50)
    skills_2 = models.CharField(_("skills_2"), max_length=50)
    skills_3 = models.CharField(_("skills_3"), max_length=50)
    skills_4 = models.CharField(_("skills_4"), max_length=50)
    skills_5 = models.CharField(_("skills_5"), max_length=50)


    def __str__(self):
        return self.skills_1

class Experience(models.Model):
    dashboard = models.ForeignKey(Dashboard, related_name='experiences', on_delete=models.CASCADE)
    experience_title = models.CharField(_("experience_title"), max_length=100)
    experience_company = models.CharField(_("experience_company"), max_length=100)
    location = models.CharField(_("location"), max_length=50)
    start_date = models.DateField(_("start_date"))
    end_date = models.DateField(_("end_date"))
    exp_description = models.TextField(_("exp_description"), null=True, blank=True)

    def __str__(self):
        return self.experience_title    
    
class Education(models.Model):
    dashboard = models.ForeignKey(Dashboard, related_name='educations', on_delete=models.CASCADE)
    education_type = models.CharField(_("education_type"), max_length=100)
    education_start = models.DateField(_("education_start"))
    education_end = models.DateField(_("education_end"))
    degree_type = models.CharField(_("degree_type"), max_length=100)
    education_score = models.IntegerField(_("education_score"))

    def __str__(self):
        return self.education_type

class More (models.Model):
    dashboard = models.ForeignKey(Dashboard, related_name='more', on_delete=models.CASCADE)
    title = models.CharField(_("title"), max_length=50)
    desc = models.CharField(_("desc"), max_length=250)
    def __str__(self):
        return self.title

class Addons(models.Model):
    dashboard = models.OneToOneField(Dashboard, related_name='addons', on_delete=models.CASCADE)
    dob = models.DateField(_("dob"))
    street_add = models.CharField(_("street_add"), max_length=255)
    pin = models.IntegerField(_("pin"))
    city = models.CharField(_("city"), max_length=50)

    def __str__(self):
        return self.city 

class Feedback(models.Model):
    user=models.ForeignKey(User,related_name='Feedback',on_delete=models.CASCADE)
    rating=models.IntegerField()
    description=models.CharField(max_length=500)

    def __str__(self):
      return self.rating 
    
class Bidding(models.Model):
    user=models.ForeignKey(User,related_name='Bidding',on_delete=models.CASCADE)
    payment_fee=models.IntegerField()
    proposal=models.CharField(max_length=500)
    duration=models.IntegerField()


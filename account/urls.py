from django.urls import path
from . import views
from .views import RegisterUserView, VerifyUserEmail,LoginUserView,PasswordResetConfirm,PasswordResetRequestView,SetNewPassword,JobPostCreateList,LogoutUserView,DashboardListCreateView,DashboardDetailView,ExperienceListCreateView,EducationListCreateView,AddonsDetailView, MoreCreateView, FeedbackView, BiddingView


urlpatterns = [
    
    path('signup/', RegisterUserView.as_view(), name='signup'),
    path('verify-email/',VerifyUserEmail.as_view(),name='verify'),
    path('login/',LoginUserView.as_view(), name='login'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>', PasswordResetConfirm.as_view(), name='password-reset-confirm'),
    path('set-new-password/', SetNewPassword.as_view(), name='set-new-password'),
    path('logout/',LogoutUserView.as_view(),name='logout'),
    path("jobposts/",views.JobPostCreateList.as_view(),name= 'job-create'),
    path('dashboard/', DashboardListCreateView.as_view(), name='dashboard-list-create'),
    path('dashboard/<int:pk>/', DashboardDetailView.as_view(), name='dashboard-detail'),
    path('experience/', ExperienceListCreateView.as_view(), name='experience-list-create'),
    path('education/', EducationListCreateView.as_view(), name='education-list-create'),
    path('addons/<int:pk>/', AddonsDetailView.as_view(), name='addons-detail'),
    path('more/',MoreCreateView.as_view(), name='more-details'),
    path('feedback/',FeedbackView.as_view(),name='feedback'),
    path('bidding/',BiddingView.as_view(),name='bidding'),
 

]

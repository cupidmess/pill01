

# Register your models here.
from django.contrib import admin
from .models import User, Dashboard, Experience, Education, Addons, More, Feedback, Bidding

class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1  # Number of empty experience fields to show by default in the admin

class EducationInline(admin.TabularInline):
    model = Education
    extra = 1  # Number of empty education fields to show by default in the admin

class AddonsInline(admin.StackedInline):
    model = Addons
    extra = 1 
    can_delete = False

class DashboardInLine(admin.StackedInline):
    model = Dashboard
    extra = 1 

class FeedbackInline(admin.StackedInline):
    model = Feedback
    extra = 1 

class BiddingInline(admin.StackedInline):
    model = Bidding
    extra = 1 
        

class DashboardAdmin(admin.ModelAdmin):
    inlines = [ExperienceInline, EducationInline, AddonsInline]

class UserAdmin(admin.ModelAdmin):
    inlines=[DashboardInLine,FeedbackInline,BiddingInline]

class MoreAdmin (admin.StackedInline):
    model = More
    extra = 1



# Register the models in admin
admin.site.register(Dashboard, DashboardAdmin)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Addons)
admin.site.register(User,UserAdmin)



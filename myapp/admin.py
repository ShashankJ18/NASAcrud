from django.contrib import admin

from .models import Userdata, discussion_forum,Category,Object,Quiz

from django.db import models
from django.forms import ModelChoiceField

class showUser(admin.ModelAdmin):
   list_display = ['name','email','username','profile_picture','is_admin']

admin.site.register(Userdata, showUser)

class showdiscussion(admin.ModelAdmin):
    list_display = ['discussion_title','content','parent','user_id','created_at','upvote','downvote','category']

admin.site.register(discussion_forum, showdiscussion)

class showcategory(admin.ModelAdmin):
    list_display = ['name','description']

admin.site.register(Category,showcategory)

@admin.register(Object)
class SolarObjectAdmin(admin.ModelAdmin):
    list_display = ('name','obj_type')  # Fields you want to display in the admin panel

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('q_question', 'q_answer')  # Correct field names for display



from django.db import models

from django.utils.safestring import mark_safe
from django.core.validators import MaxValueValidator


class Userdata(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    password= models.CharField(max_length=10)
    is_admin = models.BooleanField(default=False)


    def profile_p(self):
               return mark_safe('<img src="{}" width="100"/>'.format(self.profile_picture.url))


    profile_p.allow_tags = True

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class discussion_forum(models.Model):
    discussion_title= models.CharField(max_length=100)
    content=models.TextField()

    user_id = models.ForeignKey('Userdata', on_delete=models.CASCADE, related_name='discussion')
    created_at=models.DateTimeField(auto_now_add=True)
    upvote=models.IntegerField()
    downvote=models.IntegerField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='discussions')  # New field for category

    def __str__(self):
        return f"{self.discussion_title} - {self.content[:50]}"  # Returns title and first 50 characters of content


class Object(models.Model):
    obj_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    obj_type = models.CharField(max_length=50)  # e.g., planet, asteroid, etc.

    def __str__(self):
        return self.name  # This is fine, as 'name' exists in this model.


class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key=True)
    q_question = models.CharField(max_length=255)  # The quiz question
    q_answer = models.CharField(max_length=100)
    option_1 = models.CharField(max_length=255, default='Default option')
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)  # Store options as JSON
    obj_id = models.ForeignKey(Object, on_delete=models.CASCADE)

    def __str__(self):
        return self.q_question  # Corrected to return the quiz question



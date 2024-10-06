from django.urls import path
from .import views

urlpatterns=[
    path('',views.indexpage,name="index"),
    path('login',views.login,name="login"),
    path('checklogin',views.checklogin,name="checklogin"),
    path('discussion',views.discussion,name="discussion"),
    path('adddiscussion',views.adddiscussion,name="adddiscussion"),
    path('upvote/<int:id>/', views.upvote, name='upvote'),
    path('downvote/<int:id>/', views.downvote, name='downvote'),
    path('adduserdata', views.adduserdata, name='adduserdata'),
    path('registerd', views.register_page,name='registerd'),
    path('add_reply/<int:id>', views.add_reply,name='add_reply'),
    path('discussion/category/<int:category_id>/', views.discussion, name='discussion_by_category'),
    # For category-specific discussions
    path('logout',views.logoutpage,name='logout'),
    path('quiz/<str:symbol>/',views.quiz,name='quiz'),
    path('solar_system/',views.solar,name='solar'),
    path('planets/',views.planets,name='planets'),

]
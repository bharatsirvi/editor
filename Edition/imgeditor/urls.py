from django.contrib import admin
from django.urls import path,include
from imgeditor import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index,name="index"),
    path('home', views.home,name="home"),
    path('crop',views.crop,name='crop'),
    path('flip',views.flip,name='flip'),   
    path('contact',views.contact,name="contact"),
    path('about',views.about,name="about"),
    path('services',views.services,name="services"),
    path('dimensions',views.dimensions,name="dimensions"),
    path('percentage',views.percentage,name="percentage"),
    path('fliprotate',views.fliprotate,name="fliprotate"),
    path('crop_reset',views.crop_reset,name="crop_reset"),
    path('resize',views.resize,name="resize"),
    path('reset',views.reset,name="reset")      
]

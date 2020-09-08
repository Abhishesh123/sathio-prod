from django.urls import path
from sathio import views


urlpatterns = [
    path('', views.index),
    path('tcondition/',views.tcondition,name="tcondition"),
    path('privacypolicy/',views.privacypolicy,name="privacypolicy"),
    path('Login/',views.Login,name="Login"),
    path('Logout/',views.Logout,name="Logout"),
    path('home/',views.home,name='home'),
    path('allpost/',views.allpost,name="allpost")
    
    ]
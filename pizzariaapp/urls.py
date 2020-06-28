from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('admin/', adminLoginView, name = 'adminloginpage'),
    path('authenticateAdmin/',authenticateAdmin),
    path('admin/adminhome/',adminHomePageView, name = 'adminhomepage'),
    path('adminlogout/',logoutAdmin),
    path('addadminpizza/',addAdminPizza),
    path('deleteadminpizza/<int:pizzaid>/',deleteAdminPizza),
    path('',homePageView, name='homepageview'),
    path('signupuser/',signupUser,name='signupUser'),
    path('userloginview/',userLoginView,name="userloginview"),
    path('authenticateUser/',authenticateUser),
    path('customer/welcome/',customerWelcomePage,name='userwelcomepage'),
    path('customer/logout/',logoutUser),
]

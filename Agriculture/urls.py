from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.testing, name='testing'),
    path('api/register/', views.registerPage, name="register"),
    path('api/login/', views.loginPage, name="login"),
    path('api/fileupload/', views.fileupload, name="fileupload"),
    path('api/logout/', views.logoutUser, name="logout"),
    path('api/getuserdetails/', views.getuserdetails, name="getuserdetails"),
    path('api/getdatawithinrange/', views.getdatawithinrange, name="getdatawithinrange"),
    path('api/getroomsdata/', views.getroomsdata, name="getroomsdata"),
    path('api/getharvestdata/', views.getharvestdata, name="getharvestdata"),
    path('api/getlayoutsectionadd/', views.getlayoutsectionadd, name="getlayoutsectionadd"),
    path('api/getlayoutsectionread/', views.getlayoutsectionread, name="getlayoutsectionread"),
    path('api/getlayoutsectionupdate/', views.getlayoutsectionupdate, name="getlayoutsectionupdate"),
    path('api/getlayoutsectiondelete/', views.getlayoutsectiondelete, name="getlayoutsectiondelete"),
    path('api/gethardwareadd/', views.gethardwareadd, name="gethardwareadd"),
    path('api/gethardwareread/', views.gethardwareread, name="gethardwareread"),
    path('api/gethardwareupdate/', views.gethardwareupdate, name="gethardwareupdate"),
    path('api/gethardwaredelete/', views.gethardwaredelete, name="gethardwaredelete"),
    path('api/getsoftwareadd/', views.getsoftwareadd, name="getsoftwareadd"),
    path('api/getsoftwareread/', views.getsoftwareread, name="getsoftwareread"),
    path('api/getsoftwareupdate/', views.getsoftwareupdate, name="getsoftwareupdate"),
    path('api/getsoftwaredelete/', views.getsoftwaredelete, name="getsoftwaredelete"),


]

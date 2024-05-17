from django.urls import path

from . import views

urlpatterns = [
    path("",views.index, name="Dashboard" ),
    path("device/<int:number>", views.get_devices, name="device-list"),
    path("unit/<int:number>", views.byUnit),
    path("test/",views.test_api ),
    path("update/", views.update_devices),
    path("daily/", views.dailyData),
    path("monthly/", views.monthlyData),
    path("bill/", views.getBill),
    
]
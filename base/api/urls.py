from django.urls import path
from . import views

urlpatterns=[
    path('',views.getRoutes),
    path('room/',views.getRooms),
]
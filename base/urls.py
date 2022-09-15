from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.loginPage),
    path('logout/', views.logoutPage),
    path('register/', views.registerPage),
    path('', views.home),
    path('room/<int:pk>/', views.room),
    path('create-room/', views.createRoom,name="create-room"),
    path('update-room/<str:pk>', views.updateRoom,name="update-room"),
    path('delete-room/<str:pk>', views.deleteRoom,name="delete-room"),
    path('user-profile/<str:pk>', views.userProfile,name="user-profile"),
    path('update-user/', views.updateUser,name="update-user"),
    path('topics/', views.topicPage,name="topics"),
    path('activity/', views.activityPage,name="activity"),
]

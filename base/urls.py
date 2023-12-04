from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("room/<str:pk>/", views.room, name="room"),
    path("create-room/", views.create_room, name="create-room"),
    path("update-room/<str:pk>/", views.update_room, name="update-room"),
    path("delete-room/<str:pk>/", views.delete_room, name="delete-room"),

    path("login/", views.login_page, name="login-page"),
    path('register/', views.register_page, name='register-user'),
    path("logout/", views.logout_user, name="logout-user"),
    path('profile/<str:pk>/', views.profile_page, name='profile'),
    path('update-user/', views.update_user, name='update-user'),

    path("register/", views.register_page, name="register-page"),
    path("delete_message/<str:pk>/", views.delete_message, name="delete-message"),
    path("edit_message/<str:pk>/", views.edit_message, name="edit-message"),

    path("topics/", views.topics_page, name="topics"),
    path("activity/", views.activity_page, name="activity"),
]
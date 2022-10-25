from django.urls import path
from . import views

urlpatterns = [
#     blogs
    path("", views.blogs, name="blogs"),

#    user authentication
    path("register/", views.Register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
]
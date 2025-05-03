from django.contrib.auth import views as auth_views
from django.urls import path

app_name = "myauth"

urlpatterns = [
    path('sign-in/', auth_views.LoginView.as_view(template_name='myauth/sign-in.html'), name="sign-in"),
    path('logout/', auth_views.LogoutView.as_view(template_name='myauth/logged_out.html'), name="logout"),
]

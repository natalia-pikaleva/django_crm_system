from django.contrib.auth import views as auth_views
from django.urls import path

from .views import UserDetailView, MyPasswordChangeView

app_name = "myauth"

urlpatterns = [
    path('sign-in/', auth_views.LoginView.as_view(template_name='myauth/sign-in.html'), name="sign-in"),
    path('logout/', auth_views.LogoutView.as_view(template_name='myauth/logged_out.html'), name="logout"),
    path('profile/<int:pk>/',UserDetailView.as_view(), name="profile"),
    path('profile/<int:pk>/update', MyPasswordChangeView.as_view(), name="password_update"),

]

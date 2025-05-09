from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import reverse


class UserDetailView(DetailView):
    """Класс реализует просмотр данных пользователя"""
    model = User
    template_name = "myauth/user-details.html"
    queryset = User.objects.all()


class MyPasswordChangeView(PasswordChangeView):
    """Класс реализует смену пароля"""
    template_name = 'myauth/change-password.html'

    def get_success_url(self):
        return reverse(
            "myauth:profile",
            kwargs={"pk": self.request.user.pk},
        )

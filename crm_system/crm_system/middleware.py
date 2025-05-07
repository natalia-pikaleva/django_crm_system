# pylint: disable=too-few-public-methods
from django.shortcuts import redirect
from django.conf import settings

class LoginRedirectMiddleware:
    """Класс реализует middle функцию для перенаправления ползователей на страницу
    авторизации при получении ошибки 401 или 403"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code in (401, 403) and not request.user.is_authenticated:
            return redirect(f'{settings.LOGIN_URL}?next={request.path}')
        return response

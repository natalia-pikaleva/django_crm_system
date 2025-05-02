from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    ServiceViewSet,
    ServiceCreateView,
    ServiceUpdateView,
    ServiceDeleteView)

app_name = "services"

router = DefaultRouter()
router.register(r'', ServiceViewSet)

urlpatterns = [
    path('create/', ServiceCreateView.as_view(), name="service_create"),
    path('<int:pk>/update/', ServiceUpdateView.as_view(), name="service_update"),
    path('<int:pk>/delete/', ServiceDeleteView.as_view(), name="service_delete"),
    path('', include(router.urls)),

]

"""
Страницы для работы с услугами
Страница отображения списка активных услуг: у каждой записи должен быть уникальный идентификатор, 
например название. Записи — ссылки на переход к детальной странице. 
Рядом с ними нужно добавить кнопки для удаления, а на странице — общую кнопку для создания новой записи.
На детальной странице должна быть неизменяемая форма с данными о записи, 
а также кнопка для редактирования и удаления записи.
Страница редактирования должна быть предзаполненной и доступной для редактирования.
На странице создания записи должна быть пустая форма для заполнения.
"""
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView)
from django.shortcuts import reverse
from django.urls import reverse_lazy
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .models import Advertisement
from .serializers import AdvertisementSerializer


class AdvCampViewSet(PermissionRequiredMixin, ModelViewSet):
    """
    Набор представлений для действий над Advertisement.
    Полный CRUD для сущностей товара
    """
    permission_required = "adv_camp.view_advertisement"

    renderer_classes = [TemplateHTMLRenderer]
    queryset = Advertisement.objects.select_related("service").all()
    serializer_class = AdvertisementSerializer

    def get_template_names(self):
        if self.action == 'list':
            return ['adv_camp/advertisement_list.html']
        elif self.action == 'retrieve':
            return ['adv_camp/advertisement_detail.html']
        return super().get_template_names()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        context = {
            'object_list': queryset,
        }
        return Response(context)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        context = {
            'object': instance,
        }
        return Response(context)


class AdvCampCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "adv_camp.add_advertisement"

    model = Advertisement
    fields = "title", "promotion_channel", "budget", "service"
    success_url = reverse_lazy("advertisement:advertisement-list")


class AdvCampUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "adv_camp.change_advertisement"

    model = Advertisement
    fields = "title", "promotion_channel", "budget", "service"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "advertisement:advertisement-detail",
            kwargs={"pk": self.object.pk},
        )


class AdvCampDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "adv_camp.delete_advertisement"

    model = Advertisement
    success_url = reverse_lazy("advertisement:advertisement-list")

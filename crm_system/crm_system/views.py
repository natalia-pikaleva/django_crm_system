from django.views.generic import TemplateView

class IndexView(TemplateView):
    """Класс реализует функцию перенаправления на шаблон index.html"""
    template_name = "index.html"

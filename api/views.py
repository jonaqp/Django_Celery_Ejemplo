from django.shortcuts import HttpResponse
from django.views.generic import TemplateView

from .tasks import prueba_suma, enviar_mail


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

from django.shortcuts import HttpResponse

from .tasks import prueba_suma, enviar_mail


# Create your views here.
def index(request):
    prueba_suma.delay(5, 6)
    enviar_mail.delay("Asunto", "Contenido mensaje", "jony327@gmail.com")

    return HttpResponse("Hola")

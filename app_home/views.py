from django.views.generic import ListView
from django.shortcuts import render, redirect
from typing import Any
from .models import HomeSite
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
#from .forms import ContactForm

class XlexHomeView(ListView):
    model = HomeSite
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        # Chama a implementação base primeiro para obter um contexto
        context = super().get_context_data(**kwargs)
        
        # Obtém o objeto HomeSite
        home_site_object = HomeSite.objects.first()
        
        # Se o objeto existir, incrementa as visualizações e adiciona a contagem ao contexto
        if home_site_object:
            home_site_object.update_views()  # Certifique-se de que esta linha esteja aqui para atualizar as visualizações
            context['views_count'] = home_site_object.views
        else:
            context['views_count'] = 0
        
        # Adiciona outras variáveis ao contexto
        context["hide_navbar"] = True
        
        return context

# Páginas do Site (sobre, contato, paginas de listas, etc)

def jurisprudencias_list(request):
    return render(request, 'jurisprudencias.html', {'hide_sidebar':True})
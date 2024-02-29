from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.urls import reverse
from django.db.models import Q
from typing import Any
from django.utils.text import slugify

from .models import (
    SumulaModel,
    TribNameSumulaModel,
    SiglaTribSumulaModel,
    )

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )

from .forms import (
    CreateSumulaForm,
    UpdateSumulaForm,
)

class SumulasListView(ListView):
    model = SumulaModel
    template_name = 'templates_sumulas/sumulas_list.html'
    ordering = ['-date_created']
    paginate_by = 12
    context_object_name = 'sumulas'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["hide_sidebar"] = True
        return context

class SumulaSingularView(DetailView):
    model = SumulaModel
    template_name = 'templates_sumulas/sumula_single.html'
    slug_field = 'slug'
    slug_url_kwarg = 'sumula_slug'
    context_object_name = 'sumulas'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.update_views()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hide_sidebar"] = True
        sumulas = self.get_object()
        context['current_app'] = 'app_sumulas'
        return context

class TribNameSumulaView(ListView):
    model = TribNameSumulaModel
    template_name = 'templates_sumulas/sumulas_trib_names.html'
    context_object_name = 'sumulas'
    
    def get_queryset(self):
        tribNameSum_slug = self.kwargs['tribNameSum_slug']
        tribunaisSum = TribNameSumulaModel.objects.get(slug=tribNameSum_slug)
        return SumulaModel.objects.filter(tribunaisSum=tribunaisSum)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        tribNameSum_slug = self.kwargs['tribNameSum_slug']
        context['tribunaisSum'] = TribNameSumulaModel.objects.get(slug=tribNameSum_slug)
        context['tribunaisSums'] = TribNameSumulaModel.objects.all()
        context['current_app'] = 'app_sumulas'
        return context


class SiglaTribSumulasView(ListView):
    model = TribNameSumulaModel
    template_name = 'templates_sumulas/sumulas_trib_siglas.html'
    context_object_name = 'sumulas'
    
    def get_queryset(self):
        siglaTrib_slug = self.kwargs['siglaTrib_slug']
        siglaTribSumula = SiglaTribSumulasView.objects.get(slug=siglaTrib_slug)
        return SumulaModel.objects.filter(siglaTribSumula=siglaTribSumula)
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        siglaTrb_slug = self.kwargs['siglaTrib_slug']
        context['siglaTribSumula'] = SiglaTribSumulasView.objects.get(slug=siglaTrib_slug)
        context['siglaTribSumulas'] = SiglaTribSumulasView.objects.all()
        context['current_app'] = 'app_sumulas'
        return context   
    
# Classes Create; 

class CreateSumulaView(CreateView):
    model = SumulaModel
    template_name = 'templates_sumulas/sumula_create_post.html'
    form_class = CreateSumulaForm
    success_url = reverse_lazy('app_sumulas:sumula-single')
    
    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        response = super(CreateSumulaView, self).form_valid(form)
        return response
    
    def get_success_url(self):
        return reverse('app_sumulas:sumula-single', kwargs={'sumula_slug': self.object.slug})

class UpdateSumulaView(UpdateView):
    model = SumulaModel
    template_name = 'templates_sumulas/sumula_update_post.html'
    form_class = UpdateSumulaForm
    success_url = reverse_lazy('app_sumulas:sumulas-list')
    

class DeleteSumulaView(DeleteView):
    model = SumulaModel
    template_name = 'templates_sumulas/sumula_delete_post.html'
    success_url = reverse_lazy('app_sumulas:sumulas-list')
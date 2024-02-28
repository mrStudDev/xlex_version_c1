from django.shortcuts import render, redirect
from .forms import STJJurisprudenciaUploadForm
from .models import STJjurisprudenciaModel
from django.views.generic import ListView, DetailView
from typing import Any
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from datetime import datetime
import json


class STJjurisprudenciaView(ListView):
    model = STJjurisprudenciaModel
    template_name = 'templates_jurisprudencias/templates_juris_stj/juris_stj_list.html'
    ordering = ['-dataPublicacao']
    paginate_by = 10

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["publicacoes_count"] = STJjurisprudenciaModel.objects.all().count()
        context["hide_sidebar"] = True
        return context

class STJjurisprudenciaSingularView(DetailView):
    model = STJjurisprudenciaModel
    template_name = 'templates_jurisprudencias/templates_juris_stj/juris_stj_single.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["hide_sidebar"] = True
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Contagem das Visualizações
        self.object.update_views() 
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


def upload_jurisprudencia_view(request):
    if request.method == 'POST':
        form = STJJurisprudenciaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            try:
                with open(uploaded_file.upload.path, 'r') as file:
                    data = json.load(file)

                instances = []
                for item in data:
                    date_str = item.get('data_formatada')
                    
                    # Convertendo a string de data para um objeto date
                    try:
                        formatted_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
                    except ValueError:
                        print(f"Erro ao converter a data: {date_str}")
                        continue

                    instance = STJjurisprudenciaModel(
                        id_herdadoSTJ=item.get('id_herdadoSTJ', ''),
                        numeroProcesso=item.get('numeroProcesso', ''),
                        numeroRegistro=item.get('numeroRegistro', ''),
                        siglaClasse=item.get('siglaClasse', ''),
                        descricaoClasse=item.get('descricaoClasse', ''),
                        nomeOrgaoJulgador=item.get('nomeOrgaoJulgador', ''),
                        ministroRelator=item.get('ministroRelator', ''),
                        dataPublicacao=item.get('dataPublicacao', ''),
                        data_formatada=formatted_date,                        
                        ementa=item.get('ementa', ''),
                        tipoDeDecisao=item.get('tipoDeDecisao', ''),
                        dataDecisao=item.get('dataDecisao', ''),
                        decisao=item.get('decisao', ''),
                        jurisprudenciaCitada=item.get('jurisprudenciaCitada', ''),
                        notas=item.get('notas', ''),
                        informacoesComplementares=item.get('informacoesComplementares', ''),
                        termosAuxiliares=item.get('termosAuxiliares', ''),
                        teseJuridica=item.get('teseJuridica', ''),
                        tema=item.get('tema', ''),
                        referenciasLegislativas=item.get('referenciasLegislativas', ''),
                        acordaosSimilares=item.get('acordaosSimilares', ''),
                        meta_description=item.get('meta_description', ''),
                        title=item.get('title', ''),                        
                        keyword=item.get('keyword', ''),
                        slug=item.get('slug', ''),
                    )
                    instances.append(instance)
                STJjurisprudenciaModel.objects.bulk_create(instances)
                messages.success(request, 'Upload e processamento bem-sucedidos.')
                return redirect('app_juris_stj:juris-stj-upload')

            except Exception as e:
                messages.error(request, f'Ocorreu um erro: {e}')

            return redirect('app_juris_stj:juris-stj-upload')
        else:
            messages.error(request, 'Formulário inválido. Por favor, verifique o arquivo enviado.')

    else:
        form = STJJurisprudenciaUploadForm()

    return render(request, 'templates_jurisprudencias/templates_juris_stj/juris_stj_uploads.html', {'form': form})


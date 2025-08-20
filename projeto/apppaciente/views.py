from __future__ import unicode_literals

from datetime import timedelta, datetime

from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.utils import timezone
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.base import TemplateView

from utils.decorators import LoginRequiredMixin, PacienteRequiredMixin

from agenda.forms import BuscaAgendaForm
from agenda.models import Agenda

from aviso.models import Aviso
from treino.forms import BuscaTreinoForm
from treino.models import Treino, TreinoExecucao
from usuario.models import Usuario

from .forms import PacienteCreateForm


class HomeView(LoginRequiredMixin, PacienteRequiredMixin, TemplateView):
    template_name = 'apppaciente/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avisos'] = Aviso.ativos.filter(destinatario__in=[self.request.user.tipo, 'TODOS'])[0:2]
        return context

class AboutView(LoginRequiredMixin, PacienteRequiredMixin, TemplateView):
    template_name = 'apppaciente/about.html'
    

class DadosPacienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Usuario
    template_name = 'apppaciente/dados_paciente_form.html'
    form_class = PacienteCreateForm  
    
    success_url = 'apppaciente_home'

    def get_object(self, queryset=None):
        return self.request.user
     
    def get_success_url(self):
        messages.success(self.request, 'Seus dados foram alterados com sucesso!')
        return reverse(self.success_url)


class MinhaAgendaListView(LoginRequiredMixin, PacienteRequiredMixin, ListView):
    model = Agenda
    template_name = 'apppaciente/agenda_minha_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dados filtrando
            context['form'] = BuscaAgendaForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            context['form'] = BuscaAgendaForm()
        return context

    def get_queryset(self):                
        qs = super().get_queryset().filter(paciente=self.request.user)      
        
        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaAgendaForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaAgendaForm()

        if form.is_valid():            
            pesquisa = form.cleaned_data.get('pesquisa')            
                        
            if pesquisa:
                qs = qs.filter(Q(fisioterapeuta__nome__icontains=pesquisa) |
                            Q(data__icontains=pesquisa) |
                            Q(hora__icontains=pesquisa) |
                            Q(comentarios__icontains=pesquisa))
        return qs
    
    
class MeuTreinoListView(LoginRequiredMixin, ListView):
    model = Treino
    template_name = 'apppaciente/treino_meu_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dados filtrando
            context['form'] = BuscaTreinoForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            context['form'] = BuscaTreinoForm()
        return context

    def get_queryset(self):                
        qs = super().get_queryset().filter(paciente=self.request.user)       
        
        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaTreinoForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaTreinoForm()

        if form.is_valid():            
            pesquisa = form.cleaned_data.get('pesquisa')            
                        
            if pesquisa:
                qs = qs.filter(Q(descricao__icontains=pesquisa))
                     
            
        return qs
 
 
class TreinoExecucaoCreateView(LoginRequiredMixin, CreateView):
    model = TreinoExecucao
    template_name = 'apppaciente/treino_execucao_form.html'
    fields = ['observacao']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        treino = Treino.objects.get(slug=self.kwargs['treino_slug'])
        context['treino'] = treino
        return context

    def form_valid(self, form):
        treino = Treino.objects.get(slug=self.kwargs['treino_slug'])
        
        qtd_treinos_realizados = TreinoExecucao.objects.filter(treino=treino).count()
        if treino.quantidade_vezes_periodo == qtd_treinos_realizados:
            treino.realizado = True
        treino_execucao = form.save(commit=False)
        treino_execucao.treino = treino
        treino_execucao.data_hora = timezone.now()
        treino_execucao.save()
        treino.save()
        
        messages.success(self.request, 'Treino marcado como realizado com sucesso!')
        return redirect('apppaciente_treino_meu_list')
    

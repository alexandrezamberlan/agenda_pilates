from __future__ import unicode_literals

from django.contrib import messages

from django.db.models import Q

from django.shortcuts import redirect, get_object_or_404

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse

from utils.decorators import LoginRequiredMixin, StaffRequiredMixin, FisioterapeutaRequiredMixin

from .models import Exercicio

from .forms import BuscaExercicioForm


class ExercicioListView(LoginRequiredMixin, FisioterapeutaRequiredMixin, ListView):
    model = Exercicio

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dados filtrando
            context['form'] = BuscaExercicioForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            context['form'] = BuscaExercicioForm()
        return context

    def get_queryset(self):                
        qs = super().get_queryset().all()        
        
        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaExercicioForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaExercicioForm()

        if form.is_valid():            
            pesquisa = form.cleaned_data.get('pesquisa')            
                        
            if pesquisa:
                qs = qs.filter(Q(descricao__icontains=pesquisa))
                     
            
        return qs
 

class ExercicioCreateView(LoginRequiredMixin, FisioterapeutaRequiredMixin, CreateView):
    model = Exercicio
    fields = ['descricao', 'tempo', 'intensidade', 'video', 'is_active']
    success_url = 'exercicio_list'
    
    
    def get_success_url(self):
        messages.success(self.request, 'Exercício cadastrado com sucesso na plataforma!')
        return reverse(self.success_url)


class ExercicioUpdateView(LoginRequiredMixin, FisioterapeutaRequiredMixin, UpdateView):
    model = Exercicio
    fields = ['descricao', 'tempo', 'intensidade', 'video', 'is_active']
    success_url = 'exercicio_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Exercício atualizado com sucesso na plataforma!')
        return reverse(self.success_url) 


class ExercicioDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Exercicio
    success_url = 'exercicio_list'

    def get_success_url(self):
        messages.success(self.request, 'Exercício removido com sucesso na plataforma!')
        return reverse(self.success_url) 

    def post(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        try:
            self.object.delete()
            success_url = self.get_success_url()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à esse exercício, permissão negada!')
        return redirect(self.success_url)


class ExercicioAnimacaoView(LoginRequiredMixin, DetailView):
    """
    View para exibir a animação de um exercício individual
    """
    model = Exercicio
    template_name = 'exercicio/exercicio_animacao.html'
    context_object_name = 'exercicio'
    
    def get_object(self):
        return get_object_or_404(Exercicio, slug=self.kwargs['slug'], is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exercicio = self.get_object()
        
        # Calcular o tempo total da animação (preparação + contração + relaxamento)
        tempo_preparacao = 5  # 5 segundos de preparação
        tempo_contracao = exercicio.tempo
        tempo_relaxamento = exercicio.tempo
        tempo_total = tempo_preparacao + tempo_contracao + tempo_relaxamento
        
        context['tempo_total'] = tempo_total
        
        return context
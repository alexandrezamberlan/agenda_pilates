from __future__ import unicode_literals

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.utils import timezone
import json

from django.db.models import Q

from django.shortcuts import redirect

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse

from utils.decorators import LoginRequiredMixin, StaffRequiredMixin, FisioterapeutaRequiredMixin

from .models import Treino, TreinoExecucao

from .forms import BuscaTreinoForm, TreinoForm, MeuTreinoForm


class TreinoListView(LoginRequiredMixin, ListView):
    model = Treino

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
        qs = super().get_queryset().all()        
        
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
 

class TreinoCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Treino
    form_class = TreinoForm
    success_url = 'treino_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Treino cadastrado com sucesso na plataforma!')
        return reverse(self.success_url)


class TreinoUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Treino
    form_class = TreinoForm
    success_url = 'treino_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Treino atualizado com sucesso na plataforma!')
        return reverse(self.success_url) 


class TreinoDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Treino
    success_url = 'treino_list'

    def get_success_url(self):
        messages.success(self.request, 'Treino removido com sucesso na plataforma!')
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
            messages.error(request, 'Há dependências ligadas à esse treino, permissão negada!')
        return redirect(self.success_url)


class TreinoExecucaoView(LoginRequiredMixin, DetailView):
    """
    View para exibir a página de execução do treino com interface JavaScript dinâmica
    """
    model = Treino
    template_name = 'treino/treino_execucao.html'
    context_object_name = 'treino'
    success_url = 'apppaciente_treino_meu_list'
    
    
    def get_object(self):
        return get_object_or_404(Treino, slug=self.kwargs['slug'], is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        treino = self.get_object()
        
        # Adicionar informações extras se necessário
        context['total_exercicios'] = treino.exercicios.count()
        context['tempo_total_estimado'] = self.calcular_tempo_total(treino)
        
        return context
    
    def calcular_tempo_total(self, treino):
        """
        Calcula o tempo total estimado para o treino em segundos
        """
        tempo_total = 5  # Preparação inicial
        
        for exercicio in treino.exercicios.all():
            # Tempo de contração + relaxamento para cada repetição
            tempo_exercicio = (exercicio.tempo * 2) * treino.quantidade_repeticoes
            tempo_total += tempo_exercicio
        
        # Pausas entre exercícios (exceto após o último)
        if treino.exercicios.count() > 1:
            tempo_total += treino.pausas * (treino.exercicios.count() - 1)
        
        return tempo_total


@require_http_methods(["POST"])
@csrf_exempt  # Removido para usar CSRF token no frontend
def registrar_execucao_treino(request, treino_id):
    """
    View para registrar a execução de um treino via AJAX
    """
    try:
        # Verificar se usuário está autenticado
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'Usuário não autenticado'
            }, status=401)
        
        # Buscar o treino
        treino = get_object_or_404(Treino, id=treino_id, is_active=True)
        
        # Verificar se o usuário tem permissão (é o paciente do treino ou fisioterapeuta)
        if not (request.user == treino.paciente or request.user == treino.fisioterapeuta or request.user.is_staff):
            return JsonResponse({
                'success': False,
                'error': 'Permissão negada'
            }, status=403)
        
        # Parse dos dados JSON
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Dados JSON inválidos'
            }, status=400)
        
        # Criar registro de execução
        execucao = TreinoExecucao.objects.create(
            treino=treino,
            data_hora=timezone.now(),
            observacao=data.get('observacao', 'Treino executado via interface web')
        )
        
        # Marcar treino como realizado se ainda não estiver
        if not treino.realizado:
            treino.realizado = True
            treino.save()
        
        return JsonResponse({
            'success': True,
            'execucao_id': execucao.id,
            'data_hora': execucao.data_hora.isoformat(),
            'message': 'Execução registrada com sucesso!'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }, status=500)


def treino_execucao_historico(request, slug):
    """
    View para exibir histórico de execuções de um treino
    """
    treino = get_object_or_404(Treino, slug=slug, is_active=True)
    
    # Verificar permissão
    if not (request.user == treino.paciente or request.user == treino.fisioterapeuta or request.user.is_staff):
        messages.error(request, 'Você não tem permissão para visualizar este treino.')
        return redirect('treino_list')
    
    execucoes = TreinoExecucao.objects.filter(treino=treino).order_by('-data_hora')
    
    context = {
        'treino': treino,
        'execucoes': execucoes,
        'total_execucoes': execucoes.count()
    }
    
    return render(request, 'treino/treino_execucao_historico.html', context)
    
    
class MeuTreinoListView(LoginRequiredMixin, FisioterapeutaRequiredMixin, ListView):
    model = Treino
    template_name = 'treino/treino_meu_list.html'

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
        qs = super().get_queryset().filter(fisioterapeuta=self.request.user)     
        
        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaTreinoForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaTreinoForm()

        if form.is_valid():            
            pesquisa = form.cleaned_data.get('pesquisa')            
                        
            if pesquisa:
                qs = qs.filter(Q(descricao__icontains=pesquisa) | Q(paciente__nome__icontains=pesquisa) | Q(exercicio__descricao__icontains=pesquisa))
                     
        return qs
 

class MeuTreinoCreateView(LoginRequiredMixin, FisioterapeutaRequiredMixin, CreateView):
    model = Treino
    form_class = MeuTreinoForm
    template_name = 'treino/treino_meu_form.html'
    success_url = 'treino_meu_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Treino cadastrado com sucesso na plataforma!')
        return reverse(self.success_url)
    
    def form_valid(self, form):
        try:
            self.object = form.save(commit=False)
            self.object.fisioterapeuta = self.request.user
            self.object.save()
        except Exception as e:
            messages.error(self.request, 'Este treino já está na plataforma!')
            return self.form_invalid(form)
        
        return super().form_valid(form)


class MeuTreinoUpdateView(LoginRequiredMixin, FisioterapeutaRequiredMixin, UpdateView):
    model = Treino
    form_class = MeuTreinoForm
    template_name = 'treino/treino_meu_form.html'
    success_url = 'treino_meu_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Treino atualizado com sucesso na plataforma!')
        return reverse(self.success_url) 
    
    def form_valid(self, form):
        try:
            self.object = form.save(commit=False)
            self.object.fisioterapeuta = self.request.user
            self.object.save()
        except Exception as e:
            messages.error(self.request, 'Este treino já está na plataforma!')
            return self.form_invalid(form)
        
        return super().form_valid(form)


class MeuTreinoDeleteView(LoginRequiredMixin, FisioterapeutaRequiredMixin, DeleteView):
    model = Treino
    template_name = 'treino/treino_meu_confirm_delete.html'
    success_url = 'treino_meu_list'

    def get_success_url(self):
        messages.success(self.request, 'Treino removido com sucesso na plataforma!')
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
            messages.error(request, 'Há dependências ligadas à esse treino, permissão negada!')
        return redirect(self.success_url)
    
    
class TreinoExecucaoObservacoesListView(LoginRequiredMixin, ListView):
    model = TreinoExecucao
    template_name = 'treino/treino_execucao_observacoes_list.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        treino = Treino.objects.get(slug=self.kwargs['treino_slug'])
        context['treino'] = treino
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if self.request.GET:
    #         #quando ja tem dados filtrando
    #         context['form'] = BuscaTreinoForm(data=self.request.GET)
    #     else:
    #         #quando acessa sem dados filtrando
    #         context['form'] = BuscaTreinoForm()
    #     return context

    def get_queryset(self):                
        qs = super().get_queryset().filter(treino__slug=self.kwargs['treino_slug']).exclude(observacao__isnull=True).exclude(observacao__exact='')
        
        # if self.request.GET:
        #     #quando ja tem dados filtrando
        #     form = BuscaTreinoForm(data=self.request.GET)
        # else:
        #     #quando acessa sem dados filtrando
        #     form = BuscaTreinoForm()

        # if form.is_valid():            
        #     pesquisa = form.cleaned_data.get('pesquisa')            
                        
        #     if pesquisa:
        #         qs = qs.filter(Q(descricao__icontains=pesquisa))
                     
            
        return qs
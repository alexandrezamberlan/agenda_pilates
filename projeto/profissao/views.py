from __future__ import unicode_literals

from django.contrib import messages

from django.db.models import Q

from django.shortcuts import redirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse

from utils.decorators import LoginRequiredMixin, StaffRequiredMixin, SecretariaRequiredMixin

from .models import Profissao

from .forms import BuscaProfissaoForm


class ProfissaoListView(LoginRequiredMixin, SecretariaRequiredMixin, ListView):
    model = Profissao

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dados filtrando
            context['form'] = BuscaProfissaoForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            context['form'] = BuscaProfissaoForm()
        return context

    def get_queryset(self):                
        qs = super().get_queryset().all()        
        
        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaProfissaoForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaProfissaoForm()

        if form.is_valid():            
            pesquisa = form.cleaned_data.get('pesquisa')            
                        
            if pesquisa:
                qs = qs.filter(descricao__icontains=pesquisa)             
            
        return qs
 

class ProfissaoCreateView(LoginRequiredMixin, SecretariaRequiredMixin, CreateView):
    model = Profissao
    fields = ['descricao', 'is_active']
    success_url = 'profissao_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Profissão cadastrada com sucesso na plataforma!')
        return reverse(self.success_url)


class ProfissaoUpdateView(LoginRequiredMixin, SecretariaRequiredMixin, UpdateView):
    model = Profissao
    fields = ['descricao', 'is_active']
    success_url = 'profissao_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Profissão atualizada com sucesso na plataforma!')
        return reverse(self.success_url) 


class ProfissaoDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Profissao
    success_url = 'profissao_list'

    def get_success_url(self):
        messages.success(self.request, 'Profissão removida com sucesso na plataforma!')
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
            messages.error(request, 'Há dependências ligadas à essa Profissão, permissão negada!')
        return redirect(self.success_url)
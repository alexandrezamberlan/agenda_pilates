from __future__ import unicode_literals

from django.contrib import messages

from django.db.models import Q

from django.shortcuts import redirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse

from utils.decorators import LoginRequiredMixin, StaffRequiredMixin, SecretariaRequiredMixin

from .models import Renda

from .forms import BuscaRendaForm


class RendaListView(LoginRequiredMixin, SecretariaRequiredMixin, ListView):
    model = Renda

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dados filtrando
            context['form'] = BuscaRendaForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            context['form'] = BuscaRendaForm()
        return context

    def get_queryset(self):                
        qs = super().get_queryset().all()        
        
        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaRendaForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaRendaForm()

        if form.is_valid():            
            pesquisa = form.cleaned_data.get('pesquisa')            
                        
            if pesquisa:
                qs = qs.filter(descricao__icontains=pesquisa)             
            
        return qs
 

class RendaCreateView(LoginRequiredMixin, SecretariaRequiredMixin, CreateView):
    model = Renda
    fields = ['descricao', 'is_active']
    success_url = 'renda_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Renda cadastrada com sucesso na plataforma!')
        return reverse(self.success_url)


class RendaUpdateView(LoginRequiredMixin, SecretariaRequiredMixin, UpdateView):
    model = Renda
    fields = ['descricao',  'is_active']
    success_url = 'renda_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Renda atualizada com sucesso na plataforma!')
        return reverse(self.success_url) 


class RendaDeleteView(LoginRequiredMixin, SecretariaRequiredMixin, DeleteView):
    model = Renda
    success_url = 'renda_list'

    def get_success_url(self):
        messages.success(self.request, 'Renda removida com sucesso na plataforma!')
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
            messages.error(request, 'Há dependências ligadas à essa Renda, permissão negada!')
        return redirect(self.success_url)
from __future__ import unicode_literals

from django.contrib import messages

from django.db.models import Q

from django.shortcuts import redirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse

from utils.decorators import LoginRequiredMixin, StaffRequiredMixin, FisioterapeutaRequiredMixin

from .models import Artigo

from .forms import BuscaArtigoForm


class ArtigoListView(LoginRequiredMixin, ListView):
    model = Artigo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dados filtrando
            context['form'] = BuscaArtigoForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            context['form'] = BuscaArtigoForm()
        return context

    def get_queryset(self):                
        qs = super().get_queryset().all()        
        
        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaArtigoForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaArtigoForm()

        if form.is_valid():            
            pesquisa = form.cleaned_data.get('pesquisa')            
                        
            if pesquisa:
                qs = qs.filter(Q(titulo__icontains=pesquisa) | Q(texto__icontains=pesquisa))
                     
            
        return qs
 

class ArtigoCreateView(LoginRequiredMixin, FisioterapeutaRequiredMixin, CreateView):
    model = Artigo
    fields = ['titulo', 'texto', 'arquivo', 'is_active']
    success_url = 'artigo_list'
    
    def form_valid(self, form):
        try:
            artigo = form.save(commit=False)
            artigo.responsavel = self.request.user
            artigo.save()
            self.object = artigo
        except Exception as e:
            messages.error(self.request, 'Erro ao associar artigo ao usuário. %s' % e)
        
        return super(ArtigoCreateView, self).form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Artigo cadastrado com sucesso na plataforma!')
        return reverse(self.success_url)


class ArtigoUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Artigo
    fields = ['titulo', 'texto', 'arquivo', 'is_active']
    success_url = 'artigo_list'
    
    def form_valid(self, form):
        try:
            artigo = form.save(commit=False)
            artigo.responsavel = self.request.user
            artigo.save()
            self.object = artigo
        except Exception as e:
            messages.error(self.request, 'Erro ao associar artigo ao usuário. %s' % e)
        
        return super(ArtigoUpdateView, self).form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Artigo atualizado com sucesso na plataforma!')
        return reverse(self.success_url) 


class ArtigoDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Artigo
    success_url = 'artigo_list'

    def get_success_url(self):
        messages.success(self.request, 'Artigo removido com sucesso na plataforma!')
        return reverse(self.success_url) 

    def post(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à esse artigo, permissão negada!')
        return redirect(self.success_url)
from __future__ import unicode_literals

from django.contrib import messages

from django.db.models import Q

from django.shortcuts import redirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse

from utils.decorators import LoginRequiredMixin, StaffRequiredMixin, FisioterapeutaRequiredMixin, SecretariaRequiredMixin

from .models import Agenda

from .forms import BuscaAgendaForm, AgendaForm, MinhaAgendaForm


class AgendaListView(LoginRequiredMixin, FisioterapeutaRequiredMixin, ListView):
    model = Agenda

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
        qs = super().get_queryset().all()        
        
        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaAgendaForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaAgendaForm()

        if form.is_valid():            
            pesquisa = form.cleaned_data.get('pesquisa')            
                        
            if pesquisa:
                qs = qs.filter(Q(paciente__nome__icontains=pesquisa) |
                               Q(fisioterapeuta__nome__icontains=pesquisa) |
                               Q(data__icontains=pesquisa) |
                               Q(hora__icontains=pesquisa) |
                               Q(comentarios__icontains=pesquisa))
        return qs
 

class AgendaCreateView(LoginRequiredMixin, SecretariaRequiredMixin, CreateView):
    model = Agenda
    form_class = AgendaForm
    success_url = 'agenda_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Consulta cadastrada com sucesso na plataforma!')
        return reverse(self.success_url)


class AgendaUpdateView(LoginRequiredMixin, SecretariaRequiredMixin, UpdateView):
    model = Agenda
    form_class = AgendaForm
    success_url = 'agenda_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Consulta atualizada com sucesso na plataforma!')
        return reverse(self.success_url) 


class AgendaDeleteView(LoginRequiredMixin, SecretariaRequiredMixin, DeleteView):
    model = Agenda
    success_url = 'agenda_list'

    def get_success_url(self):
        messages.success(self.request, 'Consulta removida com sucesso na plataforma!')
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
            messages.error(request, 'Há dependências ligadas à essa Consulta, permissão negada!')
        return redirect(self.success_url)
    
    
class MinhaAgendaListView(LoginRequiredMixin, FisioterapeutaRequiredMixin, ListView):
    model = Agenda
    template_name = 'agenda/agenda_minha_list.html'

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
        qs = super().get_queryset().filter(fisioterapeuta=self.request.user)      
        
        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaAgendaForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaAgendaForm()

        if form.is_valid():            
            pesquisa = form.cleaned_data.get('pesquisa')            
                        
            if pesquisa:
                qs = qs.filter(Q(paciente__nome__icontains=pesquisa) |
                            Q(data__icontains=pesquisa) |
                            Q(hora__icontains=pesquisa) |
                            Q(comentarios__icontains=pesquisa))
        return qs


class MinhaAgendaCreateView(LoginRequiredMixin, FisioterapeutaRequiredMixin, CreateView):
    model = Agenda
    form_class = MinhaAgendaForm
    template_name = 'agenda/agenda_minha_form.html'
    success_url = 'agenda_minha_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Consulta cadastrada com sucesso na plataforma!')
        return reverse(self.success_url)
    
    def form_valid(self, form):
        try:
            self.object = form.save(commit=False)
            self.object.fisioterapeuta = self.request.user
            self.object.save()
        except Exception as e:
            messages.error(self.request, 'Esta consulta já está agendada')
            return self.form_invalid(form)
        
        return super().form_valid(form)


class MinhaAgendaUpdateView(LoginRequiredMixin, FisioterapeutaRequiredMixin, UpdateView):
    model = Agenda
    form_class = MinhaAgendaForm
    template_name = 'agenda/agenda_minha_form.html'
    success_url = 'agenda_minha_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Consulta atualizada com sucesso na plataforma!')
        return reverse(self.success_url) 

    def form_valid(self, form):
        try:
            self.object = form.save(commit=False)
            self.object.fisioterapeuta = self.request.user
            self.object.save()
        except Exception as e:
            messages.error(self.request, 'Esta consulta já está agendada')
            return self.form_invalid(form)
        
        return super().form_valid(form)


class MinhaAgendaDeleteView(LoginRequiredMixin, FisioterapeutaRequiredMixin, DeleteView):
    model = Agenda
    template_name = 'agenda/agenda_minha_confirm_delete.html'
    success_url = 'agenda_minha_list'

    def get_success_url(self):
        messages.success(self.request, 'Consulta removida com sucesso na plataforma!')
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
            messages.error(request, 'Há dependências ligadas à essa Consulta, permissão negada!')
        return redirect(self.success_url)
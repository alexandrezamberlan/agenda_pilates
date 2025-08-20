from django import forms
from django.db import models

from .models import Agenda
from usuario.models import Usuario


class BuscaAgendaForm(forms.Form):        
    pesquisa = forms.CharField(label='Pesquisa livre', required=False)
    
    
class AgendaForm(forms.ModelForm):
    paciente = forms.ModelChoiceField(label='Paciente em treinamento *', queryset=Usuario.pacientes_ativos.all())
    fisioterapeuta = forms.ModelChoiceField(label='Fisioterapeuta que prescreve o treinamento *', queryset=Usuario.fisioterapeutas.all())
        
    class Meta:
        model = Agenda
        fields = ['paciente', 'fisioterapeuta', 'data', 'hora', 'comentarios', 'realizado', 'is_active']


class MinhaAgendaForm(forms.ModelForm):
    paciente = forms.ModelChoiceField(label='Paciente em treinamento *', queryset=Usuario.pacientes_ativos.all())
    # fisioterapeuta = forms.ModelChoiceField(label='Fisioterapeuta que prescreve o treinamento *', queryset=Usuario.fisioterapeutas.all())
    
        
    class Meta:
        model = Agenda
        fields = ['paciente', 'data', 'hora', 'comentarios', 'realizado', 'is_active']
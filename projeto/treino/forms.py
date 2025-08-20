from django import forms
from django.db import models

from .models import Treino
from usuario.models import Usuario


class BuscaTreinoForm(forms.Form):        
    pesquisa = forms.CharField(label='Pesquisa livre', required=False)
    
    
class TreinoForm(forms.ModelForm):
    paciente = forms.ModelChoiceField(label='Paciente em treinamento *', queryset=Usuario.pacientes_ativos.all())
    fisioterapeuta = forms.ModelChoiceField(label='Fisioterapeuta que prescreve o treinamento *', queryset=Usuario.fisioterapeutas.all())
        
    class Meta:
        model = Treino
        fields = ['descricao', 'paciente', 'fisioterapeuta', 'exercicios', 'quantidade_repeticoes', 'pausas', 'data_inicio', 'data_fim', 'quantidade_vezes_periodo', 'realizado', 'is_active']


class MeuTreinoForm(forms.ModelForm):
    paciente = forms.ModelChoiceField(label='Paciente em treinamento *', queryset=Usuario.pacientes_ativos.all())
    
        
    class Meta:
        model = Treino
        fields = ['descricao', 'paciente', 'exercicios', 'quantidade_repeticoes', 'pausas', 'data_inicio', 'data_fim', 'quantidade_vezes_periodo', 'realizado', 'is_active']

 
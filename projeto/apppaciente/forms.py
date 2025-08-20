from django import forms

from django.core.validators import MaxValueValidator, MinValueValidator

from profissao.models import Profissao
from instituicao.models import Instituicao
from usuario.models import Usuario


class PacienteCreateForm(forms.ModelForm):
    nome = forms.CharField(label='Nome completo *', help_text='* Campos obrigatórios',required=True)        
    profissao = forms.ModelChoiceField(label='Profissão', queryset=Profissao.profissoes_ativas.all(), required=False)
    email = forms.EmailField(label='Email *', help_text='Use o email válido. Será usado para acessar sistema e recuperar senha!',required=True)
    celular = forms.CharField(label='Número celular com DDD *', help_text="Use DDD, por exemplo 55987619832",required=True)
    cpf = forms.CharField(label='CPF *',required=True)    
    
        
    class Meta:
        model = Usuario
        fields = ['nome', 'profissao', 'email', 'celular', 'cpf']



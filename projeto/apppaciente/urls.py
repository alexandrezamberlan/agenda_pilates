from __future__ import unicode_literals
from django.urls import path

from core.views import HomeRedirectView

from .views import (DadosPacienteUpdateView, MinhaAgendaListView, MeuTreinoListView,          
                    HomeView, AboutView, TreinoExecucaoCreateView)

urlpatterns = [
   path('home', HomeView.as_view(), name='apppaciente_home'), 
   # path('', HomeRedirectView.as_view(), name='home_redirect'),
   path('about', AboutView.as_view(), name='apppaciente_about'),
   
   path('meus-dados/', DadosPacienteUpdateView.as_view(), name='apppaciente_dados_update'),
   path('minhasagendas/', MinhaAgendaListView.as_view(), name='apppaciente_agenda_minha_list'),
   path('meustreinos/', MeuTreinoListView.as_view(), name='apppaciente_treino_meu_list'),
   path('meustreinos/<slug:treino_slug>/execucao', TreinoExecucaoCreateView.as_view(), name='apppaciente_treino_execucao_create'),
]

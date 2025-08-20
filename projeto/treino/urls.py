from django.urls import path

from .views import (TreinoListView, TreinoCreateView, TreinoUpdateView, TreinoDeleteView,
                    MeuTreinoCreateView, MeuTreinoUpdateView, MeuTreinoListView, MeuTreinoDeleteView,
                    TreinoExecucaoView, TreinoExecucaoObservacoesListView)
                    # registrar_execucao_treino, treino_execucao_historico


urlpatterns = [
	path('list/', TreinoListView.as_view(), name='treino_list'),
	path('cad/', TreinoCreateView.as_view(), name='treino_create'),
	path('<slug:slug>/', TreinoUpdateView.as_view(), name='treino_update'),
	path('<slug:slug>/delete/', TreinoDeleteView.as_view(), name='treino_delete'), 
 
 	path('meutreino/cad/', MeuTreinoCreateView.as_view(), name='treino_meu_create'),
	path('meutreino/<slug:slug>/', MeuTreinoUpdateView.as_view(), name='treino_meu_update'),
	path('meustreinos/list/', MeuTreinoListView.as_view(), name='treino_meu_list'),
 	path('meutreino/<slug:slug>/delete', MeuTreinoDeleteView.as_view(), name='treino_meu_delete'),
 	path('observacoes/<slug:treino_slug>/', TreinoExecucaoObservacoesListView.as_view(), name='apppaciente_treino_observacoes'),
  
	
 	# URLs para execução de treino - SERÁ QUE NAO DEVERIA ESTAR NA urls.py do apppaciente?
	path('<slug:slug>/executar/', TreinoExecucaoView.as_view(), name='treino_executar'),
	
	# REVER!!!
 	# path('<int:treino_id>/registrar-execucao/', registrar_execucao_treino, name='treino_registrar_execucao'),
	# path('<slug:slug>/historico/', treino_execucao_historico, name='treino_execucao_historico'),
]
 
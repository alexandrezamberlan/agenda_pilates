from django.urls import path

from .views import ProfissaoListView, ProfissaoCreateView
from .views import ProfissaoUpdateView, ProfissaoDeleteView


urlpatterns = [
	path('list/', ProfissaoListView.as_view(), name='profissao_list'),
	path('cad/', ProfissaoCreateView.as_view(), name='profissao_create'),
	path('<slug:slug>/', ProfissaoUpdateView.as_view(), name='profissao_update'),
	path('<slug:slug>/delete/', ProfissaoDeleteView.as_view(), name='profissao_delete'), 
]
 
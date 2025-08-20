from django.urls import path

from .views import AgendaListView, AgendaCreateView, AgendaUpdateView, AgendaDeleteView
from .views import MinhaAgendaCreateView, MinhaAgendaUpdateView, MinhaAgendaDeleteView, MinhaAgendaListView

urlpatterns = [
	path('list/', AgendaListView.as_view(), name='agenda_list'),
	path('cad/', AgendaCreateView.as_view(), name='agenda_create'),
	path('<slug:slug>/', AgendaUpdateView.as_view(), name='agenda_update'),
	path('<slug:slug>/delete/', AgendaDeleteView.as_view(), name='agenda_delete'), 
 
 	path('cad/minhaagenda/', MinhaAgendaCreateView.as_view(), name='agenda_minha_create'),
	path('<slug:slug>/minhaagenda/', MinhaAgendaUpdateView.as_view(), name='agenda_minha_update'),
	path('list/minhasagendas/', MinhaAgendaListView.as_view(), name='agenda_minha_list'),
 	path('<slug:slug>/delete/minhaagenda/', MinhaAgendaDeleteView.as_view(), name='agenda_minha_delete'),
]
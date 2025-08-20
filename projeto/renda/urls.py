from django.urls import path

from .views import RendaListView, RendaCreateView
from .views import RendaUpdateView, RendaDeleteView


urlpatterns = [
	path('list/', RendaListView.as_view(), name='renda_list'),
	path('cad/', RendaCreateView.as_view(), name='renda_create'),
	path('<slug:slug>/', RendaUpdateView.as_view(), name='renda_update'),
	path('<slug:slug>/delete/', RendaDeleteView.as_view(), name='renda_delete'), 
]
 
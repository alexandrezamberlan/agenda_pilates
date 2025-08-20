from django.urls import path

from .views import ArtigoListView, ArtigoCreateView
from .views import ArtigoUpdateView, ArtigoDeleteView


urlpatterns = [
	path('list/', ArtigoListView.as_view(), name='artigo_list'),
	path('cad/', ArtigoCreateView.as_view(), name='artigo_create'),
	path('<slug:slug>/', ArtigoUpdateView.as_view(), name='artigo_update'),
	path('<slug:slug>/delete/', ArtigoDeleteView.as_view(), name='artigo_delete'), 
]
 
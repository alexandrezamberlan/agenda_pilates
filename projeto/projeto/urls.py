from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('paciente/', include('apppaciente.urls')), 
    path('agenda/', include('agenda.urls')),  
    path('artigo/', include('artigo.urls')), 
    path('aviso/', include('aviso.urls')), 
    path('profissao/', include('profissao.urls')), 
    path('exercicio/', include('exercicio.urls')), 
    path('instituicao/', include('instituicao.urls')), 
    path('usuario/', include('usuario.urls')), 
    path('renda/', include('renda.urls')),  
    path('treino/', include('treino.urls')),  
    path('accounts/', include('django.contrib.auth.urls')),
]

#url para arquivos de media quando em desenvolvimento
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, 
    document_root = settings.STATIC_ROOT)   

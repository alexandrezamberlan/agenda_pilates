from __future__ import unicode_literals

import os

from django.db import models
from django.dispatch import receiver
from django.urls import reverse

from utils.gerador_hash import gerar_hash

class ArtigoAtivoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Artigo(models.Model):
    titulo = models.CharField('Título *', unique=True, db_index=True, max_length=100, help_text='* Campo obrigatório')       
    texto = models.TextField('Texto *', help_text='* Campo obrigatório', blank=True, null=False)
    arquivo = models.FileField('Arquivo PDF de para avaliação (sem autores e identificação)', upload_to='midias', help_text='Utilize arquivo .PDF')
    data = models.DateField('Data *', auto_now_add=True, help_text='* Campo obrigatório')
    responsavel = models.ForeignKey('usuario.Usuario', verbose_name= 'Autor responsável pela submissão *', on_delete=models.PROTECT, related_name='responsavel')
      
    is_active = models.BooleanField('Ativo', default=True, help_text='Se ativo, a renda pode ser usada no sistema.')
    slug = models.SlugField('Hash',max_length= 200,null=True,blank=True)

    objects = models.Manager()
    rendas_ativas = ArtigoAtivoManager()

    class Meta:
        ordering            =   ['-is_active','titulo']
        verbose_name        =   'artigo'
        verbose_name_plural =   'artigos'

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):        
        if not self.slug:
            self.slug = gerar_hash()
 
        self.titulo = self.titulo.upper()
        super(Artigo, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('artigo_update', kwargs={'slug': self.slug})

    @property
    def get_delete_url(self):
        return reverse('artigo_delete', kwargs={'slug': self.slug})


#triggers para limpeza dos arquivos apagados ou alterados. No Django é chamado de signals
#deleta o arquivo fisico ao excluir o item midia
@receiver(models.signals.post_delete, sender=Artigo)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.arquivo:
        if os.path.isfile(instance.arquivo.path):
            os.remove(instance.arquivo.path)
    

#deleta o arquivo fisico ao alterar o arquivo do item midia
@receiver(models.signals.pre_save, sender=Artigo)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        obj = Artigo.objects.get(pk=instance.pk)
        if not obj.arquivo:
            return False
        old_file = obj.arquivo
        new_file = instance.arquivo
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    except Artigo.DoesNotExist:
        return False

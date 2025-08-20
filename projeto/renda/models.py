from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

from utils.gerador_hash import gerar_hash

class RendaAtivoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Renda(models.Model):       
    descricao = models.CharField('Descrição da renda *', unique=True, db_index=True, max_length=100, help_text='* Campo obrigatório')
    valor_salario_minimo = models.DecimalField('Valor do salário mínimo *', max_digits=10, decimal_places=2, default=0.00, null=True,blank=True, help_text='Valor do salário mínimo para essa Renda')          
    is_active = models.BooleanField('Ativo', default=True, help_text='Se ativo, a renda pode ser usada no sistema.')
    slug = models.SlugField('Hash',max_length= 200,null=True,blank=True)

    objects = models.Manager()
    rendas_ativas = RendaAtivoManager()

    class Meta:
        ordering            =   ['-is_active','descricao']
        verbose_name        =   'renda'
        verbose_name_plural =   'rendas'

    def __str__(self):
        return self.descricao

    def save(self, *args, **kwargs):        
        if not self.slug:
            self.slug = gerar_hash()
 
        self.descricao = self.descricao.upper()
        super(Renda, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('renda_update', kwargs={'slug': self.slug})

    @property
    def get_delete_url(self):
        return reverse('renda_delete', kwargs={'slug': self.slug})

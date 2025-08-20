from __future__ import unicode_literals

import os

from django.db import models
from django.dispatch import receiver
from django.urls import reverse

from utils.gerador_hash import gerar_hash

class ExercicioAtivoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Exercicio(models.Model):
    #1 campo da tupla fica no banco de dados
    #2 campo da tupla eh mostrado para o usuario
    INTENSIDDE = (
        ('25', '25%'),
        ('50', '50%' ),
        ('75', '75%' ),        
        ('100', '100%' ),        
    )
    descricao = models.CharField('Descrição do exercício *', unique=True, db_index=True, max_length=100, help_text='* Campo obrigatório')       
    tempo = models.IntegerField('Tempo de execução (em segundos) *', help_text='Procure manter o tempo entre 5 e 60 segundos.', default=10)   
    intensidade = models.CharField('Intensidade *', max_length=3, choices=INTENSIDDE, help_text='A intensidade do exercício', default='25')  
    video = models.URLField('Link do video', max_length=100, blank=True, null=True)
      
    is_active = models.BooleanField('Ativo', default=True, help_text='Se ativo, o exercício pode ser usado no sistema.')
    slug = models.SlugField('Hash',max_length= 200,null=True,blank=True)

    objects = models.Manager()
    exercicios_ativos = ExercicioAtivoManager()

    class Meta:
        ordering            =   ['-is_active','descricao']
        verbose_name        =   'exercicio'
        verbose_name_plural =   'exercicios'

    def __str__(self):
        return self.descricao

    def save(self, *args, **kwargs):        
        if not self.slug:
            self.slug = gerar_hash()
 
        self.descricao = self.descricao.upper()
        super(Exercicio, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('exercicio_update', kwargs={'slug': self.slug})

    @property
    def get_delete_url(self):
        return reverse('exercicio_delete', kwargs={'slug': self.slug})

    @property
    def get_animacao_url(self):
        return reverse('exercicio_animacao', kwargs={'slug': self.slug})


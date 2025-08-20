from __future__ import unicode_literals

import os

from django.db import models
from django.dispatch import receiver
from django.urls import reverse

from utils.gerador_hash import gerar_hash

from exercicio.models import Exercicio

class TreinoAtivoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class TreinoExecucao(models.Model):
    treino = models.ForeignKey('Treino', verbose_name='Treino *', on_delete=models.RESTRICT, help_text='* Campo obrigatório. Treino que foi realizado.', related_name='treino_executado')
    data_hora = models.DateTimeField('Data e horade execução *', auto_now=True)
    observacao = models.TextField('Alguma observação para o fisioterapeuta?', null=True, blank=True, help_text='Observações sobre a execução do treino.')

    class Meta:
        ordering = ['-data_hora']
        verbose_name = 'treino execução'
        verbose_name_plural = 'treinos execuções'

    def __str__(self):
        return f'Treino: {self.treino.descricao} - Data: {self.data_hora.strftime("%d/%m/%Y %H:%M:%S")}'
    
    def save(self, *args, **kwargs):        
        self.observacao = self.observacao.upper()
        super(TreinoExecucao, self).save(*args, **kwargs)


class Treino(models.Model):
    descricao = models.CharField('Descrição do treino *', unique=True, db_index=True, max_length=100, help_text='* Campo obrigatório. Tente expressar a ideia geral do treino.')           
    paciente = models.ForeignKey('usuario.Usuario', verbose_name='Paciente *', on_delete=models.RESTRICT, help_text='* Campo obrigatório. Paciente que receberá o treino.', related_name='paciente')
    fisioterapeuta = models.ForeignKey('usuario.Usuario', verbose_name='Fisioterapeuta *', on_delete=models.RESTRICT, help_text='* Campo obrigatório. Fisioterapeuta que prescreveu o treino.', related_name='fisioterapeuta')
    exercicios = models.ManyToManyField('exercicio.Exercicio', verbose_name='Exercícios *', help_text='* Campo obrigatório. Exercícios que compõem o treino.', related_name='exercicios')
    pausas = models.IntegerField('Pausas em segundos', null=True, blank=False, help_text='Pausas entre os exercícios. O valor deve ser em segundos. Se não for preenchido, o treino será realizado sem pausas entre os exercícios.', default=0)
    data_inicio = models.DateField('Data de início', null=True, blank=True, help_text='Data de início do treino.')
    data_fim = models.DateField('Data de término', null=True, blank=True, help_text='Data de término do treino.')
    realizado = models.BooleanField('Realizado', default=False, help_text='Se o treino foi realizado pelo paciente.')
    quantidade_repeticoes = models.IntegerField('Quantidade de repetições', null=True, blank=False, default=1, help_text='Quantidade de repetições de cada exercício no treino. No mínimo, deve ser 1. Se não for preenchido, o treino será realizado apenas uma vez.')  
    quantidade_vezes_periodo = models.IntegerField('Quantidade de vezes o treino deve ser realizado no período', null=True, blank=False, default=1, help_text='Vezes que o treino deve ser realizado no período entre a data de início e a data de término. Se não for preenchido, o treino será realizado apenas uma vez.')  
      
    is_active = models.BooleanField('Ativo', default=True, help_text='Se ativo, o exercício pode ser usado no sistema.')
    slug = models.SlugField('Hash',max_length= 200,null=True,blank=True)

    objects = models.Manager()
    treinos_ativos = TreinoAtivoManager()
    

    class Meta:
        ordering            =   ['-is_active','descricao']
        verbose_name        =   'treino'
        verbose_name_plural =   'treinos'

    def __str__(self):
        return self.descricao

    def save(self, *args, **kwargs):        
        if not self.slug:
            self.slug = gerar_hash()
 
        self.descricao = self.descricao.upper()
        super(Treino, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('treino_update', kwargs={'slug': self.slug})

    @property
    def get_delete_url(self):
        return reverse('treino_delete', kwargs={'slug': self.slug})

    @property
    def get_meu_absolute_url(self):
        return reverse('treino_meu_update', kwargs={'slug': self.slug})

    @property
    def get_meu_delete_url(self):
        return reverse('treino_meu_delete', kwargs={'slug': self.slug})
    
    @property
    def get_treino_execucao_create_url(self):
        return reverse('apppaciente_treino_execucao_create', kwargs={'treino_slug': self.slug})
    
    @property
    def get_observacoes_treino_url(self):
        return reverse('apppaciente_treino_observacoes', kwargs={'treino_slug': self.slug})

    @property
    def qtd_desse_treino_realizado(self):        
        quantidade = TreinoExecucao.objects.filter(treino=self, treino__paciente=self.paciente).count()
        return quantidade
    
    @property
    def meta_treino_atingida(self):
        quantidade = TreinoExecucao.objects.filter(treino=self, treino__paciente=self.paciente).count()
        
        return quantidade >= self.quantidade_vezes_periodo
    
    @property
    def observacoes_treino(self):
        return TreinoExecucao.objects.filter(treino=self).exclude(observacao__isnull=True).exclude(observacao__exact='').count()
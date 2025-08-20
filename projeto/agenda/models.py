from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

from utils.gerador_hash import gerar_hash


class AgendaAtivaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Agenda(models.Model):
    paciente = models.ForeignKey('usuario.Usuario', verbose_name='Paciente *', on_delete=models.RESTRICT, help_text='* Campo obrigatório. Paciente na consulta ou agenda.', related_name='paciente_agenda')
    fisioterapeuta = models.ForeignKey('usuario.Usuario', verbose_name='Fisioterapeuta *', on_delete=models.RESTRICT, help_text='* Campo obrigatório. Fisioterapeuta no atendimento.', related_name='fisioterapeuta_agenda')
    data = models.DateField('Data consulta', help_text='Data consulta. Use o formato dd/mm/aaaa.')    
    hora = models.TimeField('Hora consulta', help_text='Hora consulta. Use o formato hh:mm.')
    comentarios = models.TextField('Comentários', max_length=2000, help_text='Comentários sobre a consulta.', blank=True, null=True)
    realizado = models.BooleanField('Realizado', default=False, help_text='Se a consulta foi realizada.')
      
    is_active = models.BooleanField('Ativo', default=True, help_text='Se ativo, a consulta encontrará na agenda do paciente.')
    slug = models.SlugField('Hash',max_length= 200,null=True,blank=True)

    objects = models.Manager()
    agendas_ativas = AgendaAtivaManager()

    class Meta:
        ordering            =   ['-is_active','-data','-hora']
        unique_together     =   ('paciente', 'fisioterapeuta', 'data', 'hora')
        verbose_name        =   'agenda'
        verbose_name_plural =   'agendas'

    def __str__(self):
        return '%s com %s. %s - %s' % (self.paciente.nome, self.fisioterapeuta.nome, self.data.strftime('%d/%m/%Y'), self.hora.strftime('%H:%M'))

    def save(self, *args, **kwargs):        
        if not self.slug:
            self.slug = gerar_hash()
        super(Agenda, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('agenda_update', kwargs={'slug': self.slug})

    @property
    def get_delete_url(self):
        return reverse('agenda_delete', kwargs={'slug': self.slug})

    @property
    def get_minha_absolute_url(self):
        return reverse('agenda_minha_update', kwargs={'slug': self.slug})

    @property
    def get_minha_delete_url(self):
        return reverse('agenda_minha_delete', kwargs={'slug': self.slug})


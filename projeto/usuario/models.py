from __future__ import unicode_literals

from datetime import datetime
from django.utils import timezone

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models
from django.db.models import Q
from django.urls import reverse

from utils.gerador_hash import gerar_hash

from agenda.models import Agenda
from treino.models import Treino


class AdministradorAtivoManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(tipo='ADMINISTRADOR', is_active=True)


class FisioterapeutaAtivoManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(Q(tipo='FISIOTERAPEUTA') | Q(tipo='ADMINISTRADOR'), is_active=True)
    

class PacienteAtivoManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(tipo='PACIENTE', is_active=True)


class UsuarioAtivoManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    
class PacienteAtivoManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(tipo='PACIENTE', is_active=True)


class Usuario(AbstractBaseUser):
    #1 campo da tupla fica no banco de dados
    #2 campo da tupla eh mostrado para o usuario
    TIPOS_USUARIOS = (
        ('ADMINISTRADOR', 'Administrador'),
        ('FISIOTERAPEUTA', 'Fisioterapeuta' ),
        ('SECRETARIA', 'Secretária' ),
        ('PACIENTE', 'Paciente' ),        
    )
    
    SEXO = (
        ('FEMININO', 'Feminino'),
        ('MASCULINO', 'Masculino' ),
        ('NÃO DESEJA INFORMAR', 'Não deseja informar' ),
    )
    
    ESCOLARIDADE = (
        ('NÃO ALFABETIZADO', 'Não alfabetizado'),
        ('ENSINO FUNDAMENTAL INCOMPLETO', 'Ensino Fundamental incompleto'),
        ('ENSINO FUNDAMENTAL COMPLETO', 'Ensino Fundamental completo'),
        ('ENSINO MÉDIO INCOMPLETO', 'Ensino Médio incompleto'),
        ('ENSINO MÉDIO COMPLETO', 'Ensino Médio completo'),
        ('ENSINO SUPERIOR INCOMPLETO', 'Ensino Superior incompleto'),
        ('ENSINO SUPERIOR COMPLETO', 'Ensino Superior completo'),
        ('PÓS GRADUAÇÃO', 'Pós Graduação'),
        ('MESTRADO', 'Mestrado'),
        ('DOUTORADO', 'Doutorado'),
    )
    
    POSSUI_FILHOS = (
        ('SIM COM ATENÇÃO', 'Sim, tem filhos que demandam atenção'),   
        ('SIM SEM ATENÇÃO', 'Sim, tem filhos mas que NÃO demandam atenção'),
        ('NÃO POSSUI', 'Não tem filhos'),
    )
    
    JORNADA_TRABALHO = (
        ('NENHUMA', 'Não está trabalhando atualmente'),
        ('ATE 10 HORAS', 'Até 10 horas'),
        ('DE 11 A 20 HORAS', 'De 11 a 20 horas'),
        ('DE 21 A 30 HORAS', 'De 21 a 30 horas'),
        ('DE 31 A 40 HORAS', 'De 31 a 40 horas'),
        ('MAIS DE 40 HORAS', 'Mais de 40 horas'),
    )
    
    USERNAME_FIELD = 'email'

    tipo = models.CharField('Tipo do usuário *', max_length=15, choices=TIPOS_USUARIOS, default='PACIENTE', help_text='* Campos obrigatórios')
    nome = models.CharField('Nome completo *', max_length=100)
    sexo = models.CharField('Sexo *', max_length=20, choices=SEXO, help_text='* Campos obrigatórios')
    data_nascimento = models.DateField('Data de nascimento *', help_text='Use o formato dd/mm/aaaa', null=True, blank=True)   
    profissao = models.ForeignKey('profissao.Profissao', verbose_name= 'Profissão do usuário', on_delete=models.PROTECT, related_name='profissao', null=True, blank=True)     
    instituicao = models.ForeignKey('instituicao.Instituicao', verbose_name= 'Clínica do usuário (profissional ou paciente)', on_delete=models.PROTECT, related_name='instituicao', null=True, blank=True)     
    email = models.EmailField('Email', unique=True, max_length=100, db_index=True)
    celular = models.CharField('Número celular com DDD *', max_length=14, help_text="Use DDD, por exemplo 55987619832")
    cpf = models.CharField('CPF *', max_length=14, help_text='ATENÇÃO: Somente os NÚMEROS')    
    aceita_termo = models.BooleanField('Marque o aceite do termo de consentimento', default=False, help_text='Se marcado, usuário tem consentimento de uso do sistema')
    
    #Atualização de escolaridade, renda, filhos e trabalho.
    escolaridade = models.CharField('Escolaridade *', max_length=30, choices=ESCOLARIDADE, null=True, blank=True, help_text='* Campos obrigatórios')
    renda = models.ForeignKey('renda.Renda', verbose_name= 'Renda do usuário', on_delete=models.PROTECT, related_name='renda', null=True, blank=True)
    possui_filhos = models.CharField('Possui filhos *', max_length=15, choices=POSSUI_FILHOS, null=True, blank=True, help_text='* Campos obrigatórios')
    jornada_trabalho = models.CharField('Jornada de trabalho *', max_length=20, choices=JORNADA_TRABALHO, null=True, blank=True, help_text='* Campos obrigatórios')
    
    is_active = models.BooleanField('Ativo', default=False, help_text='Se ativo, o usuário tem permissão para acessar o sistema')
    slug = models.SlugField('Hash',max_length= 200,null=True,blank=True)

    objects = UserManager()
    administradores = AdministradorAtivoManager()
    fisioterapeutas = FisioterapeutaAtivoManager()
    pacientes = PacienteAtivoManager()
    usuarios_ativos = UsuarioAtivoManager()
    pacientes_ativos = PacienteAtivoManager()


    class Meta:
        ordering            =   ['-tipo','nome']
        verbose_name        =   ('usuário')
        verbose_name_plural =   ('usuários')

    def __str__(self):
        return '%s | %s' % (self.nome, self.celular)

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()
        self.nome = self.nome.upper()
        self.email = self.email.lower()
        if not self.id:
            self.set_password(self.password) #criptografa a senha digitada no forms
        super(Usuario, self).save(*args, **kwargs)

    def get_id(self):
        return self.id

    @property
    def get_primeiro_nome(self):
        lista = self.nome.split(" ")
        return lista[0]

    @property
    def get_sobrenome(self):
        lista = self.nome.split(" ")
        return lista[-1]

    @property
    def is_staff(self):
        if self.tipo == 'ADMINISTRADOR':
            return True
        return False

    @property
    def get_absolute_url(self):
        return reverse('usuario_update', kwargs={'slug': self.slug})
    
    @property
    def get_paciente_absolute_url(self):
        return reverse('usuario_paciente_update', kwargs={'slug': self.slug})

    @property
    def get_delete_url(self):
        return reverse('usuario_delete', kwargs={'slug': self.slug})

    @property
    def get_usuario_register_activate_url(self):
        return '%s%s' % (settings.DOMINIO_URL, reverse('usuario_register_activate', kwargs={'slug': self.slug}))

    @property
    def qtd_agendas_hoje(self):
        data_atual = timezone.now().date()
        return Agenda.objects.filter(fisioterapeuta=self, data=data_atual).count()
    
    @property
    def qtd_agendas_amanha(self):
        data_amanha = timezone.now().date() + timezone.timedelta(days=1)
        return Agenda.objects.filter(fisioterapeuta=self, data=data_amanha).count()

    @property
    def qtd_agendas_realizadas(self):
        return Agenda.objects.filter(fisioterapeuta=self, realizado=True).count()
    
    @property
    def qtd_agendas_canceladas(self):
        data_atual = timezone.now().date()
        return Agenda.objects.filter(fisioterapeuta=self, realizado=False, data__lte=data_atual).count()
    
    @property
    def minhas_consultas_realizadas(self):
        return Agenda.objects.filter(paciente=self, realizado=True).order_by('-data', '-hora').count()
    
    @property
    def minhas_consultas_amanha(self):
        data_amanha = timezone.now().date() + timezone.timedelta(days=1)
        return Agenda.objects.filter(paciente=self, data=data_amanha).count()
    
    @property
    def minhas_consultas_futuras(self):
        data_atual = timezone.now().date()
        return Agenda.objects.filter(paciente=self, realizado=False, data__gte=data_atual).order_by('data', 'hora').count()
    
    @property
    def meus_treinos_disponiveis(self):
        return Treino.objects.filter(paciente=self).count()
    
    @property
    def meus_treinos_realizados(self):
        return Treino.objects.filter(paciente=self, realizado=True).count()
    
    @property
    def meus_treinos_em_atraso(self):
        return Treino.objects.filter(paciente=self, realizado=False, data_inicio__lt=datetime.now()).count()
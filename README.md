# Agenda Pilates - AGEPIL

Projeto de alunos voluntários do Laboratório de Práticas para gestão de agendas em clínica de Pilates

PENDENCIAS
    - 
    -
    -

- apps
    - profissoa usuario
        - descrição
        - is_active
        - slug

    - renda
        - descricao
        - valor_salario_minimo
        - is_active
        - slug
            - depois de feito o app, cadastrar no banco de dados
                Sem renda
                Até 0,5 salário mínimo 
                De 0,5 a 1 salário mínimo 
                De 1 a 2 salários mínimos 
                De 2 a 3 salários mínimos 
                De 3 a 5 salários mínimos 
                De 5 a 10 salários mínimos 
                Acima de 10 salários mínimos 
                Prefere não informar

    - usuario
        - tipos: administrador, fisioterapeuta, paciente vinculo com tipo usuário
        - nome
        - email (chave primária)
        - celular
        - cpf
        - data_nascimento
        - instituição vinculo com instituição
        - is_active
        - slug
        - escolaridade (null=True, blank=False)
            Não Alfabetizado
            Ensino Fundamental Incompleto
            Ensino Fundamental Completo
            Ensino Médio Incompleto
            Ensino Médio Completo
            Ensino Superior Incompleto
            Ensino Superior Completo
            Pós-graduação Completa
            Mestrado Completo
            Doutorado Completo
        - renda vinculo com renda (null=True, blank=False)
        - possui filhos? (null=True, blank=False)
            Sim, tenho filhos que demandam minha atenção
            Não, não tenho filhos que demandam minha atenção
            Não tenho filhos
        - jornada de trabalho semanal (null=True, blank=False)
            Até 10 horas semanais
            De 11 a 20 horas semanais
            De 21 a 30 horas semanais
            De 31 a 40 horas semanais
            De 41 a 44 horas semanais
            Mais de 44 horas semanais
            Não estou trabalhando atualmente

    -  instituição/clinica
        - nome
        - sigla (opcional)
        - cidade
        - estado
        - país
        - is_active
        - slug

    (RETIRAR) - artigo
        - titulo
        - texto
        - arquivo
        - data
        - is_active
        - slug
        - usuario que carregou, mas com visualização do administrador/coordenador

    - profissao
        - descricao
        - is_active
        - slug

    (RETIRAR)- exercicio
        - descricao
        - tempo - segundos
        - intensidade - % de 50 a 100 (50, 75, 100)
        - video - 
        - is_active
        - slug
        
    (RETIRAR)- treino
        - descricao
        - paciente
        - fisioterapeuta
        - exercicios vinculo com exercicio
        - pausas
        - realizado
        - cronograma de treino (período; dataInicio a dataFim + vezes a fazer)

    - agenda
        - paciente vinculo com usuario do tipo paciente
        - fisio vinculo com usuario do tipo fisio
        - data
        - hora
 
Sugestões de CSS
    - https://bootsnipp.com/snippets/eNe4v
    - https://adminlte.io/themes/AdminLTE/index2.html
    - https://bootswatch.com/3/

Icons bootstrap - https://www.w3schools.com/icons/bootstrap_icons_glyphicons.asp




# .env

SECRET_KEY='=%6aqk0p^aux0qvolqn_7efyj(@wh*wtc_!n10u8_o4!l#k6)h'
DEBUG=True 
STATIC_URL=/static/

DOMINIO_URL='http://localhost:8000'

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587

EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_USE_STARTTLS = False

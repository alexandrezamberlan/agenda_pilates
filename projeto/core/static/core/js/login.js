// Script para a página de login
$(document).ready(function() {
    // Aplicar foco no primeiro campo
    $('#id_username').focus();
    
    // Adicionar classes Bootstrap aos campos do formulário
    $('.form-control').addClass('form-control');
    
    // Efeito visual nos campos de input
    $('.form-control').on('focus', function() {
        $(this).parent().addClass('has-focus');
    });
    
    $('.form-control').on('blur', function() {
        $(this).parent().removeClass('has-focus');
    });
    
    // Validação básica do formulário
    $('#loginForm').on('submit', function(e) {
        var username = $('#id_username').val();
        var password = $('#id_password').val();
        
        if (!username || !password) {
            e.preventDefault();
            alert('Por favor, preencha todos os campos obrigatórios.');
            return false;
        }
    });
}); 
document.addEventListener('DOMContentLoaded', function() {
    // Ajustar a altura da tabela para ocupar toda a tela
    var tableContainer = document.querySelector('.lojas-container');
    var windowHeight = window.innerHeight;
    tableContainer.style.height = windowHeight + 'px';

    // Adicionar o evento de rolagem para ocultar a barra de endereço
    tableContainer.addEventListener('scroll', function() {
        window.scrollTo(0, 1);
    });

    // Adicionar o evento de clique no link de perfil
    var profileLink = document.getElementById('profile-link');
    
    profileLink.addEventListener('click', function(event) {
        // Verificar se o usuário está conectado usando o atributo personalizado
        var isLoggedIn = profileLink.getAttribute('data-logged-in') === 'true';
        
        // Se o usuário não estiver conectado, a navegação padrão ocorrerá
        if (!isLoggedIn) {
            return;
        }
        
        // Prevenir o comportamento padrão do link
        event.preventDefault();
        
        // Se o usuário estiver conectado, exibir o menu suspenso
        var dropdownContent = document.querySelector('.dropdown-content');
        dropdownContent.style.display = 'block';
    });
});

// Código JavaScript para ocultar a barra de ferramentas e a barra de URL ao rolar a tabela
function hideAddressBar() {
    // Solicita ao navegador que role a página para o topo
    window.scrollTo(0, 1);
}



document.addEventListener('DOMContentLoaded', function() {
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





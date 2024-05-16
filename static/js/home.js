var hamburger = document.querySelector(".Hamburger");
var container = document.querySelector(".container");
var sidebar = document.querySelector(".Sidebar");

// Função para abrir o menu hamburguer
hamburger.addEventListener("click", function(){
    container.classList.toggle("show-menu");
});



// Função para fechar o menu ao clicar fora
document.addEventListener("click", function(event) {
    if (container.classList.contains("show-menu")) {
        if (!hamburger.contains(event.target) && !sidebar.contains(event.target)) {
            console.log("Clique fora do Sidebar");
            container.classList.remove("show-menu");                  
        }
    }
  });

//Função para abrir o menu suspensso para o perfil
document.addEventListener('DOMContentLoaded', function() {
    var profileLink = document.getElementById('profile-link');
    var dropdownContent = document.querySelector('.dropdown-content');
    
    profileLink.addEventListener('click', function(event) {
        // Verificar se o usuário está conectado usando o atributo personalizado
        var isLoggedIn = profileLink.getAttribute('data-logged-in') === 'true';
        
        // Se o usuário não estiver conectado, a navegação padrão ocorrerá
        if (!isLoggedIn) {
            return;
        }
        
        // Prevenir o comportamento padrão do link
        event.preventDefault();
        
        // Exibir o menu suspenso
        dropdownContent.style.display = 'block';
    });
    
    // Adicionar um ouvinte de eventos de clique ao documento inteiro
    document.addEventListener('click', function(event) {
        // Verificar se o clique ocorreu dentro do menu suspenso ou no link de perfil
        var isClickInsideProfileLink = event.target === profileLink || profileLink.contains(event.target);
        var isClickInsideDropdownContent = event.target === dropdownContent || dropdownContent.contains(event.target);
        
        // Se o clique ocorreu fora do menu suspenso e do link de perfil, feche o menu
        if (!isClickInsideDropdownContent && !isClickInsideProfileLink) {
            dropdownContent.style.display = 'none';
        }
    });
});
        


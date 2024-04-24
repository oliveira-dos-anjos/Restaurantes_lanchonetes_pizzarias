document.addEventListener('DOMContentLoaded', function() {
    var tableContainer = document.getElementById('lojas-container');
    var windowHeight = window.innerHeight;
    tableContainer.style.height = windowHeight + 'px';

    var lastScrollTop = 0;
    tableContainer.addEventListener('scroll', function() {
        var st = tableContainer.scrollTop;

        if (st > lastScrollTop) {
            // Rolar para baixo
            exitFullscreen();
        } else {
            // Rolar para cima
            enterFullscreen();
        }

        lastScrollTop = st <= 0 ? 0 : st;
    });

    function enterFullscreen() {
        if (!document.fullscreenElement) {
            try {
                tableContainer.requestFullscreen();
            } catch (error) {
                console.error('Erro ao tentar entrar em tela cheia:', error);
            }
        }
    }

    function exitFullscreen() {
        if (document.fullscreenElement) {
            try {
                document.exitFullscreen();
            } catch (error) {
                console.error('Erro ao tentar sair da tela cheia:', error);
            }
        }
    }

    var profileLink = document.getElementById('profile-link');
    profileLink.addEventListener('click', function(event) {
        var isLoggedIn = profileLink.getAttribute('data-logged-in') === 'true';
        if (!isLoggedIn) {
            return;
        }
        event.preventDefault();
        var dropdownContent = document.querySelector('.dropdown-content');
        dropdownContent.style.display = 'block';
    });
});

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
        
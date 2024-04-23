document.addEventListener('DOMContentLoaded', function() {
    var tableContainer = document.querySelector('.lojas-container');
    var windowHeight = window.innerHeight;
    tableContainer.style.height = windowHeight + 'px';

    tableContainer.addEventListener('scroll', function() {
        if (document.fullscreenElement === null) { // Verifica se já está em tela cheia
            try {
                // Tenta entrar no modo de tela cheia
                tableContainer.requestFullscreen();
            } catch (error) {
                console.error('Erro ao tentar entrar em tela cheia:', error);
            }
        }
    });

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


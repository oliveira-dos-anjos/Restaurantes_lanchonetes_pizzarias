document.addEventListener("DOMContentLoaded", function() {
    var mainContent = document.getElementById('main-content');
    var lastScrollTop = 0;
    var userPrompted = false;

    // Função para entrar em tela cheia
    function enterFullScreen() {
        if (document.documentElement.requestFullscreen) {
            document.documentElement.requestFullscreen();
        } else if (document.documentElement.mozRequestFullScreen) {  
            document.documentElement.mozRequestFullScreen();  
        } else if (document.documentElement.webkitRequestFullscreen) {  
            document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);  
        } else if (document.documentElement.msRequestFullscreen) {  
            document.documentElement.msRequestFullscreen();  
        }
    }

    // Função para sair de tela cheia
    function exitFullScreen() {
        if (document.fullScreenElement || document.mozFullScreen || document.webkitIsFullScreen) {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.mozCancelFullScreen) {
                document.mozCancelFullScreen();
            } else if (document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            } else if (document.msExitFullscreen) {
                document.msExitFullscreen();
            }
        }
    }

    if (mainContent) {
        mainContent.addEventListener('scroll', function() {
            var scrollTop = mainContent.scrollTop;

            if (scrollTop > lastScrollTop && !userPrompted) {
                userPrompted = true;
                // Solicita permissão ao usuário
                var confirmFullScreen = confirm("Você gostaria de entrar em tela cheia?");
                if (confirmFullScreen) {
                    enterFullScreen();
                }
            } else if (scrollTop <= lastScrollTop && userPrompted) {
                exitFullScreen();
            }

            lastScrollTop = scrollTop;
        });
    } else {
        console.error('Elemento main-content não encontrado.');
    }
});



document.addEventListener("DOMContentLoaded", function() {
    // Função para ajustar a altura do main-content
    function setMainContentHeight() {
        var mainContent = document.getElementById('main-content');
        if (mainContent) {
            // Define a altura do main-content igual à altura da janela
            mainContent.style.height = (window.innerHeight - 50) + 'px';
        } else {
            console.error('Elemento main-content não encontrado.');
        }
    }

    // Define a altura inicial
    setMainContentHeight();

    // Ajusta a altura quando a janela é redimensionada
    window.addEventListener('resize', setMainContentHeight);
});

document.querySelectorAll('.loja-item').forEach(item => {
    item.addEventListener('click', function(event) {
        // Obtém o nome da loja a partir do elemento HTML
        const storeName = this.querySelector('h3').textContent;

        selectStore(event, storeName);
    });
});

// Função para guardar as informações da loja para abrir o perfil da mesma
function selectStore(event, storeName) {
    event.preventDefault();

    // Crie um formulário para enviar os dados para o servidor
    let form = document.createElement('form');
    form.method = 'POST';
    form.action = '/profile';

    try {
        // Adicione campos ocultos ao formulário com os dados da loja
        let nameField = document.createElement('input');
        nameField.type = 'hidden';
        nameField.name = 'store_name';
        nameField.value = storeName;

        form.appendChild(nameField);

        // Adicione o formulário ao corpo do documento e envie-o
        document.body.appendChild(form);
        form.submit();
    } catch (error) {
        console.log('Erro capturado:', error.message);
    }
}



document.addEventListener("DOMContentLoaded", function() {
    // Seleciona o elemento com a classe 'lojas-container'
    const target = document.querySelector('.lojas-container');

    // Verifica se o elemento existe
    if (target) {
        function animeNavBar() {
            console.log("rolando");

            // Verifica se o documento está em modo de tela cheia
            if (document.fullscreenElement || document.mozFullScreenElement || document.webkitFullscreenElement || document.msFullscreenElement) {
                console.log("Saindo do modo de tela cheia");

                // Sair do modo de tela cheia
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                } else if (document.mozCancelFullScreen) { // Para Firefox
                    document.mozCancelFullScreen();
                } else if (document.webkitExitFullscreen) { // Para Chrome, Safari e Opera
                    document.webkitExitFullscreen();
                } else if (document.msExitFullscreen) { // Para IE/Edge
                    document.msExitFullscreen();
                }
            } else {
                console.log("Entrando em modo de tela cheia");

                // Entrar no modo de tela cheia
                const elem = document.documentElement; // ou use um elemento específico, por exemplo, target
                if (elem.requestFullscreen) {
                    elem.requestFullscreen();
                } else if (elem.mozRequestFullScreen) { // Para Firefox
                    elem.mozRequestFullScreen();
                } else if (elem.webkitRequestFullscreen) { // Para Chrome, Safari e Opera
                    elem.webkitRequestFullscreen();
                } else if (elem.msRequestFullscreen) { // Para IE/Edge
                    elem.msRequestFullscreen();
                }
            }
        }

        // Adiciona o ouvinte de evento de rolagem ao window
        window.addEventListener('scroll', function() {
            animeNavBar();
        });

    } else {
        console.log("Elemento 'lojas-container' não encontrado.");
    }
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

    console.log("aqui veio");

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


document.addEventListener("DOMContentLoaded", function() {
    // Seleciona a div main-content
    var mainContent = document.getElementById('main-content');

    // Variável para armazenar a posição de rolagem anterior
    var lastScrollTop = 0;

    // Adiciona o ouvinte de rolagem
    mainContent.addEventListener('scroll', function() {
        // Pega a posição de rolagem atual
        var scrollTop = mainContent.scrollTop;

        // Compara a posição atual com a posição anterior
        if (scrollTop > lastScrollTop) {
            console.log('Rolou para baixo');
            // Ação para rolar para baixo
        } else {
            console.log('Rolou para cima');
            // Ação para rolar para cima
        }

        // Atualiza a posição de rolagem anterior
        lastScrollTop = scrollTop;
    });
});

document.addEventListener("DOMContentLoaded", function() {
    // Função para ajustar a altura do main-content
    function setMainContentHeight() {
        var mainContent = document.getElementById('main-content');
        if (mainContent) {
            // Define a altura do main-content igual à altura da janela
            mainContent.style.height = (window.innerHeight - 0) + 'px';
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



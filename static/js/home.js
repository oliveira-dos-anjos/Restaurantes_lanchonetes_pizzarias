var hamburger = document.querySelector(".Hamburger");
var container = document.querySelector(".container");
var sidebar = document.querySelector(".Sidebar");

// Função para abrir o menu hamburguer
hamburger.addEventListener("click", function(){
    container.classList.toggle("show-menu");
    const lojasContainer = document.querySelector('.lojas-container');
    lojasContainer.classList.add('disabled-click');
});



// Função para fechar o menu ao clicar fora
document.addEventListener("click", function(event) {
    if (container.classList.contains("show-menu")) {
        if (!hamburger.contains(event.target) && !sidebar.contains(event.target)) {
            console.log("Clique fora do Sidebar");
            container.classList.remove("show-menu");
            const lojasContainer = document.querySelector('.lojas-container');
            lojasContainer.classList.remove('disabled-click');                 
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
        console.log("clicado")
        const lojasContainer = document.querySelector('.lojas-container');
        lojasContainer.classList.add('disabled-click');

    });
    
    // Adicionar um ouvinte de eventos de clique ao documento inteiro
    document.addEventListener('click', function(event) {
        // Verificar se o clique ocorreu dentro do menu suspenso ou no link de perfil
        var isClickInsideProfileLink = event.target === profileLink || profileLink.contains(event.target);
        var isClickInsideDropdownContent = event.target === dropdownContent || dropdownContent.contains(event.target);
        
        // Se o clique ocorreu fora do menu suspenso e do link de perfil, feche o menu
        if (!isClickInsideDropdownContent && !isClickInsideProfileLink) {
            dropdownContent.style.display = 'none';
            const lojasContainer = document.querySelector('.lojas-container');
            lojasContainer.classList.remove("disabled-click")
        }
    });
});
        



// Adiciona o ouvinte de evento de rolagem ao container
container.addEventListener('scroll', function() {
  var deslocamentoY = container.scrollTop;
  var alturaContainer = container.clientHeight;
  var alturaDocumento = document.documentElement.scrollHeight;

  // Verifica se o container foi rolado o suficiente para esconder a barra de navegação
  toggleNavigationBar(deslocamentoY > alturaContainer);
  console.log("rolando")
});

// Adiciona o ouvinte de evento de rolagem à página inteira
document.addEventListener("scroll", function() {
  var deslocamentoY = window.scrollY;
  console.log("rolando")
  var alturaJanela = window.innerHeight;

  // Verifica se a página foi rolada o suficiente para esconder a barra de navegação
  toggleNavigationBar(deslocamentoY > alturaJanela);
  console.log("rolando")
});

//Função para guardar as informacoes da loja para abrir o perfil da mesma
function selectStore(event, storeName, storeDetails, openingHours, imagePath) {
    event.preventDefault();

    // Crie um formulário para enviar os dados para o servidor
    let form = document.createElement('form');
    form.method = 'POST';
    form.action = '/profile';

    // Adicione campos ocultos ao formulário com os dados da loja
    let nameField = document.createElement('input');
    nameField.type = 'hidden';
    nameField.name = 'store_name';
    nameField.value = storeName;

    let detailsField = document.createElement('input');
    detailsField.type = 'hidden';
    detailsField.name = 'store_details';
    detailsField.value = storeDetails;

    let hoursField = document.createElement('input');
    hoursField.type = 'hidden';
    hoursField.name = 'opening_hours';
    hoursField.value = openingHours;

    let imageField = document.createElement('input');
    imageField.type = 'hidden';
    imageField.name = 'image_path';
    imageField.value = imagePath;

    form.appendChild(nameField);
    form.appendChild(detailsField);
    form.appendChild(hoursField);
    form.appendChild(imageField);
    
    // Adicione o formulário ao corpo do documento e envie-o
    document.body.appendChild(form);
    form.submit();
}




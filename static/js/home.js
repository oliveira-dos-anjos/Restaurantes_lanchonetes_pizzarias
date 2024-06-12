// Adiciona o ouvinte de evento de rolagem ao lojasContainer
const target = document.querySelector('lojas-Container');

function animeNavBar(){
    console.log("rolando")
    console.log('para baixo')
    document.webkitExitFullscreen();
}

window.addEventListener('scroll', function(){
    animeNavBar();
})


  animeNavBar();
// Adiciona o ouvinte de evento de rolagem ao lojasContainer
const target = document.querySelector('lojas-Container');

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
        const elem = document.documentElement; // ou use um elemento específico, por exemplo, lojasContainer
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

window.addEventListener('scroll', function(){
    animeNavBar();
})


  


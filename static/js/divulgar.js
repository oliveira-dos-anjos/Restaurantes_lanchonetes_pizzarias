function previewImage(event) {
    const input = event.target;
    if (input.files && input.files[0]) {
        const reader = new FileReader();

        reader.onload = function(e) {
            const preview = document.getElementById('preview-image');
            preview.src = e.target.result;
        }

        reader.readAsDataURL(input.files[0]); 
    }
}


// Atualiza o valor exibido para o horário de encerramento
const closingTime = document.getElementById('closing-time');
const closingTimeValue= document.getElementById('closing-time-value');

closingTime.addEventListener('input', function() {
    closingTimeValue.textContent = this.value;
});

document.addEventListener('DOMContentLoaded', () => {
    const minDeliveryTimeInput = document.getElementById('min-delivery-time');
    const minDeliveryValueSpan = document.getElementById('min-delivery-value');
    const maxDeliveryTimeInput = document.getElementById('max-delivery-time');
    const maxDeliveryValueSpan = document.getElementById('max-delivery-value');

    minDeliveryTimeInput.addEventListener('input', () => {
        minDeliveryValueSpan.textContent = minDeliveryTimeInput.value;
    });

    maxDeliveryTimeInput.addEventListener('input', () => {
        maxDeliveryValueSpan.textContent = maxDeliveryTimeInput.value;
    });

    // Inicializa os valores com 00:00
    minDeliveryValueSpan.textContent = minDeliveryTimeInput.value;
    maxDeliveryValueSpan.textContent = maxDeliveryTimeInput.value;
});


// Atualiza o valor exibido para o tempo mínimo de entrega
const minDeliveryTime = document.getElementById('min-delivery-time');
const minDeliveryValue = document.getElementById('min-delivery-value');

minDeliveryTime.addEventListener('input', function() {
    minDeliveryValue.textContent = this.value;
});

// Atualiza o valor exibido para o tempo máximo de entrega
const maxDeliveryTime = document.getElementById('max-delivery-time');
const maxDeliveryValue = document.getElementById('max-delivery-value');

maxDeliveryTime.addEventListener('input', function() {
    maxDeliveryValue.textContent = this.value;
});


document.addEventListener("DOMContentLoaded", function() {
    var imageDiv = document.querySelector('.image-upload');  // Seleciona a div que contém a imagem
    var previewImage = imageDiv.querySelector('img');        // Seleciona a tag <img> dentro da div
    var imageSrcInput = document.getElementById('image-src'); // Campo oculto para armazenar os dados da imagem
    var storeNameInput = document.getElementById('store-name'); // Campo para o nome da loja

    // Evento quando a imagem é alterada
    imageDiv.addEventListener('change', function(event) {
        var file = event.target.files[0];
        var reader = new FileReader();

        reader.onload = function(e) {
            previewImage.src = e.target.result;
            imageSrcInput.value = e.target.result; // Define o valor do campo oculto como base64 da imagem
        };

        if (file) {
            reader.readAsDataURL(file); // Lê o arquivo como base64
        }
    });
});
''

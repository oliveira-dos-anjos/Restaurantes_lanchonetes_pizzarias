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

// Adiciona um evento de escuta para o input de arquivo
const uploadInput = document.getElementById('upload');
uploadInput.addEventListener('change', previewImage);

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
    var imageUpload = document.querySelector('.image-upload');
    var previewImage = imageUpload.querySelector('img');
    var imageSrcInput = document.getElementById('image-src'); 

    imageUpload.addEventListener('change', function(event) {
        var file = event.target.files[0];
        var reader = new FileReader();

        reader.onload = function(e) {
            previewImage.src = e.target.result;
            imageSrcInput.value = e.target.result;
        };

        reader.readAsDataURL(file);
        console.log(file)
    });
});

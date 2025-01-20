const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('capture');
const imageDataInput = document.getElementById('imageData');
const result = document.getElementById('result');

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia){
    // Activer la caméra
    navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: 'environment' }
    })

    .then(stream => {
        video.srcObject = stream;
        video.play();
    })
    .catch(err => console.error('Erreur d’accès à la caméra :', err));

    // Ajuster la taille du canvas
    video.addEventListener('loadedmetadata', () => {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
    });

    // Capture de l'image
    captureButton.addEventListener('click', () => {
        const context = canvas.getContext('2d');

        // Dessiner l'image vidéo dans le canvas
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Convertir en base64
        const imageData = canvas.toDataURL('image/png');
        imageDataInput.value = imageData;

        // Afficher les données capturées
        result.textContent = "Image capturée. Prête à être envoyée.";
    });
}else {
    alert("Votre navigateur ne prend pas en charge l'accès à la caméra.");
}
video.onerror = (e) => console.error('Erreur vidéo :', e);
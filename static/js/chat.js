const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/');
const arrow = document.getElementById('arrow');
const messagesDiv = document.getElementById('messages');

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    if (data.message === 'WebSocket desconectado, recarga la página para conectarse de nuevo') {
        messagesDiv.innerHTML += `
            <div class="alert alert-primary my-3" style="color:black; z-index: 2;">
                <img src="path/to/your/user-icon.png" alt="User" style="width: 20px; height: 20px; vertical-align: middle; margin-right: 5px;">
                ${data.message}
            </div>
        `;
    } else {
        // Eliminar el mensaje de espera
        const waitMessageElement = document.getElementById('wait-message');
        if (waitMessageElement) {
            waitMessageElement.remove();
        }

        // Mostrar la respuesta del bot
        messagesDiv.innerHTML += `
            <div class="bot-message">
                ${formatResponse(data.response)}
            </div>
        `;
        
        arrow.style.display = 'none';

        // Desplazar automáticamente hacia abajo
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
};

document.getElementById('chat-form').onsubmit = function (event) {
    event.preventDefault();
    const messageInputDom = document.getElementById('message-input');
    const message = messageInputDom.value;

    // Mostrar el mensaje del usuario
    messagesDiv.innerHTML += `
        <div class="user-message">
            ${message}
        </div>
    `;

    // Mostrar el mensaje de espera con puntos animados
    const waitMessage = `
        <div id="wait-message" class="bot-message">
            <span id="dots">•</span>
        </div>
    `;
    messagesDiv.innerHTML += waitMessage;

    // Animación de puntos
    let dotCount = 1;
    const dotsElement = document.getElementById('dots');
    setInterval(() => {
        if (dotCount < 3) {
            dotCount++;
        } else {
            dotCount = 1; // Reinicia el conteo
        }
        dotsElement.textContent = '•'.repeat(dotCount); // Actualiza el contenido
    }, 500); // Cambia los puntos cada 500 ms

    // Enviar el mensaje
    chatSocket.send(JSON.stringify({ 'message': message }));
    
    // Limpiar el campo de entrada
    messageInputDom.value = '';

    // Desplazar automáticamente hacia abajo
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    console.log("Mensaje enviado:", message); // Para depuración
};

// Función para formatear la respuesta
function formatResponse(response) {
    const lines = response.split(/[\.:]/).map(line => line.trim()).filter(line => line.length > 0);
    return lines.map(line => `<p>${line.trim()}.</p>`).join('');
};

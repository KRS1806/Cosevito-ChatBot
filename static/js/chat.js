const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/');
const arrow = document.getElementById('arrow'); // Referencia a la flecha
const messagesDiv = document.getElementById('messages'); // Referencia al div de mensajes


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
        // Mostrar el mensaje del usuario
        messagesDiv.innerHTML += `
    <div class="user-message">
        ${data.message}
    </div>
`;

        // Mostrar la respuesta del bot
        messagesDiv.innerHTML += `
    <div class="bot-message">
        ${data.response}
    </div>
`;
    }

    // Ocultar el mensaje de espera y los elementos de bienvenida
    document.getElementById('wait-message').style.display = 'none';
    arrow.style.display = 'none';

    // Desplazar automáticamente hacia abajo para mostrar el último mensaje
    messagesDiv.scrollbottom = messagesDiv.scrollHeight;
};

document.getElementById('chat-form').onsubmit = function (event) {
    event.preventDefault();
    const messageInputDom = document.getElementById('message-input');
    const message = messageInputDom.value;

    // Mostrar el mensaje de espera
    document.getElementById('wait-message').style.display = 'block';

    // Enviar el mensaje al servidor WebSocket
    chatSocket.send(JSON.stringify({
        'message': message
    }));

    // Limpiar el campo de entrada
    messageInputDom.value = '';
};
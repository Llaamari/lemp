const statusDot = document.getElementById('status');
const statusText = document.getElementById('status-text');
const messagesDiv = document.getElementById('messages');
const nicknameInput = document.getElementById('nickname');
const messageInput = document.getElementById('message');
const sendBtn = document.getElementById('send-btn');

const clientId = 'web_' + Math.random().toString(16).substr(2, 8);
const brokerUrl = (location.protocol === 'https:' ? 'wss://' : 'ws://')
    + window.location.host + '/mqtt';
    function addMessage(nickname, text, createdAt) {
        const div = document.createElement('div');
        div.className = 'msg';
        div.innerHTML = `<strong>${nickname}</strong>: ${text} <br><time>${createdAt}</time>`;
        messagesDiv.appendChild(div);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    
// Hae viimeiset 10 viestiä Flask API:sta
fetch('/api/messages?limit=10')
.then(r => r.json())
.then(rows => {
    const box = document.getElementById('messages');
    box.innerHTML = ""; // nollaa ennen kuin lisätään historia
    rows.forEach(row => {
        box.innerHTML += `<div class="msg"><span class="nick">${row.nickname}:</span> ${row.message}</div>`;
    });
})

.catch(err => console.error("Viestihistorian lataus tietokannasta epäonnistui", err));
// Yhdistä MQTT
const client = mqtt.connect(brokerUrl, { clientId, clean: true });

client.on('connect', () => {
    statusDot.style.background = 'green';
    statusText.textContent = 'Yhdistetty';
    client.subscribe('chat/messages');
    client.subscribe("chat/messages", { qos: 0 });
});

client.on('message', (topic, payload) => {
    try {
        const data = JSON.parse(payload.toString());
        const nick = data.nickname || "Tuntematon";
        const text = data.text || data.message;
        const time = data.created_at || new Date().toLocaleString("fi-FI");
        addMessage(nick, text, time);
    } catch(e) {
        console.error("Virheellinen viesti", e);
    }
});

function sendMsg() {
    const msg = {
        nickname: nicknameInput.value.trim() || "Nimetön",
        text: messageInput.value.trim(),
        clientId
    };
    
    if (msg.text) client.publish("chat/messages", JSON.stringify(msg));
    messageInput.value = "";
}

sendBtn.addEventListener('click', sendMsg);
messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') sendMsg();
});
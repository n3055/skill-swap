// Elements for Navigation
const nameInput = document.getElementById('nameInput');
const getHelpBtn = document.getElementById('getHelpBtn');
const helpBtn = document.getElementById('helpBtn');

const desktop2 = document.getElementById('desktop-2');
const desktop1 = document.getElementById('desktop-1');
const desktop3 = document.getElementById('desktop-3');
const desktop5 = document.getElementById('desktop-5');

// Navigation to "GET HELP" Page
getHelpBtn.addEventListener('click', () => {
    if (nameInput.value.trim()) {
        desktop2.classList.add('hidden');
        desktop1.classList.remove('hidden');
    } else {
        alert('Please enter your name.');
    }
});

// Navigation to "HELP" Page
helpBtn.addEventListener('click', () => {
    if (nameInput.value.trim()) {
        desktop2.classList.add('hidden');
        desktop3.classList.remove('hidden');
    } else {
        alert('Please enter your name.');
    }
});

// Navigation to Desktop-5
document.getElementById('findHelpBtn').addEventListener('click', () => {
    desktop1.classList.add('hidden');
    desktop5.classList.remove('hidden');
});

document.getElementById('findExpertiseBtn').addEventListener('click', () => {
    desktop3.classList.add('hidden');
    desktop5.classList.remove('hidden');
});

// Chat Box Functionality
const chatBox = document.getElementById('chatBox');
const chatMessage = document.getElementById('chatMessage');
const sendBtn = document.getElementById('sendBtn');

sendBtn.addEventListener('click', () => {
    const message = chatMessage.value.trim();
    if (message) {
        const timestamp = new Date().toLocaleTimeString();
        chatBox.innerHTML += `<p><strong>You:</strong> ${message} <small>${timestamp}</small></p>`;
        chatMessage.value = '';
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});

// Canvas Drawing Logic
const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');
let drawing = false;
let erasing = false;

// Set default pen color and size
ctx.strokeStyle = '#000';
ctx.lineWidth = 2;

// Event listeners for drawing
canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mouseout', stopDrawing);

// Correct button IDs and ensure eraser works
document.getElementById('penBtn').addEventListener('click', () => {
    erasing = false;
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;
});

document.getElementById('eraserBtn').addEventListener('click', () => {
    erasing = true;
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 10;
});

document.getElementById('clearBtn').addEventListener('click', () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
});

// Ensure drawing logic is properly implemented
function startDrawing(e) {
    drawing = true;
    ctx.beginPath();
    ctx.moveTo(e.offsetX, e.offsetY);
}

function draw(e) {
    if (!drawing) return;

    ctx.lineTo(e.offsetX, e.offsetY);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(e.offsetX, e.offsetY);
}

function stopDrawing() {
    drawing = false;
    ctx.beginPath();
}
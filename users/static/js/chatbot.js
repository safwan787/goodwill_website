const toggleBtn = document.getElementById("chatbot-toggle");
const chatBox = document.getElementById("chatbot-box");
const closeBtn = document.getElementById("chatbot-close");
const responseBox = document.getElementById("chatbot-response");

const WHATSAPP_NUMBER = "918075564099"; // Goodwill number

// Toggle chatbot
toggleBtn.onclick = () => {
    chatBox.style.display = "block";
};

closeBtn.onclick = () => {
    chatBox.style.display = "none";
};

// Handle button clicks
document.querySelectorAll(".bot-options button").forEach(btn => {
    btn.onclick = () => {
        const type = btn.getAttribute("data-msg");
        handleResponse(type);
    };
});

// Handle slash commands
function handleSlashCommand(text) {
    if (text.startsWith("/")) {
        const cmd = text.toLowerCase();

        if (cmd === "/offers") return showOffers();
        if (cmd === "/enquiry") return showWhatsapp();
        if (cmd === "/store") return showStore();
        if (cmd === "/custom") return showCustom();
        if (cmd === "/help") return showHelp();

        return botMessage("❓ Unknown command. Type /help to see available options.");
    }
}

// Main handler
function handleResponse(type) {
    switch (type) {
        case "products":
            botMessage("🛍 You can browse all our products from the Shop section.");
            break;

        case "offers":
            showOffers();
            break;

        case "custom":
            showCustom();
            break;

        case "contact":
            showWhatsapp();
            break;

        case "store":
            showStore();
            break;
    }
}

// Response helpers
function showOffers() {
    botMessage(`
        🎁 <b>Current Offers</b><br>
        • Discounts on selected frames<br>
        • Special combo gift packs<br>
        • Festival offers available<br><br>
        Visit the Offers section for details.
    `);
}

function showCustom() {
    botMessage(`
        📝 <b>Custom Orders</b><br>
        We offer customized frames, gifts & momentos.<br>
        Share your idea with our team on WhatsApp.
    `);
}

function showStore() {
    botMessage(`
        📍 <b>Visit Our Store</b><br>
        Experience our products in person.<br>
        Location: Kerala, India<br>
        Timings: 9:30 AM – 8:30 PM
    `);
}

function showWhatsapp() {
    const link = `https://wa.me/${WHATSAPP_NUMBER}`;
    botMessage(`
        💬 <b>WhatsApp Support</b><br>
        <a href="${link}" target="_blank">
            Click here to chat with us
        </a>
    `);
}

function showHelp() {
    botMessage(`
        ℹ️ <b>Available Commands</b><br>
        /offers – View offers<br>
        /enquiry – WhatsApp support<br>
        /store – Store details<br>
        /custom – Custom orders<br>
        /help – Show commands
    `);
}

function botMessage(msg) {
    responseBox.innerHTML = `<div class="bot-msg">${msg}</div>`;
}

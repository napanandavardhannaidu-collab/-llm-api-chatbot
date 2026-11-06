
const API_URL = "http://127.0.0.1:8000";

const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const clearBtn = document.getElementById("clear-btn");
const loading = document.getElementById("loading");

// One ID is maintained for this browser conversation.
let conversationId = crypto.randomUUID();

function addMessage(content, sender) {
    const message = document.createElement("div");
    message.classList.add("message", sender);

    // Use textContent to safely display API responses.
    message.textContent = content;

    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const message = userInput.value.trim();

    if (!message) return;

    addMessage(message, "user");
    userInput.value = "";

    sendBtn.disabled = true;
    loading.classList.remove("hidden");

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                conversation_id: conversationId,
                message: message
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Something went wrong");
        }

        addMessage(data.response, "bot");

    } catch (error) {
        addMessage(`Error: ${error.message}`, "bot");
    } finally {
        loading.classList.add("hidden");
        sendBtn.disabled = false;
        userInput.focus();
    }
}

async function clearConversation() {
    try {
        const response = await fetch(
            `${API_URL}/history/${conversationId}`,
            { method: "DELETE" }
        );

        if (!response.ok) {
            throw new Error("Could not clear conversation");
        }

        conversationId = crypto.randomUUID();

        chatBox.replaceChildren();

        addMessage(
            "Conversation cleared! How can I help you?",
            "bot"
        );

    } catch (error) {
        addMessage(`Error: ${error.message}`, "bot");
    }
}

sendBtn.addEventListener("click", sendMessage);

userInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        sendMessage();
    }
});

clearBtn.addEventListener("click", clearConversation);

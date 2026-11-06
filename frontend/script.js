
const API_URL = "http://172.18.246.151:8000";

const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const clearBtn = document.getElementById("clear-btn");
const loading = document.getElementById("loading");

// Generate a conversation ID without requiring crypto.randomUUID().
function generateConversationId() {
    return (
        "conv_" +
        Date.now() +
        "_" +
        Math.random().toString(36).slice(2, 10)
    );
}

// Maintain one ID for the current browser conversation.
let conversationId = generateConversationId();

function addMessage(content, sender) {
    const message = document.createElement("div");

    message.classList.add("message", sender);

    // Safely display text without interpreting HTML.
    message.textContent = content;

    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const message = userInput.value.trim();

    if (!message || sendBtn.disabled) {
        return;
    }

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
            throw new Error(
                data.detail || "Something went wrong"
            );
        }

        addMessage(data.response, "bot");

    } catch (error) {
        console.error("Chat API error:", error);

        addMessage(
            `Error: ${error.message}`,
            "bot"
        );

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
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {
            throw new Error("Could not clear conversation");
        }

        conversationId = generateConversationId();

        chatBox.replaceChildren();

        addMessage(
            "Conversation cleared! How can I help you?",
            "bot"
        );

    } catch (error) {
        console.error("Clear conversation error:", error);

        addMessage(
            `Error: ${error.message}`,
            "bot"
        );
    }
}

// Send button event.
sendBtn.addEventListener("click", sendMessage);

// Enter key event.
userInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        sendMessage();
    }
});

// Clear button event.
clearBtn.addEventListener("click", clearConversation);

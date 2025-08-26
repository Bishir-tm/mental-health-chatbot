document.addEventListener("DOMContentLoaded", () => {
  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("chat-input");
  const chatMessages = document.getElementById("chat-messages");
  const newChatBtn = document.getElementById("newChatBtn");
  const statusIndicator = document.getElementById("status-indicator");

  let messages = [];
  let modelReady = false;

  const addMessage = (role, content) => {
    const message = { role, content };
    messages.push(message);
    renderMessages();
  };

  const renderMessages = () => {
    chatMessages.innerHTML = "";
    messages.forEach((message) => {
      const messageElement = document.createElement("div");
      messageElement.classList.add(
        message.role === "user" ? "user-message" : "assistant-message"
      );
      messageElement.textContent = message.content;
      chatMessages.appendChild(messageElement);
    });
    chatMessages.scrollTop = chatMessages.scrollHeight;
  };

  const showLoadingIndicator = () => {
    const loadingElement = document.createElement("div");
    loadingElement.classList.add("assistant-message");
    loadingElement.innerHTML =
      '<div class="loading-dots"><span></span><span></span><span></span></div>';
    chatMessages.appendChild(loadingElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  };

  const removeLoadingIndicator = () => {
    const loadingElement = chatMessages.querySelector(".loading-dots");
    if (loadingElement) {
      loadingElement.parentElement.remove();
    }
  };

  const updateStatusIndicator = (status, message) => {
    if (statusIndicator) {
      statusIndicator.className = "status-indicator";
      statusIndicator.classList.add(status);
      statusIndicator.textContent = message;
    }
  };

  const checkModelStatus = async () => {
    try {
      const response = await fetch("/api/health");
      const data = await response.json();

      if (data.status === "ready") {
        modelReady = true;
        updateStatusIndicator("ready", "🟢 AI Model Ready");
        chatInput.disabled = false;
        chatInput.placeholder = "Type your message here...";
      } else {
        modelReady = false;
        updateStatusIndicator("loading", "🟡 AI Model Loading...");
        chatInput.disabled = true;
        chatInput.placeholder = "Please wait, AI model is loading...";
        // Check again in 5 seconds
        setTimeout(checkModelStatus, 5000);
      }
    } catch (error) {
      modelReady = false;
      updateStatusIndicator("error", "🔴 AI Model Error");
      chatInput.disabled = true;
      chatInput.placeholder = "AI model unavailable. Please refresh the page.";
    }
  };

  chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const userInput = chatInput.value.trim();
    if (!userInput || !modelReady) return;

    addMessage("user", userInput);
    chatInput.value = "";
    showLoadingIndicator();

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ messages }),
      });

      const data = await response.json();
      removeLoadingIndicator();

      if (response.status === 503) {
        // Model still loading
        addMessage(
          "assistant",
          "The AI model is still loading. Please wait a moment and try again."
        );
        modelReady = false;
        checkModelStatus();
      } else if (data.error) {
        addMessage(
          "assistant",
          "I apologize, but I encountered an error. Please try again or start a new conversation."
        );
      } else {
        addMessage("assistant", data.response);
        if (data.crisis) {
          const crisisAlert = document.createElement("div");
          crisisAlert.classList.add("alert", "alert-danger", "mt-3");
          crisisAlert.innerHTML = `
                        <h4 class="alert-heading">Immediate Support Available</h4>
                        <p>It sounds like you are going through a very difficult time. Your safety is the most important thing. Please reach out for help.</p>
                        <hr>
                        <p class="mb-0">You can call the Nigerian emergency hotline at 112, or reach out to the Suicide Research and Prevention Initiative (SURPIN) at 08092106463.</p>
                    `;
          chatMessages.appendChild(crisisAlert);
        }
      }
    } catch (error) {
      removeLoadingIndicator();
      addMessage(
        "assistant",
        "I apologize, but I encountered a connection error. Please check your connection and try again."
      );
    }
  });

  newChatBtn.addEventListener("click", () => {
    messages = [];
    chatMessages.innerHTML =
      '<div class="assistant-message">Hello. How are you feeling today?</div>';
  });

  // Initialize
  checkModelStatus();
  addMessage("assistant", "Hello. How are you feeling today?");
});

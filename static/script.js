document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const newChatBtn = document.getElementById('newChatBtn');

    let messages = [];

    const addMessage = (role, content) => {
        const message = { role, content };
        messages.push(message);
        renderMessages();
    };

    const renderMessages = () => {
        chatMessages.innerHTML = '';
        messages.forEach(message => {
            const messageElement = document.createElement('div');
            messageElement.classList.add(message.role === 'user' ? 'user-message' : 'assistant-message');
            messageElement.textContent = message.content;
            chatMessages.appendChild(messageElement);
        });
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    const showLoadingIndicator = () => {
        const loadingElement = document.createElement('div');
        loadingElement.classList.add('assistant-message');
        loadingElement.innerHTML = '<div class="loading-dots"><span></span><span></span><span></span></div>';
        chatMessages.appendChild(loadingElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    const removeLoadingIndicator = () => {
        const loadingElement = chatMessages.querySelector('.loading-dots');
        if (loadingElement) {
            loadingElement.parentElement.remove();
        }
    };

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const userInput = chatInput.value.trim();
        if (!userInput) return;

        addMessage('user', userInput);
        chatInput.value = '';
        showLoadingIndicator();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ messages })
            });

            const data = await response.json();
            removeLoadingIndicator();

            if (data.error) {
                alert(data.error);
            } else {
                addMessage('assistant', data.response);
                if (data.crisis) {
                    const crisisAlert = document.createElement('div');
                    crisisAlert.classList.add('alert', 'alert-danger', 'mt-3');
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
            alert('An error occurred while processing your request. Please try again.');
        }
    });

    newChatBtn.addEventListener('click', () => {
        messages = [];
        chatMessages.innerHTML = '<div class="assistant-message">Hello. How are you feeling today?</div>';
    });

    addMessage('assistant', 'Hello. How are you feeling today?');
});

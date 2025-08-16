// script.js

document.addEventListener('DOMContentLoaded', () => {
    const messagesContainer = document.getElementById('messages');
    const chatInput = document.getElementById('chatInput');
    const chatForm = document.getElementById('chatForm');
    const newChatBtn = document.getElementById('newChatBtn');
    const messagesEndRef = document.getElementById('messagesEndRef');
    const sendBtn = document.getElementById('sendBtn');

    let messages = [
        { id: 'init', role: 'assistant', content: "Hello. How are you feeling today?" }
    ];
    let isLoading = false;

    const scrollToBottom = () => {
        messagesEndRef.scrollIntoView({ behavior: 'smooth' });
    };

    const displayMessage = (message) => {
        const messageBubble = document.createElement('div');
        messageBubble.classList.add('message-bubble', message.role);

        if (message.role === 'assistant') {
            const avatar = document.createElement('div');
            avatar.classList.add('avatar', 'assistant');
            avatar.textContent = 'AI';
            messageBubble.appendChild(avatar);
        }

        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        messageContent.innerHTML = `<p>${message.content}</p>`;
        messageBubble.appendChild(messageContent);

        if (message.role === 'user') {
            const avatar = document.createElement('div');
            avatar.classList.add('avatar', 'user');
            avatar.textContent = 'User';
            messageBubble.appendChild(avatar);
        }

        messagesContainer.appendChild(messageBubble);
    };

    const renderMessages = () => {
        messagesContainer.innerHTML = ''; // Clear existing messages
        messages.forEach(displayMessage);
        scrollToBottom();
    };

    const showLoadingIndicator = () => {
        isLoading = true;
        sendBtn.disabled = true;
        chatInput.disabled = true;

        const loadingBubble = document.createElement('div');
        loadingBubble.classList.add('message-bubble', 'assistant');
        loadingBubble.id = 'loadingIndicator';

        const avatar = document.createElement('div');
        avatar.classList.add('avatar', 'assistant');
        avatar.textContent = 'AI';
        loadingBubble.appendChild(avatar);

        const loadingContent = document.createElement('div');
        loadingContent.classList.add('message-content');
        loadingContent.innerHTML = `
            <div class="loading-indicator">
                <span class="loading-dot"></span>
                <span class="loading-dot"></span>
                <span class="loading-dot"></span>
            </div>
        `;
        loadingBubble.appendChild(loadingContent);
        messagesContainer.appendChild(loadingBubble);
        scrollToBottom();
    };

    const hideLoadingIndicator = () => {
        isLoading = false;
        sendBtn.disabled = false;
        chatInput.disabled = false;
        const loadingIndicator = document.getElementById('loadingIndicator');
        if (loadingIndicator) {
            loadingIndicator.remove();
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!chatInput.value.trim() || isLoading) return;

        const userMessage = {
            id: Date.now().toString(),
            role: 'user',
            content: chatInput.value.trim(),
        };

        messages.push(userMessage);
        displayMessage(userMessage);
        chatInput.value = '';
        scrollToBottom();

        showLoadingIndicator();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ chatHistory: messages }),
            });

            const data = await response.json();

            if (data.error) {
                alert(`Error: ${data.error}`); // Simple error display
                messages.pop(); // Remove user message if AI fails
            } else if (data.response) {
                const assistantMessage = {
                    id: Date.now().toString() + '-ai',
                    role: 'assistant',
                    content: data.response,
                };
                messages.push(assistantMessage);
                displayMessage(assistantMessage);
            }
        } catch (error) {
            console.error('Fetch error:', error);
            alert('An error occurred while connecting to the server. Please try again.');
            messages.pop(); // Remove user message if network fails
        } finally {
            hideLoadingIndicator();
            scrollToBottom();
        }
    };

    chatForm.addEventListener('submit', handleSubmit);

    newChatBtn.addEventListener('click', () => {
        messages = [
            { id: 'init', role: 'assistant', content: "Hello. How are you feeling today?" }
        ];
        renderMessages();
    });

    // Initial render
    renderMessages();
});

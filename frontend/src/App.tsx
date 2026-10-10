import { useState } from "react";
// @ts-expect-error CSS is loaded by the bundler and has no TypeScript declarations.
import "./App.css";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface ChatResponse {
  response: string;
}

function App() {
  const [message, setMessage] = useState<string>("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const sendMessage = async (): Promise<void> => {
    if (!message.trim() || loading) {
      return;
    }

    const userMessage = message.trim();

    // Add user's message to chat
    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },     
        body: JSON.stringify({
         message: userMessage,
         history: messages,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to get response from server");
      }

      const data: ChatResponse = await response.json();

      // Add AI response
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.response,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: "Sorry, something went wrong. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (
    event: React.KeyboardEvent<HTMLTextAreaElement>
  ): void => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="app">
      <div className="chat-container">
        <header className="chat-header">
          <h1>AI Appointment Assistant</h1>
          <p>How can I help you today?</p>
        </header>

        <div className="messages">
          {messages.length === 0 && (
            <div className="welcome">
              <h2>Welcome 👋</h2>
              <p>
                Ask me about therapists or available appointment slots.
              </p>
            </div>
          )}

          {messages.map((item, index) => (
            <div
              key={index}
              className={`message ${
                item.role === "user"
                  ? "user-message"
                  : "assistant-message"
              }`}
            >
              {item.content}
            </div>
          ))}

          {loading && (
            <div className="message assistant-message">
              Thinking...
            </div>
          )}
        </div>

        <div className="input-area">
          <textarea
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message..."
            rows={1}
          />

          <button
            onClick={sendMessage}
            disabled={loading || !message.trim()}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
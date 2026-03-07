import React, { useState, useEffect, useRef } from "react";
import { sendMessage, getChatHistory, clearChatHistory } from "../api";

interface Props {
  workspaceId: number | null;
  workspaceName: string;
}

const Chatbot: React.FC<Props> = ({ workspaceId, workspaceName }) => {
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  const loadHistory = async () => {
    if (!workspaceId) return;
    const data = await getChatHistory(workspaceId);
    setMessages(data);
  };

  useEffect(() => {
    setMessages([]);
    loadHistory();
  }, [workspaceId]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || !workspaceId) return;
    const userMsg = input.trim();
    setInput("");
    setMessages(prev => [...prev, { role: "user", content: userMsg }]);
    setLoading(true);
    try {
      const data = await sendMessage(workspaceId, userMsg);
      setMessages(prev => [...prev, { role: "assistant", content: data.response }]);
    } catch {
      setMessages(prev => [...prev, { role: "assistant", content: "Error: Could not get response." }]);
    }
    setLoading(false);
  };

  const handleClear = async () => {
    if (!workspaceId) return;
    await clearChatHistory(workspaceId);
    setMessages([]);
  };

  if (!workspaceId) {
    return (
      <div className="bg-white rounded-xl shadow p-6 flex items-center justify-center h-64">
        <p className="text-gray-400">Select a workspace to start chatting</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow flex flex-col h-[500px]">
      <div className="flex justify-between items-center p-4 border-b">
        <h2 className="font-bold text-gray-700">🤖 AI Chat — {workspaceName}</h2>
        <button onClick={handleClear} className="text-xs text-red-400 hover:text-red-600">
          Clear History
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.length === 0 && (
          <p className="text-gray-400 text-sm text-center mt-8">
            Ask me anything about your imported papers!
          </p>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
            <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-2xl text-sm ${
              m.role === "user"
                ? "bg-blue-600 text-white rounded-br-none"
                : "bg-gray-100 text-gray-800 rounded-bl-none"
            }`}>
              {m.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 px-4 py-2 rounded-2xl text-sm text-gray-500 rounded-bl-none">
              Thinking...
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="p-4 border-t flex gap-2">
        <input
          className="flex-1 border rounded-full px-4 py-2 text-sm outline-none"
          placeholder="Ask about your research papers..."
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && handleSend()}
        />
        <button onClick={handleSend}
          className="bg-blue-600 text-white px-4 py-2 rounded-full text-sm hover:bg-blue-700">
          Send
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
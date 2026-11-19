import React, { useState, useRef, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import {
  MessageSquare,
  Send,
  Sparkles,
  Bot,
  User,
  Compass,
  ArrowRight,
  BookOpen,
  DollarSign,
  CloudRain
} from 'lucide-react';
import api from '../api/client';
import { useAuth } from '../context/AuthContext';

const PROMPT_SUGGESTIONS = [
  'Can you help reduce my trip budget?',
  'Suggest cheaper homestays or hotels.',
  'What should I visit on day two of my trip?',
  'Is this destination suitable during monsoon season?',
  'Suggest family-friendly modifications.',
  'What regional cuisine should I definitely try?'
];

export default function AssistantPage() {
  const { user } = useAuth();
  const location = useLocation();
  const itineraryContext = location.state?.itineraryContext || null;

  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: `Hello ${user?.full_name?.split(' ')[0] || 'Traveler'}! I am TripMind AI, your personal travel assistant. I am grounded with indexed destination knowledge, Scikit-Learn prediction models, and live weather advisories.\n\nHow can I help optimize your travel plans today?`,
      sources: []
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (textToSend) => {
    const query = textToSend || inputText;
    if (!query.trim() || loading) return;

    const userMsg = {
      id: Date.now(),
      role: 'user',
      content: query.trim()
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputText('');
    setLoading(true);

    try {
      const res = await api.post('/assistant/chat', {
        session_id: sessionId,
        trip_id: itineraryContext?.trip_id,
        message: query.trim(),
        current_destination: itineraryContext?.destination_name || 'India',
        current_budget: itineraryContext?.total_budget,
        itinerary_context: itineraryContext
      });

      setSessionId(res.data.session_id);

      const botMsg = {
        id: Date.now() + 1,
        role: 'assistant',
        content: res.data.reply,
        sources: res.data.retrieved_sources || [],
        suggested_actions: res.data.suggested_actions || []
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.warn('Chat error:', err);
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          role: 'assistant',
          content: 'Sorry, I encountered a temporary connection issue. Please check your request or try again in a moment.',
          sources: []
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 h-[calc(100vh-5rem)] flex flex-col space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center text-white shadow-md shadow-cyan-500/20">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-white flex items-center gap-2">
              TripMind AI Travel Assistant
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-cyan-950 text-cyan-400 border border-cyan-800">
                FAISS RAG + Gemini
              </span>
            </h1>
            <p className="text-xs text-slate-400">
              {itineraryContext?.destination_name ? `Active Context: ${itineraryContext.destination_name} (Budget: ₹${itineraryContext.total_budget})` : 'Context-aware intelligent travel concierge'}
            </p>
          </div>
        </div>
      </div>

      {/* Chat Messages Log */}
      <div className="flex-1 overflow-y-auto space-y-4 p-4 rounded-2xl bg-slate-900/60 border border-slate-800 shadow-inner">
        {messages.map((msg) => {
          const isBot = msg.role === 'assistant';
          return (
            <div
              key={msg.id}
              className={`flex items-start gap-3 ${isBot ? '' : 'flex-row-reverse'}`}
            >
              <div
                className={`w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0 text-xs font-bold ${
                  isBot
                    ? 'bg-cyan-950 text-cyan-400 border border-cyan-800'
                    : 'bg-blue-600 text-white'
                }`}
              >
                {isBot ? <Bot className="w-4 h-4" /> : <User className="w-4 h-4" />}
              </div>

              <div
                className={`max-w-[85%] sm:max-w-[75%] rounded-2xl p-4 text-xs sm:text-sm leading-relaxed space-y-2.5 shadow-md ${
                  isBot
                    ? 'bg-slate-900 border border-slate-800 text-slate-200'
                    : 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white'
                }`}
              >
                <div className="whitespace-pre-wrap">{msg.content}</div>

                {/* Grounded RAG Sources Badge */}
                {msg.sources && msg.sources.length > 0 && (
                  <div className="pt-2 border-t border-slate-800/80 flex flex-wrap items-center gap-1.5 text-[10px] text-slate-400">
                    <BookOpen className="w-3 h-3 text-cyan-400 flex-shrink-0" />
                    <span className="font-semibold text-slate-300">Grounded in:</span>
                    {msg.sources.map((s, idx) => (
                      <span key={idx} className="bg-slate-950 px-2 py-0.5 rounded border border-slate-800 text-cyan-300">
                        {s}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {loading && (
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-xl bg-cyan-950 text-cyan-400 border border-cyan-800 flex items-center justify-center">
              <Bot className="w-4 h-4" />
            </div>
            <div className="p-3.5 rounded-2xl bg-slate-900 border border-slate-800 text-xs text-slate-400 flex items-center gap-2">
              <Sparkles className="w-3.5 h-3.5 text-cyan-400 animate-spin" />
              Retrieving knowledge base and formulating response...
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Prompt Suggestions */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1 no-scrollbar">
        {PROMPT_SUGGESTIONS.map((s, i) => (
          <button
            key={i}
            onClick={() => handleSendMessage(s)}
            className="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 hover:border-cyan-500/40 text-[11px] text-slate-300 whitespace-nowrap transition-colors"
          >
            {s}
          </button>
        ))}
      </div>

      {/* Chat Input Bar */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSendMessage();
        }}
        className="flex items-center gap-2 p-1.5 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl"
      >
        <input
          type="text"
          placeholder="Ask anything about destinations, budget reduction, weather, or itinerary changes..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          className="flex-1 bg-transparent text-xs sm:text-sm text-white placeholder-slate-500 px-4 py-2.5 focus:outline-none"
        />
        <button
          type="submit"
          disabled={loading || !inputText.trim()}
          className="p-2.5 rounded-xl bg-cyan-400 hover:bg-cyan-300 text-slate-950 font-bold transition-colors disabled:opacity-40 flex items-center justify-center shadow"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}

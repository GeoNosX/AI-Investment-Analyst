'use client';

import { useState, useRef, useEffect } from 'react';
import { BotMessageSquare, User, SendHorizonal, LoaderCircle } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

type Message = {
  id: number;
  type: 'user' | 'bot';
  content: string;
  ticker?: string;
};

export default function Home() {
  const [ticker, setTicker] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      type: 'bot',
      content: 'Hello! Enter a stock ticker (e.g., AAPL, TSLA) below to generate an institutional investment report.',
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!ticker.trim() || isLoading) return;

    const currentTicker = ticker.toUpperCase().trim();
    setTicker('');

    const userMessageId = Date.now();
    setMessages((prev) => [
      ...prev,
      { id: userMessageId, type: 'user', content: `Analyze ${currentTicker}`, ticker: currentTicker },
    ]);

    setIsLoading(true);

    const botMessageId = userMessageId + 1;
    setMessages((prev) => [
      ...prev,
      { id: botMessageId, type: 'bot', content: '', ticker: currentTicker },
    ]);

    try {
      const response = await fetch(`http://localhost:8000/analyze/${currentTicker}`);

      if (!response.body) throw new Error('No response body');

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let accumulatedReport = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        accumulatedReport += chunk;

        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === botMessageId ? { ...msg, content: accumulatedReport } : msg
          )
        );
      }
    } catch (error) {
      console.error('Streaming Error:', error);
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === botMessageId
            ? { ...msg, content: `⚠️ Error connecting to the analysis server. Please ensure the backend is running on port 8000.` }
            : msg
        )
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col bg-gray-50 text-gray-900">
      <header className="sticky top-0 z-10 border-b bg-white/95 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <BotMessageSquare className="w-8 h-8 text-blue-600" />
            <h1 className="text-2xl font-bold tracking-tight">FinBot <span className='text-gray-400 font-normal'>Institutional Analyst</span></h1>
          </div>
          <div className='text-sm px-3 py-1 rounded-full bg-green-100 text-green-800 font-medium'>
            Live Market Data
          </div>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6 max-w-5xl mx-auto w-full">
        {messages.map((message) => (
          <div key={message.id} className={`flex gap-4 ${message.type === 'user' ? 'justify-end' : ''}`}>
            {message.type === 'bot' && (
              <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center border border-blue-200 shrink-0 mt-1">
                <BotMessageSquare className="w-6 h-6 text-blue-600" />
              </div>
            )}
            
            {/* Updated container width and overflow for Markdown tables */}
            <div className={`p-4 rounded-2xl max-w-[85%] overflow-x-auto shadow-sm ${message.type === 'user' ? 'bg-blue-600 text-white rounded-br-none' : 'bg-white border rounded-bl-none'
              }`}>
              {message.ticker && message.type === 'bot' && message.content && (
                <div className="font-mono text-xs text-blue-500 mb-2 uppercase tracking-wider border-b pb-1">
                  Analysis for {message.ticker}
                </div>
              )}
              
              {/* Conditional rendering: Markdown for Bot, raw text for User */}
              {message.type === 'bot' ? (
                <div className="prose prose-sm md:prose-base max-w-none prose-tables:border-collapse prose-th:border prose-th:bg-gray-50 prose-td:border prose-th:p-2 prose-td:p-2 prose-blue">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {message.content}
                  </ReactMarkdown>
                  
                  {isLoading && message.id === messages[messages.length - 1].id && message.content === "" && (
                     <span className="inline-flex gap-2 items-center text-gray-400 italic not-prose mt-2">
                       <LoaderCircle className="w-4 h-4 animate-spin" /> Gathering financial data & news...
                     </span>
                  )}
                </div>
              ) : (
                <p className="whitespace-pre-wrap text-sm leading-relaxed">{message.content}</p>
              )}
            </div>

            {message.type === 'user' && (
              <div className="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center border shrink-0 mt-1">
                <User className="w-6 h-6 text-gray-600" />
              </div>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <footer className="sticky bottom-0 border-t bg-white p-4">
        <form onSubmit={handleAnalyze} className="max-w-5xl mx-auto flex gap-3">
          <input
            type="text"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            placeholder="Enter Stock Ticker (e.g., NVDA, MSFT)..."
            className="flex-1 p-4 border rounded-xl focus:ring-2 focus:ring-blue-200 focus:border-blue-500 outline-none transition disabled:bg-gray-100"
            disabled={isLoading}
            maxLength={10}
          />
          <button
            type="submit"
            className="bg-blue-600 text-white p-4 rounded-xl hover:bg-blue-700 transition disabled:bg-gray-300 shrink-0 flex items-center gap-2 font-medium"
            disabled={isLoading || !ticker.trim()}
          >
            {isLoading ? (
              <LoaderCircle className="w-6 h-6 animate-spin" />
            ) : (
              <SendHorizonal className="w-6 h-6" />
            )}
            {isLoading ? 'Analyzing...' : 'Analyze'}
          </button>
        </form>
      </footer>
    </main>
  );
}
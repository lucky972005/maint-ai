"use client";

import { useEffect, useRef, useState } from "react";
import { Bot, Mic, Send, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { useApp } from "@/components/providers";

function MessageContent({ content }: { content: string }) {
  const parts = content.split(/(\*\*[^*]+\*\*|\n)/g);
  return (
    <div className="whitespace-pre-wrap text-sm">
      {parts.map((part, index) => {
        if (part.startsWith("**") && part.endsWith("**")) {
          return <strong key={index}>{part.slice(2, -2)}</strong>;
        }
        if (part === "\n") return <br key={index} />;
        return part;
      })}
    </div>
  );
}

interface Message {
  role: "user" | "assistant";
  content: string;
}

const QUICK_PROMPTS = [
  "Why is my motor overheating?",
  "What's the torque spec?",
  "Show wiring diagram",
  "How do I replace the belt?",
];

interface ChatWidgetProps {
  machineContext?: string;
  sessionContext?: string;
  machineId?: string;
  fullPage?: boolean;
}

export function ChatWidget({
  machineContext,
  sessionContext,
  machineId,
  fullPage = false,
}: ChatWidgetProps) {
  const { profile } = useApp();
  const storageKey = machineId ? `fixbot:${machineId}` : profile?.id ? `fixbot:${profile.id}` : "fixbot:global";
  const [messages, setMessages] = useState<Message[]>(() => {
    if (typeof window !== "undefined") {
      const stored = window.localStorage.getItem(storageKey);
      if (stored) {
        try {
          return JSON.parse(stored) as Message[];
        } catch {
          /* ignore parse errors */
        }
      }
    }

    return [
      {
        role: "assistant",
        content: machineContext
          ? `Hi! I'm FixBot, your AI mechanic. I see you're working on **${machineContext}**${sessionContext ? ` (${sessionContext})` : ""}. How can I help?`
          : "Hi! I'm FixBot, your AI maintenance assistant. Ask me anything about repairs, specs, or troubleshooting.",
      },
    ];
  });
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    window.localStorage.setItem(storageKey, JSON.stringify(messages.slice(-20)));
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, storageKey]);

  useEffect(() => {
    if (machineContext && messages.length === 1) {
      setMessages([
        {
          role: "assistant",
          content: `Hi! I'm FixBot, your AI mechanic. I see you're working on **${machineContext}**${sessionContext ? ` (${sessionContext})` : ""}. How can I help?`,
        },
      ]);
    }
  }, [machineContext, sessionContext, messages.length]);

  const sendMessage = async (text: string) => {
    if (!text.trim() || loading) return;

    const userMsg: Message = { role: "user", content: text };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);
    setSuggestions([]);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: [...messages, userMsg].map((message) => ({
            role: message.role,
            content: message.content,
          })),
          machineContext: sessionContext
            ? `${machineContext ?? ""}${machineContext ? " - " : ""}${sessionContext}`
            : machineContext,
        }),
      });
      const data = await res.json();
      setMessages((prev) => [...prev, { role: "assistant", content: data.message }]);
      if (data.suggestions) setSuggestions(data.suggestions);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Sorry, I couldn't process that. Please try again." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const startVoiceInput = () => {
    const win = window as Window & { webkitSpeechRecognition?: typeof window.SpeechRecognition };
    const SpeechRecognition = win.SpeechRecognition || win.webkitSpeechRecognition;
    if (!SpeechRecognition) return;
    const recognition = new SpeechRecognition();
    recognition.onresult = (event: Event) => {
      const results = (
        event as unknown as { results: { [i: number]: { [j: number]: { transcript: string } } } }
      ).results;
      const transcript = results[0][0].transcript;
      sendMessage(transcript);
    };
    recognition.start();
  };

  return (
    <div className={`flex flex-col ${fullPage ? "h-[calc(100vh-140px)]" : "h-96"}`}>
      <div ref={scrollRef} className="flex-1 space-y-4 overflow-y-auto p-4">
        {messages.map((message, index) => (
          <div key={index} className={`flex gap-3 ${message.role === "user" ? "flex-row-reverse" : ""}`}>
            <div
              className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full ${
                message.role === "assistant" ? "bg-primary" : "bg-secondary"
              }`}
            >
              {message.role === "assistant" ? (
                <Bot className="h-4 w-4 text-primary-foreground" />
              ) : (
                <User className="h-4 w-4" />
              )}
            </div>
            <Card className={`max-w-[80%] p-3 ${message.role === "user" ? "border-primary/20 bg-primary/10" : ""}`}>
              <MessageContent content={message.content} />
            </Card>
          </div>
        ))}
        {loading && (
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Bot className="h-4 w-4 animate-pulse" />
            FixBot is thinking...
          </div>
        )}
      </div>

      {!messages.some((message) => message.role === "user") && (
        <div className="flex flex-wrap gap-2 px-4 pb-2">
          {QUICK_PROMPTS.map((prompt) => (
            <Button key={prompt} variant="outline" size="sm" onClick={() => sendMessage(prompt)}>
              {prompt}
            </Button>
          ))}
        </div>
      )}

      {suggestions.length > 0 && (
        <div className="flex flex-wrap gap-2 px-4 pb-2">
          {suggestions.map((suggestion) => (
            <Button
              key={suggestion}
              variant="ghost"
              size="sm"
              className="text-primary"
              onClick={() => sendMessage(suggestion)}
            >
              {suggestion}
            </Button>
          ))}
        </div>
      )}

      <div className="flex gap-2 border-t border-border p-4">
        <Input
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Ask FixBot..."
          onKeyDown={(event) => event.key === "Enter" && sendMessage(input)}
        />
        <Button size="icon" variant="outline" onClick={startVoiceInput}>
          <Mic className="h-4 w-4" />
        </Button>
        <Button size="icon" onClick={() => sendMessage(input)} disabled={loading}>
          <Send className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}

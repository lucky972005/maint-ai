export type VoiceCommand =
  | "next"
  | "previous"
  | "repeat"
  | "tools"
  | "safety"
  | "help"
  | "unknown";

export interface VoiceControlCallbacks {
  onNext?: () => void;
  onPrevious?: () => void;
  onRepeat?: () => void;
  onTools?: () => void;
  onSafety?: () => void;
  onHelp?: () => void;
  onListeningChange?: (listening: boolean) => void;
  onTranscript?: (text: string) => void;
}

interface SpeechRecognitionEvent extends Event {
  results: SpeechRecognitionResultList;
}

interface SpeechRecognitionInstance extends EventTarget {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  start: () => void;
  stop: () => void;
  abort: () => void;
  onresult: ((event: SpeechRecognitionEvent) => void) | null;
  onend: (() => void) | null;
  onerror: ((event: Event) => void) | null;
}

declare global {
  interface Window {
    SpeechRecognition: new () => SpeechRecognitionInstance;
    webkitSpeechRecognition: new () => SpeechRecognitionInstance;
  }
}

const COMMAND_PATTERNS: { pattern: RegExp; command: VoiceCommand }[] = [
  { pattern: /^(next|forward|continue)(\s+step)?$/i, command: "next" },
  { pattern: /^(back|previous)(\s+step)?$/i, command: "previous" },
  { pattern: /^(repeat|say again|again)$/i, command: "repeat" },
  { pattern: /^(tools|equipment|tool list)$/i, command: "tools" },
  { pattern: /^(safety|warning|danger|confirm safety)$/i, command: "safety" },
  { pattern: /^help$/i, command: "help" },
];

export function parseVoiceCommand(text: string): VoiceCommand {
  const normalized = text.trim().replace(/[.,!?]/g, "");
  for (const { pattern, command } of COMMAND_PATTERNS) {
    if (pattern.test(normalized)) return command;
  }
  return "unknown";
}

export class VoiceController {
  private recognition: SpeechRecognitionInstance | null = null;
  private callbacks: VoiceControlCallbacks = {};
  private muted = false;
  private listening = false;
  private shouldRestart = false;

  constructor() {
    if (typeof window !== "undefined") {
      const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;
      if (SpeechRecognition) {
        this.recognition = new SpeechRecognition();
        this.recognition.continuous = true;
        this.recognition.interimResults = false;
        this.recognition.lang = navigator.language || "en-US";
        this.setupHandlers();
      }
    }
  }

  private setupHandlers() {
    if (!this.recognition) return;

    this.recognition.onresult = (event: SpeechRecognitionEvent) => {
      const last = event.results[event.results.length - 1];
      const transcript = last[0].transcript.trim();
      this.callbacks.onTranscript?.(transcript);
      this.handleCommand(parseVoiceCommand(transcript));
    };

    this.recognition.onend = () => {
      this.listening = false;
      this.callbacks.onListeningChange?.(false);
      if (this.shouldRestart && !this.muted) {
        try {
          this.recognition?.start();
          this.listening = true;
          this.callbacks.onListeningChange?.(true);
        } catch {
          /* ignore restart errors */
        }
      }
    };

    this.recognition.onerror = () => {
      this.listening = false;
      this.callbacks.onListeningChange?.(false);
    };
  }

  setCallbacks(callbacks: VoiceControlCallbacks) {
    this.callbacks = callbacks;
  }

  startListening() {
    if (!this.recognition || this.muted) return;
    this.shouldRestart = true;
    try {
      this.recognition.start();
      this.listening = true;
      this.callbacks.onListeningChange?.(true);
    } catch {
      /* already started */
    }
  }

  stopListening() {
    this.shouldRestart = false;
    this.recognition?.stop();
    this.listening = false;
    this.callbacks.onListeningChange?.(false);
  }

  setMuted(muted: boolean) {
    this.muted = muted;
    if (muted) this.stopListening();
    else this.startListening();
  }

  isMuted(): boolean {
    return this.muted;
  }

  isListening(): boolean {
    return this.listening;
  }

  isSupported(): boolean {
    return this.recognition !== null;
  }

  speak(text: string, onEnd?: () => void) {
    if (this.muted || typeof window === "undefined" || !window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = navigator.language || "en-US";
    utterance.rate = 0.95;
    if (onEnd) utterance.onend = onEnd;
    window.speechSynthesis.speak(utterance);
  }

  stopSpeaking() {
    window.speechSynthesis?.cancel();
  }

  private handleCommand(command: VoiceCommand) {
    switch (command) {
      case "next":
        this.callbacks.onNext?.();
        break;
      case "previous":
        this.callbacks.onPrevious?.();
        break;
      case "repeat":
        this.callbacks.onRepeat?.();
        break;
      case "tools":
        this.callbacks.onTools?.();
        break;
      case "safety":
        this.callbacks.onSafety?.();
        break;
      case "help":
        this.callbacks.onHelp?.();
        break;
    }
  }
}

export const voiceController = typeof window !== "undefined" ? new VoiceController() : null;

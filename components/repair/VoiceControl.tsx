"use client";

import { useCallback, useEffect, useState } from "react";
import { Mic, MicOff, Volume2, VolumeX } from "lucide-react";
import { Button } from "@/components/ui/button";
import { VoiceController } from "@/lib/voice";
import type { RepairStep } from "@/lib/types";
import Link from "next/link";

interface VoiceControlProps {
  step: RepairStep;
  onNext: () => void;
  onPrevious: () => void;
  machineName: string;
  machineId: string;
  procedureType?: string;
}

export function VoiceControl({ step, onNext, onPrevious, machineName, machineId, procedureType }: VoiceControlProps) {
  const [listening, setListening] = useState(false);
  const [muted, setMuted] = useState(false);
  const [controller] = useState(() => new VoiceController());

  const speakStep = useCallback(() => {
    controller.speak(`Step ${step.step}. ${step.instruction}`);
  }, [controller, step.instruction, step.step]);

  useEffect(() => {
    if (!controller.isSupported()) return;

    controller.setCallbacks({
      onNext,
      onPrevious,
      onRepeat: () => speakStep(),
      onTools: () => controller.speak(`Required tool: ${step.tool_needed.replace(/_/g, " ")}`),
      onSafety: () => controller.speak(step.safety),
      onListeningChange: setListening,
    });

    if (!muted) {
      controller.startListening();
      speakStep();
    }

    return () => controller.stopListening();
  }, [controller, muted, onNext, onPrevious, speakStep, step.safety, step.tool_needed]);

  const toggleMute = () => {
    const newMuted = !muted;
    setMuted(newMuted);
    controller.setMuted(newMuted);
    if (!newMuted) speakStep();
  };

  return (
    <div className="absolute top-3 right-3 flex gap-2 z-10">
      <Button
        size="icon"
        variant="secondary"
        className={`bg-black/50 backdrop-blur ${listening ? "mic-listening" : ""}`}
        onClick={toggleMute}
      >
        {muted ? <VolumeX className="h-4 w-4" /> : <Volume2 className="h-4 w-4" />}
      </Button>
      <Button
        size="icon"
        variant="secondary"
        className={`bg-black/50 backdrop-blur ${listening && !muted ? "text-primary mic-listening" : ""}`}
      >
        {listening && !muted ? <Mic className="h-4 w-4" /> : <MicOff className="h-4 w-4" />}
      </Button>
      <Link
        href={`/chat?machineId=${encodeURIComponent(machineId)}&machine=${encodeURIComponent(machineName)}${procedureType ? `&procedure=${encodeURIComponent(procedureType)}` : ""}&step=${step.step}`}
      >
        <Button size="icon" variant="secondary" className="bg-black/50 backdrop-blur">
          ?
        </Button>
      </Link>
    </div>
  );
}

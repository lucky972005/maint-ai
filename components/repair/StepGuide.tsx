"use client";

import { useState } from "react";
import { Camera, ChevronLeft, ChevronRight, SkipForward } from "lucide-react";
import { ProgressTracker } from "./ProgressTracker";
import { ArOverlay } from "@/components/scanner/ArOverlay";
import { ToolDetector } from "@/components/scanner/ToolDetector";
import { SafetyCheck } from "./SafetyCheck";
import { VoiceControl } from "./VoiceControl";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { Machine, RepairStep } from "@/lib/types";

interface StepGuideProps {
  machine: Machine;
  steps: RepairStep[];
  currentStep: number;
  procedureType: string;
  onNext: () => void;
  onPrevious: () => void;
  onSkip: () => void;
  onComplete: () => void;
}

export function StepGuide({
  machine,
  steps,
  currentStep,
  procedureType,
  onNext,
  onPrevious,
  onSkip,
  onComplete,
}: StepGuideProps) {
  const step = steps[currentStep];
  const totalSteps = steps.length;
  const [showSafety, setShowSafety] = useState(false);
  const [showToolVerify, setShowToolVerify] = useState(false);
  const [toolVerified, setToolVerified] = useState(false);
  const [safetyConfirmed, setSafetyConfirmed] = useState(false);

  const needsSafety = step.is_dangerous || (currentStep + 1) % 3 === 0;
  const needsTool = step.requires_tool_verification && !toolVerified;

  const handleNext = () => {
    if (needsSafety && !safetyConfirmed) {
      setShowSafety(true);
      return;
    }
    if (needsTool) {
      setShowToolVerify(true);
      return;
    }
    setToolVerified(false);
    setSafetyConfirmed(false);
    if (currentStep >= totalSteps - 1) {
      onComplete();
      return;
    }
    onNext();
  };

  const handleSafetyConfirm = () => {
    setSafetyConfirmed(true);
    setShowSafety(false);
    if (needsTool) {
      setShowToolVerify(true);
      return;
    }

    setToolVerified(false);
    if (currentStep >= totalSteps - 1) {
      onComplete();
    } else {
      onNext();
    }
  };

  return (
    <div className="flex min-h-[calc(100vh-64px)] flex-col">
      <ProgressTracker current={currentStep + 1} total={totalSteps} procedureType={procedureType} />

      <Card className="mx-4 mt-3 border-primary/20">
        <CardContent className="flex items-center gap-3 p-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-muted text-xs font-semibold text-primary">
            STEP
          </div>
          <div className="min-w-0 flex-1">
            <p className="truncate font-medium">{machine.name}</p>
            <p className="text-xs text-muted-foreground">{machine.model} - {machine.location}</p>
          </div>
          <Badge variant={machine.status === "operational" ? "success" : "warning"}>{machine.status}</Badge>
        </CardContent>
      </Card>

      <div className="relative mx-4 mt-3 min-h-[300px] flex-1 overflow-hidden rounded-lg border border-border">
        <ArOverlay markers={[step.ar_marker]} fallbackImage={machine.image_url ?? undefined} />
        <VoiceControl
          step={step}
          onNext={handleNext}
          onPrevious={onPrevious}
          machineName={machine.name}
          machineId={machine.id}
          procedureType={procedureType}
        />
      </div>

      <div className="space-y-3 p-4">
        <div className="flex items-start justify-between">
          <div>
            <p className="text-xs font-medium text-primary">Step {step.step}</p>
            <p className="mt-1 text-base">{step.instruction}</p>
          </div>
        </div>

        <div className="flex flex-wrap gap-2 text-xs">
          <Badge variant="outline">Tool: {step.tool_needed.replace(/_/g, " ")}</Badge>
          <Badge variant="outline">Safety: {step.safety.slice(0, 40)}...</Badge>
        </div>

        <Button variant="outline" size="sm" className="w-full">
          <Camera className="h-4 w-4" />
          Document this step
        </Button>

        <div className="flex gap-2">
          <Button variant="outline" onClick={onPrevious} disabled={currentStep === 0} className="flex-1">
            <ChevronLeft className="h-4 w-4" />
            Previous
          </Button>
          <Button onClick={handleNext} className="orange-glow flex-1">
            Next
            <ChevronRight className="h-4 w-4" />
          </Button>
          <Button variant="ghost" onClick={onSkip} disabled={currentStep >= totalSteps - 1}>
            <SkipForward className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <SafetyCheck
        open={showSafety}
        warnings={[step.safety, "Ensure lockout/tagout is applied", "Wear appropriate PPE"]}
        onConfirm={handleSafetyConfirm}
        onCancel={() => setShowSafety(false)}
      />

      {showToolVerify && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/95 p-4">
          <div className="w-full max-w-md">
            <ToolDetector
              expectedTool={step.tool_needed}
              onVerified={() => {
                setShowToolVerify(false);
                setToolVerified(true);
                if (currentStep >= totalSteps - 1) onComplete();
                else onNext();
              }}
              onSkip={() => {
                setShowToolVerify(false);
                if (currentStep >= totalSteps - 1) onComplete();
                else onNext();
              }}
            />
            <Button variant="ghost" className="mt-4 w-full" onClick={() => setShowToolVerify(false)}>
              Cancel
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}

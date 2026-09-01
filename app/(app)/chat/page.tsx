"use client";

import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { AppShell } from "@/components/layout/app-shell";
import { ChatWidget } from "@/components/chat/ChatWidget";
import { getMachineById } from "@/lib/demo-data";

function ChatContent() {
  const searchParams = useSearchParams();
  const machineId = searchParams.get("machineId") ?? undefined;
  const machineName = searchParams.get("machine") ?? undefined;
  const procedure = searchParams.get("procedure") ?? undefined;
  const step = searchParams.get("step") ?? undefined;
  const machine = machineId ? getMachineById(machineId) : undefined;
  const context = machine ? `${machine.name} (${machine.model ?? machine.category})` : machineName;
  const sessionContext = [procedure ? `Procedure ${procedure}` : null, step ? `Step ${step}` : null]
    .filter(Boolean)
    .join(" - ");

  return (
    <ChatWidget
      machineId={machine?.id ?? machineId}
      machineContext={context}
      sessionContext={sessionContext || undefined}
      fullPage
    />
  );
}

export default function ChatPage() {
  return (
    <AppShell title="FixBot">
      <Suspense fallback={<div className="p-4">Loading chat...</div>}>
        <ChatContent />
      </Suspense>
    </AppShell>
  );
}

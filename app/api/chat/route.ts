import { NextResponse } from "next/server";
import { generateTextResponse, isAIConfigured } from "@/lib/ai";

export const dynamic = "force-dynamic";

const DEMO_RESPONSES: Record<string, string> = {
  overheating:
    "Motor overheating is commonly caused by:\n\n1. **Blocked ventilation** - Clean cooling fans and vents\n2. **Overloading** - Check if machine exceeds rated capacity\n3. **Bearing failure** - Inspect bearings for wear; replace if noisy\n\n**Torque spec for M8 bolts:** 25-30 Nm\n\nRecommended: Run motor inspection procedure and check insulation resistance with multimeter (>1 Mohm).",
  torque:
    "Standard torque specifications:\n\n- **M6 bolts:** 10-12 Nm\n- **M8 bolts:** 25-30 Nm\n- **M10 bolts:** 45-50 Nm\n- **Belt tension:** 15-20 lbs deflection at midpoint\n\nAlways use a calibrated torque wrench. Refer to machine manual for model-specific values.",
  wiring:
    "For electrical wiring inspection:\n\n1. De-energize and lockout\n2. Check wire colors: Red=phase, Blue=neutral, Green/Yellow=ground\n3. Verify terminal tightness (0.5-0.7 Nm for control wiring)\n4. Test insulation resistance >1 Mohm\n\nWarning: Only qualified electricians should work on live circuits.",
};

function getDemoResponse(content: string, machineContext?: string): string {
  const lower = content.toLowerCase();
  const prefix = machineContext ? `Regarding your **${machineContext}**:\n\n` : "";

  if (lower.includes("overheat")) return prefix + DEMO_RESPONSES.overheating;
  if (lower.includes("torque")) return prefix + DEMO_RESPONSES.torque;
  if (lower.includes("wiring") || lower.includes("diagram")) return prefix + DEMO_RESPONSES.wiring;
  if (lower.includes("belt")) {
    return (
      prefix +
      "Belt replacement steps:\n\n1. Lockout/tagout the machine\n2. Release belt tension\n3. Remove old belt, inspect pulleys\n4. Install new belt with proper alignment\n5. Adjust tension (15-20 lbs deflection)\n6. Test run and verify tracking"
    );
  }

  return (
    prefix +
    "I can help with maintenance procedures, troubleshooting, torque specs, and safety guidelines. Try asking about:\n- Motor overheating\n- Torque specifications\n- Wiring diagrams\n- Belt replacement"
  );
}

export async function POST(req: Request) {
  try {
    const { messages, machineContext } = await req.json();
    const lastMessage = messages[messages.length - 1]?.content ?? "";

    if (isAIConfigured()) {
      try {
        const systemPrompt = `You are FixBot, an expert industrial maintenance AI assistant. ${machineContext ? `The technician is currently working on: ${machineContext}.` : ""} Provide concise, practical advice. Use markdown for formatting. Include safety warnings when relevant. Suggest specific tools and procedures.`;

        const message = await generateTextResponse(
          [{ role: "system", content: systemPrompt }, ...messages],
          800
        );
        const suggestions = ["What tools do I need?", "Show safety warnings", "What's the next step?"];

        return NextResponse.json({ message, suggestions });
      } catch (aiError) {
        console.error("AI API error, falling back to demo:", aiError);
        // Fall through to demo response
      }
    }

    const message = getDemoResponse(lastMessage, machineContext);
    const suggestions = ["What's the torque spec?", "Show safety warnings", "Why is my motor overheating?"];

    return NextResponse.json({ message, suggestions });
  } catch (error) {
    console.error("chat error:", error);
    return NextResponse.json({
      message: "I'm having trouble connecting right now. Please check your connection and try again.",
      suggestions: [],
    });
  }
}

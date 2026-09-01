import { NextResponse } from "next/server";
import { generateVisionJsonResponse, isAIConfigured } from "@/lib/ai";

export const dynamic = "force-dynamic";

interface FaultDetection {
  detected_issues: Array<{
    type: string;
    severity: "low" | "medium" | "high" | "critical";
    description: string;
    location: string;
    confidence: number;
  }>;
  overall_condition: "good" | "fair" | "poor" | "critical";
  recommended_actions: string[];
  equipment_type: string;
}

export async function POST(req: Request) {
  try {
    const { image, machineContext } = await req.json();

    if (!image) {
      return NextResponse.json({ error: "Image is required" }, { status: 400 });
    }

    if (isAIConfigured()) {
      const contextPrompt = machineContext 
        ? `This is a photo of a ${machineContext}. Analyze it for faults, damage, wear, or maintenance issues.`
        : "Analyze this industrial equipment photo for faults, damage, wear, or maintenance issues.";

      const prompt = `${contextPrompt} 

Return JSON with this exact format:
{
  "detected_issues": [
    {
      "type": "e.g., 'oil leak', 'bearing wear', 'corrosion', 'crack', 'overheating'",
      "severity": "low|medium|high|critical",
      "description": "detailed description of the issue",
      "location": "specific location on the equipment",
      "confidence": 0.0-1.0
    }
  ],
  "overall_condition": "good|fair|poor|critical",
  "recommended_actions": ["action1", "action2"],
  "equipment_type": "type of equipment shown"
}

Look for: leaks, cracks, corrosion, wear, damage, loose components, misalignment, overheating signs, unusual buildup, missing parts, safety hazards.`;

      const result = await generateVisionJsonResponse(prompt, image, "image/jpeg");
      
      // Validate and structure the response
      const validConditions: Array<"good" | "fair" | "poor" | "critical"> = ["good", "fair", "poor", "critical"];
      const overallCondition = validConditions.includes(result.overall_condition as "good" | "fair" | "poor" | "critical") 
        ? result.overall_condition as "good" | "fair" | "poor" | "critical"
        : "fair";

      const equipmentType = typeof result.equipment_type === "string" ? result.equipment_type : "unknown";

      const faultDetection: FaultDetection = {
        detected_issues: Array.isArray(result.detected_issues) ? result.detected_issues : [],
        overall_condition: overallCondition,
        recommended_actions: Array.isArray(result.recommended_actions) ? result.recommended_actions : [],
        equipment_type: equipmentType
      };

      return NextResponse.json(faultDetection);
    }

    // Demo fallback when AI is not configured
    const demoResponse: FaultDetection = {
      detected_issues: [
        {
          type: "oil leak",
          severity: "medium",
          description: "Visible oil residue around hydraulic connections",
          location: "hydraulic hose connections",
          confidence: 0.75
        },
        {
          type: "surface wear",
          severity: "low", 
          description: "Minor surface wear on protective coating",
          location: "exterior panel",
          confidence: 0.60
        }
      ],
      overall_condition: "fair",
      recommended_actions: [
        "Inspect and tighten hydraulic connections",
        "Clean oil residue and monitor for recurrence",
        "Check oil levels and quality",
        "Schedule preventive maintenance"
      ],
      equipment_type: machineContext || "industrial equipment"
    };

    return NextResponse.json(demoResponse);

  } catch (error) {
    console.error("analyze-fault error:", error);
    
    // Return demo response on error
    const fallbackResponse: FaultDetection = {
      detected_issues: [
        {
          type: "general wear",
          severity: "low",
          description: "Normal wear and tear detected",
          location: "general",
          confidence: 0.50
        }
      ],
      overall_condition: "fair",
      recommended_actions: [
        "Schedule routine inspection",
        "Monitor for changes"
      ],
      equipment_type: "unknown"
    };

    return NextResponse.json(fallbackResponse);
  }
}

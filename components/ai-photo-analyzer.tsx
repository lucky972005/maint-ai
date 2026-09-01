"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Loader2, Brain, Camera, CheckCircle2, AlertTriangle } from "lucide-react";
import { toast } from "@/hooks/use-toast";

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

interface AiPhotoAnalyzerProps {
  onAnalysisComplete: (results: FaultDetection) => void;
  machineContext?: string;
  disabled?: boolean;
}

export function AiPhotoAnalyzer({ onAnalysisComplete, machineContext, disabled = false }: AiPhotoAnalyzerProps) {
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults] = useState<FaultDetection | null>(null);

  const handlePhotoUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (!file.type.startsWith("image/")) {
      toast({ title: "Invalid file", description: "Please upload an image file", variant: "destructive" });
      return;
    }

    setAnalyzing(true);
    setResults(null);

    try {
      const base64 = await fileToBase64(file);
      const response = await fetch("/api/analyze-fault", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: base64, machineContext }),
      });

      const data: FaultDetection = await response.json();
      setResults(data);
      onAnalysisComplete(data);
      toast({ title: "Analysis Complete", description: `Detected ${data.detected_issues.length} issue(s)` });
    } catch (error) {
      console.error("AI analysis failed:", error);
      toast({ title: "Analysis Failed", description: "Could not analyze the photo", variant: "destructive" });
    } finally {
      setAnalyzing(false);
    }
  };

  const fileToBase64 = (file: File) =>
    new Promise<string>((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const result = reader.result as string;
        resolve(result.split(",")[1] ?? "");
      };
      reader.onerror = () => reject(new Error("Failed to read file"));
      reader.readAsDataURL(file);
    });

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "critical": return "destructive";
      case "high": return "warning";
      case "medium": return "secondary";
      case "low": return "outline";
      default: return "outline";
    }
  };

  const getConditionColor = (condition: string) => {
    switch (condition) {
      case "critical": return "destructive";
      case "poor": return "warning";
      case "fair": return "secondary";
      case "good": return "outline";
      default: return "outline";
    }
  };

  return (
    <Card className="border-border/70">
      <CardHeader>
        <CardTitle className="text-lg flex items-center gap-2">
          <Brain className="h-5 w-5 text-primary" />
          AI Photo Analysis
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          Upload a photo to automatically detect faults and issues
        </p>
      </CardHeader>
      <CardContent className="space-y-4">
        <label>
          <input
            type="file"
            accept="image/*"
            capture="environment"
            className="hidden"
            onChange={handlePhotoUpload}
            disabled={disabled || analyzing}
          />
          <Button variant="outline" className="w-full" asChild disabled={disabled || analyzing}>
            <span>
              {analyzing ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Camera className="h-4 w-4 mr-2" />
                  Take Photo or Upload
                </>
              )}
            </span>
          </Button>
        </label>

        {results && (
          <div className="space-y-3 animate-in fade-in slide-in-from-top-2">
            <div className="flex items-center justify-between p-3 bg-background/50 rounded-lg">
              <span className="text-sm">Equipment:</span>
              <Badge variant="outline">{results.equipment_type}</Badge>
            </div>
            <div className="flex items-center justify-between p-3 bg-background/50 rounded-lg">
              <span className="text-sm">Condition:</span>
              <Badge variant={getConditionColor(results.overall_condition)}>
                {results.overall_condition}
              </Badge>
            </div>

            {results.detected_issues.length > 0 && (
              <div className="space-y-2">
                <p className="text-sm font-medium flex items-center gap-2">
                  <AlertTriangle className="h-4 w-4 text-warning" />
                  Detected Issues ({results.detected_issues.length})
                </p>
                {results.detected_issues.map((issue, i) => (
                  <div key={i} className="p-3 bg-background/50 rounded-lg space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="font-medium text-sm">{issue.type}</span>
                      <Badge variant={getSeverityColor(issue.severity)} className="text-xs">
                        {issue.severity}
                      </Badge>
                    </div>
                    <p className="text-xs text-muted-foreground">{issue.description}</p>
                    <p className="text-xs text-muted-foreground">📍 {issue.location}</p>
                    <div className="flex items-center gap-2 text-xs text-muted-foreground">
                      <CheckCircle2 className="h-3 w-3" />
                      {Math.round(issue.confidence * 100)}% confidence
                    </div>
                  </div>
                ))}
              </div>
            )}

            {results.recommended_actions.length > 0 && (
              <div className="space-y-2">
                <p className="text-sm font-medium">Recommended Actions:</p>
                <ul className="text-xs space-y-1 list-disc list-inside text-muted-foreground">
                  {results.recommended_actions.map((action, i) => (
                    <li key={i}>{action}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

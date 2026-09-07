"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import {
  Loader2,
  Upload,
  CheckCircle2,
  AlertCircle,
  Wrench,
  Clock,
  ArrowRight,
  Sparkles,
  MapPin,
  RotateCcw,
  FileText,
  AlertTriangle,
  Building,
  Gauge,
  Layers,
} from "lucide-react";
import { CameraView } from "./CameraView";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface ProcedureItem {
  id: string;
  procedure_type: string;
  estimated_minutes: number;
  difficulty: "easy" | "medium" | "hard";
  steps_count?: number;
}

interface Match {
  id: string;
  name: string;
  model: string;
  category: string;
  manufacturer?: string;
  location?: string;
  status?: string;
  confidence: number;
  reasoning?: string;
  detected_features?: string[];
  image_url?: string;
  specs?: Record<string, string | number>;
  procedures?: ProcedureItem[];
}

export function AiIdentifier() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [capturedImage, setCapturedImage] = useState<string | null>(null);
  const [matches, setMatches] = useState<Match[]>([]);
  const [identifiedType, setIdentifiedType] = useState<string>("");
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const identify = async (dataUrl: string) => {
    setLoading(true);
    setCapturedImage(dataUrl);
    setMatches([]);
    setErrorMessage(null);
    setSelectedIndex(0);

    try {
      const parts = dataUrl.split(",");
      const mimeMatch = parts[0]?.match(/:(.*?);/);
      const mimeType = mimeMatch ? mimeMatch[1] : "image/jpeg";
      const base64 = parts[1];

      const res = await fetch("/api/identify-machine", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: base64, mimeType }),
      });

      const data = await res.json();

      if (!res.ok || data.error) {
        setErrorMessage(data.details || data.error || "Failed to analyze image");
        return;
      }

      if (data.matches && data.matches.length > 0) {
        setMatches(data.matches);
        setIdentifiedType(data.identified_type || "Industrial Machine");
      } else {
        setErrorMessage(
          data.message ||
            "No registered machine matched this image. Try capturing a clear photo showing the whole unit or nameplate."
        );
      }
    } catch (err) {
      console.error("AI identification error:", err);
      setErrorMessage("Network error during identification. Please check your connection and retry.");
    } finally {
      setLoading(false);
    }
  };

  const handleGalleryUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => identify(reader.result as string);
    reader.readAsDataURL(file);
  };

  const handleReset = () => {
    setCapturedImage(null);
    setMatches([]);
    setIdentifiedType("");
    setErrorMessage(null);
    setSelectedIndex(0);
  };

  const activeMatch = matches[selectedIndex] ?? matches[0];

  return (
    <div className="flex min-h-[440px] flex-col lg:min-h-[640px]">
      {/* Top Camera or Captured Snapshot View */}
      <div className="relative flex-1 min-h-[300px] bg-black/90">
        {!capturedImage ? (
          <CameraView onCapture={identify} className="h-full min-h-[300px]" />
        ) : (
          <div className="relative h-full min-h-[300px] flex items-center justify-center overflow-hidden bg-black">
            <img
              src={capturedImage}
              alt="Captured equipment"
              className="max-h-[340px] w-full object-contain"
            />
            <Button
              size="sm"
              variant="secondary"
              className="absolute top-3 right-3 gap-1.5 shadow-lg bg-background/80 backdrop-blur"
              onClick={handleReset}
            >
              <RotateCcw className="h-3.5 w-3.5" />
              Retake
            </Button>
          </div>
        )}

        {/* Loading overlay with clear feedback */}
        {loading && (
          <div className="absolute inset-0 bg-black/80 backdrop-blur-sm flex flex-col items-center justify-center p-6 text-center z-10">
            <div className="relative mb-4">
              <div className="absolute -inset-2 rounded-full bg-primary/20 animate-ping" />
              <div className="relative rounded-full p-3 bg-primary/10 border border-primary/40">
                <Loader2 className="h-8 w-8 text-primary animate-spin" />
              </div>
            </div>
            <p className="text-base font-semibold text-white">Matching Against Database...</p>
            <p className="text-xs text-muted-foreground mt-1 max-w-xs">
              Gemini Vision is analyzing visual features against 20 registered factory machines.
            </p>
          </div>
        )}
      </div>

      {/* Action / Results Panel */}
      <div className="p-4 sm:p-5 space-y-4 bg-card border-t border-border">
        {/* If no match yet and not loading, show capture / upload button */}
        {!matches.length && !loading && !errorMessage && (
          <div className="space-y-3">
            <p className="text-sm text-muted-foreground text-center">
              Point at any factory machine and capture, or upload from your device
            </p>
            <label className="block">
              <input type="file" accept="image/*" className="hidden" onChange={handleGalleryUpload} />
              <Button variant="outline" className="w-full gap-2 rounded-xl" asChild>
                <span>
                  <Upload className="h-4 w-4" />
                  Upload Machine Photo
                </span>
              </Button>
            </label>
          </div>
        )}

        {/* Error / No Match Found View */}
        {errorMessage && !loading && (
          <div className="rounded-2xl border border-destructive/40 bg-destructive/10 p-4 space-y-3">
            <div className="flex items-start gap-3">
              <AlertCircle className="h-5 w-5 text-destructive mt-0.5 shrink-0" />
              <div className="space-y-1">
                <p className="text-sm font-semibold text-destructive">No Confident Match</p>
                <p className="text-xs text-muted-foreground">{errorMessage}</p>
              </div>
            </div>
            <div className="flex gap-2 pt-1">
              <Button size="sm" variant="outline" className="rounded-xl gap-1.5" onClick={handleReset}>
                <RotateCcw className="h-3.5 w-3.5" />
                Scan Again
              </Button>
              <label className="inline-block">
                <input type="file" accept="image/*" className="hidden" onChange={handleGalleryUpload} />
                <Button size="sm" variant="secondary" className="rounded-xl gap-1.5" asChild>
                  <span>
                    <Upload className="h-3.5 w-3.5" />
                    Upload Another Photo
                  </span>
                </Button>
              </label>
            </div>
          </div>
        )}

        {/* Detected Match & Interactive Menu */}
        {matches.length > 0 && activeMatch && (
          <div className="space-y-4 animate-in fade-in slide-in-from-bottom-3 duration-300">
            {/* Alternative matches selector tabs */}
            {matches.length > 1 && (
              <div className="flex items-center gap-2 overflow-x-auto pb-1">
                <span className="text-xs text-muted-foreground whitespace-nowrap">Matches:</span>
                {matches.map((m, idx) => (
                  <button
                    key={m.id}
                    onClick={() => setSelectedIndex(idx)}
                    className={`text-xs px-3 py-1.5 rounded-full font-medium transition-all whitespace-nowrap border ${
                      selectedIndex === idx
                        ? "bg-primary text-primary-foreground border-primary shadow-sm"
                        : "bg-muted/70 text-muted-foreground border-border hover:border-primary/50"
                    }`}
                  >
                    #{idx + 1} {m.name} ({Math.round(m.confidence * 100)}%)
                  </button>
                ))}
              </div>
            )}

            {/* Primary Match Card */}
            <Card className="border-primary/40 bg-gradient-to-br from-primary/10 via-card to-card shadow-lg shadow-primary/5">
              <CardContent className="p-4 space-y-3.5">
                {/* Header status row */}
                <div className="flex items-start justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <Badge
                      variant={
                        activeMatch.confidence >= 0.85
                          ? "success"
                          : activeMatch.confidence >= 0.65
                          ? "warning"
                          : "secondary"
                      }
                      className="px-2.5 py-1 text-xs gap-1 font-semibold"
                    >
                      <Sparkles className="h-3 w-3" />
                      {Math.round(activeMatch.confidence * 100)}% Match
                    </Badge>
                    {activeMatch.category && (
                      <Badge variant="outline" className="text-xs">
                        {activeMatch.category}
                      </Badge>
                    )}
                  </div>

                  <Badge
                    variant={
                      activeMatch.status === "operational"
                        ? "success"
                        : activeMatch.status === "broken"
                        ? "destructive"
                        : "warning"
                    }
                    className="capitalize text-xs"
                  >
                    {activeMatch.status || "operational"}
                  </Badge>
                </div>

                {/* Machine title & details */}
                <div className="flex items-start gap-3">
                  {activeMatch.image_url ? (
                    <img
                      src={activeMatch.image_url}
                      alt={activeMatch.name}
                      className="h-16 w-16 shrink-0 rounded-xl object-cover border border-border bg-muted shadow-sm"
                    />
                  ) : (
                    <div className="h-16 w-16 shrink-0 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center">
                      <Gauge className="h-8 w-8 text-primary" />
                    </div>
                  )}

                  <div className="min-w-0 flex-1">
                    <h3 className="text-lg font-bold truncate">{activeMatch.name}</h3>
                    <p className="text-sm font-medium text-primary truncate">{activeMatch.model}</p>
                    <div className="flex flex-wrap items-center gap-x-3 gap-y-1 mt-1 text-xs text-muted-foreground">
                      {activeMatch.manufacturer && (
                        <span className="flex items-center gap-1">
                          <Building className="h-3 w-3" />
                          {activeMatch.manufacturer}
                        </span>
                      )}
                      {activeMatch.location && (
                        <span className="flex items-center gap-1">
                          <MapPin className="h-3 w-3" />
                          {activeMatch.location}
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                {/* AI Reasoning & Visual Evidence */}
                {activeMatch.reasoning && (
                  <div className="rounded-xl border border-border/80 bg-background/70 p-3 space-y-2 text-xs">
                    <div className="flex items-center gap-1.5 font-medium text-foreground/90">
                      <Sparkles className="h-3.5 w-3.5 text-primary" />
                      <span>AI Detection Evidence</span>
                    </div>
                    <p className="text-muted-foreground leading-relaxed">{activeMatch.reasoning}</p>

                    {activeMatch.detected_features && activeMatch.detected_features.length > 0 && (
                      <div className="flex flex-wrap gap-1.5 pt-1">
                        {activeMatch.detected_features.map((feat, i) => (
                          <span
                            key={i}
                            className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-muted/80 text-[11px] text-muted-foreground border border-border/50"
                          >
                            <CheckCircle2 className="h-2.5 w-2.5 text-primary" />
                            {feat}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Machine Operations Menu */}
            <div className="space-y-2.5">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-1.5">
                  <Wrench className="h-4 w-4 text-primary" />
                  <p className="text-sm font-semibold">Available Maintenance Procedures</p>
                </div>
                {activeMatch.procedures && (
                  <span className="text-xs text-muted-foreground">
                    {activeMatch.procedures.length} procedures
                  </span>
                )}
              </div>

              {/* Procedures List */}
              {activeMatch.procedures && activeMatch.procedures.length > 0 ? (
                <div className="grid gap-2 sm:grid-cols-2">
                  {activeMatch.procedures.map((proc) => (
                    <Card
                      key={proc.id}
                      className="group cursor-pointer hover:border-primary/70 transition-all duration-200 hover:shadow-md bg-card/90"
                      onClick={() =>
                        router.push(`/repair/${activeMatch.id}/step/1?procedure=${proc.id}`)
                      }
                    >
                      <CardContent className="p-3 flex items-center justify-between gap-3">
                        <div className="min-w-0">
                          <p className="text-sm font-medium group-hover:text-primary transition-colors truncate">
                            {proc.procedure_type}
                          </p>
                          <div className="flex items-center gap-2 mt-0.5 text-xs text-muted-foreground">
                            <span className="flex items-center gap-1">
                              <Clock className="h-3 w-3" />
                              {proc.estimated_minutes} min
                            </span>
                            <span>•</span>
                            <Badge
                              variant={
                                proc.difficulty === "easy"
                                  ? "outline"
                                  : proc.difficulty === "medium"
                                  ? "secondary"
                                  : "destructive"
                              }
                              className="text-[10px] px-1.5 py-0 capitalize"
                            >
                              {proc.difficulty}
                            </Badge>
                          </div>
                        </div>

                        <Button
                          size="sm"
                          variant="ghost"
                          className="h-8 w-8 p-0 shrink-0 rounded-full group-hover:bg-primary group-hover:text-primary-foreground transition-colors"
                        >
                          <ArrowRight className="h-4 w-4" />
                        </Button>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-muted-foreground">
                  No standard procedures registered for this unit.
                </p>
              )}

              {/* Quick Actions Footer */}
              <div className="pt-2 grid grid-cols-2 sm:grid-cols-3 gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  className="rounded-xl text-xs gap-1.5"
                  onClick={() => router.push(`/repair/${activeMatch.id}`)}
                >
                  <Layers className="h-3.5 w-3.5 text-primary" />
                  Full Repair Hub
                </Button>

                <Button
                  variant="outline"
                  size="sm"
                  className="rounded-xl text-xs gap-1.5"
                  onClick={() => router.push(`/report?machineId=${activeMatch.id}`)}
                >
                  <AlertTriangle className="h-3.5 w-3.5 text-destructive" />
                  Report Fault
                </Button>

                <Button
                  variant="ghost"
                  size="sm"
                  className="rounded-xl text-xs gap-1.5 col-span-2 sm:col-span-1"
                  onClick={handleReset}
                >
                  <RotateCcw className="h-3.5 w-3.5" />
                  Scan Another
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

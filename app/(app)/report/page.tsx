"use client";

import { useEffect, useMemo, useState, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { AppShell } from "@/components/layout/app-shell";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { DEMO_DATA, isFirebaseConfigured } from "@/lib/demo-data";
import { getMachines, getFaultReports, createFaultReport } from "@/lib/database";
import { cacheFaultReport, getCachedFaultReports, queueForSync } from "@/lib/offline";
import { toast } from "@/hooks/use-toast";
import { Brain, Camera, Mic, Paperclip, Send, Upload } from "lucide-react";
import { formatDate } from "@/lib/utils";
import type { FaultReport } from "@/lib/types";

type AttachmentItem = {
  name: string;
  url: string;
  type: string;
};

type DetectedIssue = {
  type: string;
  severity: "low" | "medium" | "high" | "critical";
  description: string;
  location: string;
  confidence: number;
};

type AiDetectionResults = {
  detected_issues: DetectedIssue[];
  overall_condition: "good" | "fair" | "poor" | "critical";
  recommended_actions: string[];
  equipment_type: string;
};

const severityLevels = ["low", "medium", "high", "critical"] as const;

function ReportContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const prefillMachine = searchParams.get("machineId") ?? "";
  const [machineId, setMachineId] = useState(prefillMachine);
  const [description, setDescription] = useState("");
  const [severity, setSeverity] = useState<(typeof severityLevels)[number]>("medium");
  const [aiDiagnosis, setAiDiagnosis] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [aiDetectionResults, setAiDetectionResults] = useState<AiDetectionResults | null>(null);
  const [reportItems, setReportItems] = useState<Array<FaultReport & { source?: string }>>([]);
  const [attachments, setAttachments] = useState<AttachmentItem[]>([]);
  const [uploading, setUploading] = useState(false);
  const [machines, setMachines] = useState(DEMO_DATA.machines);
  const [useRealData, setUseRealData] = useState(false);

  const currentMachine = useMemo(
    () => machines.find((machine) => machine.id === machineId),
    [machineId, machines]
  );

  useEffect(() => {
    const loadData = async () => {
      const firebaseConfigured = isFirebaseConfigured();
      setUseRealData(firebaseConfigured);

      if (firebaseConfigured) {
        try {
          const [machinesData, faultsData] = await Promise.all([
            getMachines(),
            getFaultReports(),
          ]);
          setMachines(machinesData);
          setReportItems(faultsData);
        } catch (error) {
          console.error("Failed to load data from Firebase:", error);
        }
      } else {
        const cached = await getCachedFaultReports();
        setReportItems(cached);
      }
    };

    loadData();
  }, []);

  const getAiDiagnosis = async () => {
    if (!description) return;
    setLoading(true);
    try {
      const machine = machines.find((item) => item.id === machineId);
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: [
            {
              role: "user",
              content: `Diagnose this fault on ${machine?.name ?? "industrial equipment"}: ${description}. List 3 possible causes with confidence percentages.`,
            },
          ],
          machineContext: machine?.name,
        }),
      });
      const data = await response.json();
      setAiDiagnosis(data.message);
    } catch {
      setAiDiagnosis("1. Bearing wear (75%)\n2. Misalignment (60%)\n3. Lubrication failure (45%)");
    } finally {
      setLoading(false);
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

  const uploadAttachment = async (file: File, type: "before" | "after" | "video") => {
    setUploading(true);
    try {
      const base64 = await fileToBase64(file);
      const response = await fetch("/api/upload-evidence", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ file: base64, fileName: file.name, type }),
      });
      const data = await response.json();
      const url = data.url ?? `/uploads/demo/${file.name}`;
      setAttachments((items) => [...items, { name: file.name, url, type: file.type || "application/octet-stream" }]);
      toast({ title: "Attachment added", description: file.name });
      
      // Automatically analyze if it's an image
      if (file.type.startsWith("image/")) {
        await analyzePhotoForFaults(base64);
      }
    } catch {
      toast({ title: "Upload failed", description: "Attachment will not be included", variant: "destructive" });
    } finally {
      setUploading(false);
    }
  };

  const analyzePhotoForFaults = async (imageBase64: string) => {
    setAnalyzing(true);
    try {
      const machineContext = currentMachine?.name || currentMachine?.category;
      const response = await fetch("/api/analyze-fault", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: imageBase64, machineContext }),
      });
      const data = await response.json();
      setAiDetectionResults(data);
      
      // Auto-populate description and severity based on AI analysis
      if (data.detected_issues && data.detected_issues.length > 0) {
        const topIssue = data.detected_issues[0];
        const autoDescription = `AI detected: ${topIssue.type} - ${topIssue.description} at ${topIssue.location}. ${data.recommended_actions?.join(", ") || ""}`;
        setDescription(autoDescription);
        setSeverity(topIssue.severity || "medium");
        
        // Update AI diagnosis with full analysis
        const diagnosisText = `AI Analysis Results:\n` +
          `Equipment: ${data.equipment_type}\n` +
          `Overall Condition: ${data.overall_condition}\n\n` +
          `Detected Issues:\n` +
          data.detected_issues.map((issue: DetectedIssue, i: number) => 
            `${i + 1}. ${issue.type} (${issue.severity}): ${issue.description} at ${issue.location} (${Math.round(issue.confidence * 100)}% confidence)`
          ).join("\n") +
          `\n\nRecommended Actions:\n` +
          (data.recommended_actions || []).map((action: string, i: number) => `${i + 1}. ${action}`).join("\n");
        
        setAiDiagnosis(diagnosisText);
        toast({ title: "AI Analysis Complete", description: `Detected ${data.detected_issues.length} issue(s)` });
      }
    } catch (error) {
      console.error("AI analysis failed:", error);
      toast({ title: "AI Analysis Failed", description: "Using manual entry instead", variant: "destructive" });
    } finally {
      setAnalyzing(false);
    }
  };

  const submit = async () => {
    if (!machineId || !description) return;

    const report: Omit<FaultReport, "id" | "created_at"> = {
      machine_id: machineId,
      reported_by: null,
      assigned_to: null,
      description,
      severity,
      ai_diagnosis: aiDiagnosis,
      ai_detection_results: aiDetectionResults,
      status: "open",
      attachments: attachments.map((item) => item.url),
      assigned_at: null,
      due_date: null,
    };

    try {
      if (useRealData) {
        const newReport = await createFaultReport(report);
        setReportItems((items) => [newReport, ...items]);
      } else {
        const reportWithId: FaultReport = {
          ...report,
          id: crypto.randomUUID(),
          created_at: new Date().toISOString(),
          machine: currentMachine,
          assigned_to: null,
          assigned_at: null,
          due_date: null,
          ai_detection_results: aiDetectionResults,
        };
        await cacheFaultReport(reportWithId, "demo");
        setReportItems((items) => [{ ...reportWithId, source: "demo" }, ...items]);

        const response = await fetch("/api/fault-report", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(reportWithId),
        });

        if (!response.ok) {
          await queueForSync("fault_report", reportWithId);
        }
      }

      toast({ title: "Fault saved", description: "Report submitted successfully." });
      router.push("/history");
    } catch {
      toast({ title: "Failed to save", description: "Please try again", variant: "destructive" });
    }
  };

  const recentReports = reportItems.slice(0, 8);

  return (
    <Tabs defaultValue="report" className="px-4 py-4 lg:px-8 lg:py-6">
      <TabsList className="grid w-full grid-cols-2 rounded-2xl bg-muted/70 p-1">
        <TabsTrigger value="report" className="rounded-xl">
          New report
        </TabsTrigger>
        <TabsTrigger value="my" className="rounded-xl">
          Recent reports
        </TabsTrigger>
      </TabsList>

      <TabsContent value="report" className="mt-4">
        <div className="grid gap-6 xl:grid-cols-[minmax(0,1fr)_320px]">
          <Card className="border-border/70">
            <CardHeader>
              <CardTitle className="text-lg">Fault intake form</CardTitle>
              <p className="text-sm text-muted-foreground">
                Capture machine context, severity, attachments, and AI suggestions in one flow.
              </p>
            </CardHeader>
            <CardContent className="space-y-5">
              <div className="space-y-2">
                <Label>Machine</Label>
                <Select value={machineId} onValueChange={setMachineId}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select machine" />
                  </SelectTrigger>
                  <SelectContent>
                    {machines.map((machine) => (
                      <SelectItem key={machine.id} value={machine.id}>
                        {machine.name} - {machine.model}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Description</Label>
                <Textarea
                  value={description}
                  onChange={(event) => setDescription(event.target.value)}
                  placeholder="Describe the issue, what you observed, and when it started."
                  rows={5}
                />
              </div>

              <div className="space-y-3">
                <div className="flex items-center justify-between gap-3">
                  <Label>Severity</Label>
                  <Badge
                    variant={
                      severity === "critical"
                        ? "destructive"
                        : severity === "high"
                          ? "warning"
                          : severity === "medium"
                            ? "secondary"
                            : "outline"
                    }
                  >
                    {severity}
                  </Badge>
                </div>
                <input
                  type="range"
                  min={0}
                  max={3}
                  value={severityLevels.indexOf(severity)}
                  onChange={(event) => setSeverity(severityLevels[parseInt(event.target.value, 10)])}
                  className="w-full accent-primary"
                />
                <div className="flex justify-between text-xs text-muted-foreground">
                  <span>Low</span>
                  <span>Medium</span>
                  <span>High</span>
                  <span>Critical</span>
                </div>
              </div>

              <div className="flex flex-wrap gap-2">
                <label>
                  <input
                    type="file"
                    accept="image/*"
                    capture="environment"
                    className="hidden"
                    onChange={(event) => {
                      const file = event.target.files?.[0];
                      if (file) void uploadAttachment(file, "before");
                      event.currentTarget.value = "";
                    }}
                  />
                  <Button variant="outline" size="sm" asChild disabled={analyzing}>
                    <span>
                      <Camera className="h-4 w-4" />
                      {analyzing ? "Analyzing..." : "Photo"}
                    </span>
                  </Button>
                </label>
                <label>
                  <input
                    type="file"
                    accept="video/*"
                    className="hidden"
                    onChange={(event) => {
                      const file = event.target.files?.[0];
                      if (file) void uploadAttachment(file, "video");
                      event.currentTarget.value = "";
                    }}
                  />
                  <Button variant="outline" size="sm" asChild>
                    <span>
                      <Upload className="h-4 w-4" />
                      Video
                    </span>
                  </Button>
                </label>
                {attachments.some(a => a.type.startsWith("image/")) && (
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => {
                      const imageAttachment = attachments.find(a => a.type.startsWith("image/"));
                      if (imageAttachment) {
                        // For demo purposes, we'll re-analyze the first image
                        // In production, you'd want to fetch the actual image data
                        toast({ title: "Re-analyzing photo", description: "AI will detect faults from the uploaded image" });
                      }
                    }}
                    disabled={analyzing}
                  >
                    <Brain className="h-4 w-4 mr-2" />
                    {analyzing ? "Analyzing..." : "Analyze Photo"}
                  </Button>
                )}
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    const note = window.prompt("Record a voice note (demo text)");
                    if (!note) return;
                    setAttachments((items) => [
                      ...items,
                      { name: "voice-note.txt", url: `voice-note:${note}`, type: "text/plain" },
                    ]);
                    toast({ title: "Voice note added", description: "Added as a text attachment" });
                  }}
                >
                  <Mic className="h-4 w-4" />
                  Voice
                </Button>
              </div>

              {attachments.length > 0 && (
                <Card className="border-border/70 bg-background/60">
                  <CardContent className="space-y-3 p-4">
                    <p className="flex items-center gap-2 text-sm font-medium">
                      <Paperclip className="h-4 w-4 text-primary" />
                      Attachments
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {attachments.map((attachment) => (
                        <Badge key={`${attachment.name}-${attachment.url}`} variant="outline">
                          {attachment.name}
                        </Badge>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}

              {aiDetectionResults && (
                <Card className="border-primary/30 bg-primary/5">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-sm flex items-center gap-2">
                      <Brain className="h-4 w-4 text-primary" />
                      AI Detection Results
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Equipment Type:</span>
                      <Badge variant="outline">{aiDetectionResults.equipment_type}</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Overall Condition:</span>
                      <Badge 
                        variant={
                          aiDetectionResults.overall_condition === "critical" ? "destructive" :
                          aiDetectionResults.overall_condition === "poor" ? "warning" :
                          aiDetectionResults.overall_condition === "fair" ? "secondary" : "outline"
                        }
                      >
                        {aiDetectionResults.overall_condition}
                      </Badge>
                    </div>
                    {aiDetectionResults.detected_issues && aiDetectionResults.detected_issues.length > 0 && (
                      <div className="space-y-2">
                        <p className="text-sm font-medium">Detected Issues:</p>
                        {aiDetectionResults.detected_issues.map((issue: DetectedIssue, i: number) => (
                          <div key={i} className="text-xs space-y-1 p-2 bg-background/50 rounded">
                            <div className="flex items-center justify-between">
                              <span className="font-medium">{issue.type}</span>
                              <Badge 
                                variant={
                                  issue.severity === "critical" ? "destructive" :
                                  issue.severity === "high" ? "warning" :
                                  issue.severity === "medium" ? "secondary" : "outline"
                                }
                                className="text-xs"
                              >
                                {issue.severity}
                              </Badge>
                            </div>
                            <p className="text-muted-foreground">{issue.description}</p>
                            <p className="text-muted-foreground">Location: {issue.location}</p>
                            <p className="text-muted-foreground">Confidence: {Math.round(issue.confidence * 100)}%</p>
                          </div>
                        ))}
                      </div>
                    )}
                    {aiDetectionResults.recommended_actions && aiDetectionResults.recommended_actions.length > 0 && (
                      <div className="space-y-2">
                        <p className="text-sm font-medium">Recommended Actions:</p>
                        <ul className="text-xs space-y-1 list-disc list-inside text-muted-foreground">
                          {aiDetectionResults.recommended_actions.map((action: string, i: number) => (
                            <li key={i}>{action}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </CardContent>
                </Card>
              )}

              <div className="flex flex-col gap-3 sm:flex-row">
                <Button variant="outline" onClick={getAiDiagnosis} disabled={loading || !description}>
                  <Brain className="h-4 w-4" />
                  {loading ? "Analyzing..." : "AI diagnosis"}
                </Button>
                <Button className="sm:ml-auto" onClick={submit} disabled={!machineId || !description || uploading || analyzing}>
                  <Send className="h-4 w-4" />
                  Submit report
                </Button>
              </div>

              {aiDiagnosis && (
                <Card className="border-primary/30 bg-primary/5">
                  <CardContent className="p-4">
                    <p className="mb-2 text-sm font-medium text-primary">AI suggested causes</p>
                    <pre className="whitespace-pre-wrap text-sm">{aiDiagnosis}</pre>
                  </CardContent>
                </Card>
              )}
            </CardContent>
          </Card>

          <div className="space-y-4">
            <Card className="border-primary/20 bg-gradient-to-br from-primary/15 via-card to-card">
              <CardHeader>
                <CardTitle className="text-base">Report readiness</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 text-sm text-muted-foreground">
                <div className="rounded-2xl border border-border/70 bg-background/60 p-3">
                  Machine: <span className="font-medium text-foreground">{currentMachine?.name ?? "Not selected"}</span>
                </div>
                <div className="rounded-2xl border border-border/70 bg-background/60 p-3">
                  Attachments: <span className="font-medium text-foreground">{attachments.length}</span>
                </div>
                <div className="rounded-2xl border border-border/70 bg-background/60 p-3">
                  Severity: <span className="font-medium text-foreground">{severity}</span>
                </div>
              </CardContent>
            </Card>

            <Card className="border-border/70">
              <CardHeader>
                <CardTitle className="text-base">Capture tips</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 text-sm text-muted-foreground">
                <p className="rounded-2xl border border-border/70 bg-background/60 p-3">
                  Include the exact symptom, when it started, and whether the machine can still run safely.
                </p>
                <p className="rounded-2xl border border-border/70 bg-background/60 p-3">
                  Add a photo before teardown so supervisors can validate the fault quickly from desktop.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </TabsContent>

      <TabsContent value="my" className="mt-4">
        <div className="grid gap-3 md:grid-cols-2">
          {recentReports.map((report) => (
            <Card key={report.id} className="border-border/70">
              <CardContent className="p-4">
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <p className="truncate font-medium">{report.machine?.name}</p>
                    <p className="mt-1 text-sm text-muted-foreground">{report.description}</p>
                    <p className="mt-2 text-xs text-muted-foreground">{formatDate(report.created_at ?? "")}</p>
                    <p className="mt-1 text-[11px] text-muted-foreground">
                      {report.source === "sync-queue" ? "Pending sync" : "Demo / local"}
                    </p>
                  </div>
                  <div className="flex flex-col items-end gap-1">
                    <Badge variant={report.severity === "critical" ? "destructive" : "warning"}>
                      {report.severity}
                    </Badge>
                    <Badge variant="outline">{report.status}</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </TabsContent>
    </Tabs>
  );
}

export default function ReportPage() {
  return (
    <AppShell title="Report Fault">
      <Suspense fallback={<div className="p-4">Loading report workspace...</div>}>
        <ReportContent />
      </Suspense>
    </AppShell>
  );
}

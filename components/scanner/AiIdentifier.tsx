"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Loader2, Upload, CheckCircle2 } from "lucide-react";
import { CameraView } from "./CameraView";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface Match {
  id: string;
  name: string;
  model: string;
  confidence: number;
  image_url?: string;
}

export function AiIdentifier() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [matches, setMatches] = useState<Match[]>([]);

  const identify = async (dataUrl: string) => {
    setLoading(true);
    setMatches([]);

    try {
      const base64 = dataUrl.split(",")[1];
      const res = await fetch("/api/identify-machine", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: base64 }),
      });
      const data = await res.json();
      setMatches(data.matches ?? []);
    } catch {
      setMatches([]);
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

  return (
    <div className="flex min-h-[420px] flex-col lg:min-h-[640px]">
      <div className="relative flex-1">
        <CameraView
          onCapture={identify}
          className="h-full"
        />
        {loading && (
          <div className="absolute inset-0 bg-black/70 flex flex-col items-center justify-center">
            <Loader2 className="h-10 w-10 text-primary animate-spin mb-3" />
            <p className="text-white text-sm">Analyzing machine...</p>
          </div>
        )}
      </div>

      <div className="p-4 space-y-3 bg-card border-t border-border">
        <p className="text-sm text-muted-foreground text-center">
          Point at any industrial machine and tap capture
        </p>
        <label className="block">
          <input type="file" accept="image/*" className="hidden" onChange={handleGalleryUpload} />
          <Button variant="outline" className="w-full" asChild>
            <span><Upload className="h-4 w-4 mr-2" />Upload from Gallery</span>
          </Button>
        </label>

        {matches.length > 0 && (
          <div className="space-y-2">
            <p className="text-sm font-medium">Top Matches</p>
            {matches.map((match) => (
              <Card
                key={match.id}
                className="cursor-pointer hover:border-primary transition-colors"
                onClick={() => router.push(`/repair/${match.id}`)}
              >
                <CardContent className="flex items-center justify-between p-3.5">
                  <div className="flex items-center gap-3 min-w-0">
                    {match.image_url && (
                      <img
                        src={match.image_url}
                        alt={match.name}
                        className="h-12 w-12 shrink-0 rounded-lg object-cover border border-border bg-muted"
                      />
                    )}
                    <div className="min-w-0">
                      <p className="truncate font-medium">{match.name}</p>
                      <p className="text-xs text-muted-foreground">{match.model}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge variant={match.confidence > 0.8 ? "success" : "warning"}>
                      {Math.round(match.confidence * 100)}%
                    </Badge>
                    <CheckCircle2 className="h-5 w-5 text-primary" />
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

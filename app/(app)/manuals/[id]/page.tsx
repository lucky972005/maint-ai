"use client";

import { useParams } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { AppShell } from "@/components/layout/app-shell";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { getMachineById } from "@/lib/demo-data";
import { getCachedManual, cacheManual } from "@/lib/offline";
import { Bookmark, BookmarkCheck, ChevronLeft, Download, FileText, Search } from "lucide-react";

type ManualSection = {
  id: number;
  title: string;
  content: string[];
};

function buildSections(
  machineName: string,
  machineModel: string | null,
  machineSerial: string | null,
  machineLocation: string | null,
  machineCategory: string
) {
  return [
    {
      id: 1,
      title: "Safety Instructions",
      content: [
        "Always follow lockout/tagout before opening covers.",
        "Wear eye protection, gloves, and hearing protection where applicable.",
        "Verify zero energy state before touching electrical or moving components.",
      ],
    },
    {
      id: 2,
      title: "Specifications",
      content: [
        `Machine: ${machineName}`,
        `Model: ${machineModel ?? "unknown"}`,
        `Serial: ${machineSerial ?? "unknown"}`,
        `Location: ${machineLocation ?? "unknown"}`,
        `Category: ${machineCategory}`,
      ],
    },
    {
      id: 3,
      title: "Preventive Schedule",
      content: [
        "Daily: Visual inspection, leaks, alarms, abnormal noise.",
        "Weekly: Lubrication points, belts, connectors, guard integrity.",
        "Monthly: Filters, electrical terminals, vibration checks.",
        "Quarterly: Full inspection and procedure review.",
      ],
    },
    {
      id: 4,
      title: "Troubleshooting",
      content: [
        "Overheating: Check ventilation, load, and lubrication.",
        "Vibration: Inspect alignment, bearings, and mounts.",
        "Pressure loss: Inspect seals, hoses, and pumps.",
        "Electrical faults: Check terminals, breakers, and insulation.",
      ],
    },
  ] satisfies ManualSection[];
}

export default function ManualViewerPage() {
  const params = useParams();
  const machineId = params.id as string;
  const machine = getMachineById(machineId);
  const [search, setSearch] = useState("");
  const [bookmarks, setBookmarks] = useState<number[]>([]);
  const [cached, setCached] = useState(false);

  const sections = useMemo(() => {
    if (!machine) return [];
    return buildSections(machine.name, machine.model, machine.serial_number, machine.location, machine.category);
  }, [machine]);

  const manualContent = useMemo(() => {
    if (!machine) return "";
    return [
      `${machine.name} Maintenance Manual`,
      `Model: ${machine.model ?? "unknown"}`,
      `Serial: ${machine.serial_number ?? "unknown"}`,
      `Location: ${machine.location ?? "unknown"}`,
      "",
      ...sections.flatMap((section) => [section.title, ...section.content, ""]),
    ].join("\n");
  }, [machine, sections]);

  useEffect(() => {
    getCachedManual(machineId)
      .then((manual) => setCached(!!manual))
      .catch(() => {});
    const stored = window.localStorage.getItem(`manual-bookmarks:${machineId}`);
    if (stored) setBookmarks(JSON.parse(stored));
  }, [machineId]);

  useEffect(() => {
    window.localStorage.setItem(`manual-bookmarks:${machineId}`, JSON.stringify(bookmarks));
  }, [bookmarks, machineId]);

  const cacheForOffline = async () => {
    try {
      const blob = new Blob([manualContent], { type: "application/pdf" });
      await cacheManual(machineId, machineId, machine?.name ?? "Manual", blob);
      setCached(true);
    } catch {}
  };

  const downloadManual = () => {
    const blob = new Blob([manualContent], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `${machine?.name ?? "manual"}-maintenance-guide.txt`;
    anchor.click();
    URL.revokeObjectURL(url);
  };

  const toggleBookmark = (page: number) => {
    setBookmarks((current) =>
      current.includes(page) ? current.filter((item) => item !== page) : [...current, page].sort((a, b) => a - b)
    );
  };

  if (!machine) {
    return (
      <AppShell title="Manual">
        <div className="p-8 text-center">
          <p className="text-muted-foreground">Manual not found</p>
          <Link href="/manuals">
            <Button className="mt-4">Back to Library</Button>
          </Link>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell title="Manual">
      <div className="flex min-h-[calc(100vh-120px)] flex-col">
        <div className="flex flex-wrap items-center gap-2 border-b border-border p-3">
          <Link href="/manuals">
            <Button variant="ghost" size="sm">
              <ChevronLeft className="h-4 w-4" />
            </Button>
          </Link>
          <div className="relative h-10 w-10 shrink-0 overflow-hidden rounded-lg border border-border bg-muted">
            {machine.images?.[0] || machine.image_url ? (
              <img
                src={machine.images?.[0] || machine.image_url || ""}
                alt={machine.name}
                className="h-full w-full object-cover"
              />
            ) : (
              <FileText className="h-5 w-5 m-auto text-primary" />
            )}
          </div>
          <div className="min-w-0 flex-1">
            <p className="truncate font-medium">{machine.name}</p>
            <p className="text-xs text-muted-foreground">{machine.model} Manual • {machine.category}</p>
          </div>
          <div className="flex gap-1">
            <Button variant="outline" size="sm" onClick={cacheForOffline}>
              {cached ? "Cached" : "Cache Offline"}
            </Button>
            <Button variant="outline" size="sm" onClick={downloadManual}>
              <Download className="h-4 w-4" />
            </Button>
          </div>
        </div>

        <div className="flex gap-2 border-b border-border p-3">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder="Search manual..."
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              className="pl-9"
            />
          </div>
          <Button variant="outline" size="sm" onClick={() => toggleBookmark(1)}>
            {bookmarks.includes(1) ? <BookmarkCheck className="h-4 w-4" /> : <Bookmark className="h-4 w-4" />}
          </Button>
        </div>

        <div className="flex-1 overflow-auto bg-muted/30 p-4">
          <div className="mx-auto min-h-[800px] max-w-3xl rounded-lg border border-border bg-card p-8 shadow-lg">
            <h1 className="mb-2 text-2xl font-bold">{machine.name}</h1>
            <p className="mb-6 text-muted-foreground">Operation and Maintenance Manual - {machine.manufacturer}</p>

            {search && <p className="mb-4 text-sm text-primary">Search results for &quot;{search}&quot;</p>}

            <div className="space-y-6 text-sm leading-relaxed">
              {sections
                .filter((section) => {
                  const query = search.trim().toLowerCase();
                  if (!query) return true;
                  return (
                    section.title.toLowerCase().includes(query) ||
                    section.content.some((line) => line.toLowerCase().includes(query))
                  );
                })
                .map((section) => (
                  <section key={section.id} className="rounded-xl border border-border/70 bg-background p-4">
                    <div className="mb-3 flex items-center justify-between gap-3">
                      <div className="flex items-center gap-2">
                        <FileText className="h-4 w-4 text-primary" />
                        <h2 className="text-lg font-semibold text-primary">
                          {section.id}. {section.title}
                        </h2>
                      </div>
                      <Button variant="ghost" size="sm" onClick={() => toggleBookmark(section.id)}>
                        {bookmarks.includes(section.id) ? (
                          <BookmarkCheck className="h-4 w-4 text-primary" />
                        ) : (
                          <Bookmark className="h-4 w-4" />
                        )}
                      </Button>
                    </div>
                    <ul className="space-y-2">
                      {section.content.map((line) => (
                        <li key={line} className="flex gap-2">
                          <span className="mt-1 text-primary">-</span>
                          <span>{line}</span>
                        </li>
                      ))}
                    </ul>
                  </section>
                ))}

              {bookmarks.length > 0 && (
                <p className="text-xs text-muted-foreground">Bookmarked pages: {bookmarks.join(", ")}</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
}

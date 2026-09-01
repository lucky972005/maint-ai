"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { AppShell } from "@/components/layout/app-shell";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { DEMO_DATA } from "@/lib/demo-data";
import { BookOpen, ChevronRight, Search } from "lucide-react";

export default function ManualsPage() {
  const [search, setSearch] = useState("");
  const [bookmarks, setBookmarks] = useState<string[]>([]);

  useEffect(() => {
    const stored = window.localStorage.getItem("manual-bookmarks");
    if (stored) setBookmarks(JSON.parse(stored));
  }, []);

  const filteredMachines = useMemo(() => {
    const query = search.trim().toLowerCase();
    if (!query) return DEMO_DATA.machines;
    return DEMO_DATA.machines.filter((machine) => {
      return [machine.name, machine.model, machine.manufacturer, machine.category]
        .filter(Boolean)
        .some((field) => field?.toLowerCase().includes(query));
    });
  }, [search]);

  return (
    <AppShell title="Manuals">
      <div className="space-y-3 p-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Search manuals by machine, model, or category"
            className="pl-9"
          />
        </div>

        {bookmarks.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {bookmarks.slice(0, 5).map((bookmark) => (
              <Badge key={bookmark} variant="outline">
                Bookmarked: {bookmark}
              </Badge>
            ))}
          </div>
        )}

        {filteredMachines.map((machine) => (
          <Link key={machine.id} href={`/manuals/${machine.id}`}>
            <Card className="mb-3 border-border/50 transition-colors hover:border-primary/30">
              <CardContent className="flex items-center gap-3 p-4">
                <div className="relative flex h-14 w-14 shrink-0 items-center justify-center rounded-xl bg-muted overflow-hidden border border-border">
                  {machine.images?.[0] || machine.image_url ? (
                    <img
                      src={machine.images?.[0] || machine.image_url || ""}
                      alt={machine.name}
                      className="h-full w-full object-cover"
                    />
                  ) : (
                    <BookOpen className="h-6 w-6 text-primary" />
                  )}
                </div>
                <div className="min-w-0 flex-1">
                  <p className="font-medium">{machine.name}</p>
                  <p className="text-sm text-muted-foreground">{machine.model} - {machine.manufacturer}</p>
                  <p className="mt-1 text-xs text-muted-foreground">Category: {machine.category}</p>
                </div>
                <ChevronRight className="h-5 w-5 text-muted-foreground" />
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </AppShell>
  );
}

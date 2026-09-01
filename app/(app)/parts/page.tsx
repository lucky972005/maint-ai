"use client";

import { useMemo, useState, Suspense, useEffect } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { AppShell } from "@/components/layout/app-shell";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { DEMO_DATA, isFirebaseConfigured } from "@/lib/demo-data";
import { getParts } from "@/lib/database";
import { useApp } from "@/components/providers";
import { AlertTriangle, Boxes, Package, ShoppingCart, Sparkles } from "lucide-react";
import { BarcodeGenerator } from "@/components/parts/BarcodeGenerator";
import { ImageManager } from "@/components/image-manager";
import { PurchaseRequestModal } from "@/components/parts/PurchaseRequestModal";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";

function PartsContent() {
  const searchParams = useSearchParams();
  const machineFilter = searchParams.get("machine");
  const machine = DEMO_DATA.machines.find((item) => item.id === machineFilter);
  const { profile } = useApp();
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("all");
  const [parts, setParts] = useState(DEMO_DATA.parts);
  const [loading, setLoading] = useState(true);
  const [useRealData, setUseRealData] = useState(false);
  const [purchaseModalOpen, setPurchaseModalOpen] = useState(false);
  const [selectedForPurchase, setSelectedForPurchase] = useState<typeof DEMO_DATA.parts>([]);
  const [previewPart, setPreviewPart] = useState<(typeof DEMO_DATA.parts)[0] | null>(null);

  useEffect(() => {
    const loadData = async () => {
      const firebaseConfigured = isFirebaseConfigured();
      setUseRealData(firebaseConfigured);

      if (firebaseConfigured) {
        try {
          const partsData = await getParts();
          setParts(partsData);
        } catch (error) {
          console.error("Failed to load parts from Firebase:", error);
        }
      }
      setLoading(false);
    };

    loadData();
  }, []);

  const lowStock = useMemo(
    () => parts.filter((part) => part.stock_quantity < part.min_stock_level),
    [parts]
  );

  const filtered = useMemo(() => {
    return parts.filter((part) => {
      if (category !== "all" && part.category !== category) return false;
      if (machineFilter && !part.compatible_machines?.includes(machineFilter)) return false;
      if (search) {
        const query = search.toLowerCase();
        return part.name.toLowerCase().includes(query) || part.part_number.toLowerCase().includes(query);
      }
      return true;
    });
  }, [category, machineFilter, search, parts]);

  const isAdmin = profile?.role === "admin";
  const totalInventoryUnits = filtered.reduce((total, part) => total + part.stock_quantity, 0);
  const categories = new Set(parts.map((part) => part.category).filter(Boolean));

  if (loading) {
    return (
      <div className="p-8 text-center">
        <p className="text-muted-foreground">Loading parts inventory...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 px-4 py-4 lg:px-8 lg:py-6">
      {useRealData && (
        <div className="flex items-center justify-between p-3 bg-green-950/30 border border-green-800 rounded-lg">
          <p className="text-sm text-green-400">✓ Connected to Supabase database</p>
          <Badge variant="success">Live Data</Badge>
        </div>
      )}
      {machine && (
        <Card className="border-primary/25 bg-primary/10">
          <CardContent className="flex flex-col gap-3 p-5 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <p className="text-sm font-semibold text-primary">Repair context</p>
              <p className="mt-1 text-lg font-semibold">{machine.name}</p>
              <p className="text-sm text-muted-foreground">
                Showing parts compatible with {machine.model ?? machine.category}.
              </p>
            </div>
            <Link href={`/repair/${machine.id}`}>
              <Button variant="outline">Back to repair flow</Button>
            </Link>
          </CardContent>
        </Card>
      )}

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <Card className="border-border/70">
          <CardContent className="flex items-center gap-4 p-5">
            <div className="rounded-2xl bg-primary/15 p-3 text-primary">
              <Boxes className="h-5 w-5" />
            </div>
            <div>
              <p className="text-2xl font-semibold">{filtered.length}</p>
              <p className="text-sm text-muted-foreground">Visible parts</p>
            </div>
          </CardContent>
        </Card>
        <Card className="border-border/70">
          <CardContent className="flex items-center gap-4 p-5">
            <div className="rounded-2xl bg-yellow-500/15 p-3 text-yellow-400">
              <AlertTriangle className="h-5 w-5" />
            </div>
            <div>
              <p className="text-2xl font-semibold">{lowStock.length}</p>
              <p className="text-sm text-muted-foreground">Low-stock items</p>
            </div>
          </CardContent>
        </Card>
        <Card className="border-border/70">
          <CardContent className="flex items-center gap-4 p-5">
            <div className="rounded-2xl bg-blue-500/15 p-3 text-blue-400">
              <Package className="h-5 w-5" />
            </div>
            <div>
              <p className="text-2xl font-semibold">{totalInventoryUnits}</p>
              <p className="text-sm text-muted-foreground">Units on hand</p>
            </div>
          </CardContent>
        </Card>
        <Card className="border-border/70">
          <CardContent className="flex items-center gap-4 p-5">
            <div className="rounded-2xl bg-green-500/15 p-3 text-green-400">
              <Sparkles className="h-5 w-5" />
            </div>
            <div>
              <p className="text-2xl font-semibold">{categories.size}</p>
              <p className="text-sm text-muted-foreground">Inventory categories</p>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 xl:grid-cols-[minmax(0,1fr)_320px]">
        <div className="space-y-4">
          <Card className="border-border/70">
            <CardHeader className="gap-4">
              <div>
                <CardTitle className="text-lg">Inventory browser</CardTitle>
                <p className="text-sm text-muted-foreground">
                  Search parts by name, part number, or category.
                </p>
              </div>
              <div className="flex flex-col gap-3 lg:flex-row">
                <Input
                  placeholder="Search parts"
                  value={search}
                  onChange={(event) => setSearch(event.target.value)}
                  className="flex-1"
                />
                <Select value={category} onValueChange={setCategory}>
                  <SelectTrigger className="w-full lg:w-[180px]">
                    <SelectValue placeholder="Category" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All categories</SelectItem>
                    <SelectItem value="Mechanical">Mechanical</SelectItem>
                    <SelectItem value="Electrical">Electrical</SelectItem>
                    <SelectItem value="Hydraulic">Hydraulic</SelectItem>
                    <SelectItem value="Pneumatic">Pneumatic</SelectItem>
                    <SelectItem value="Consumable">Consumable</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
                {filtered.map((part) => (
                  <Card key={part.id} className="border-border/70 bg-background/60 hover:border-primary/40 transition">
                    <CardContent className="flex gap-4 p-4">
                      {/* Clickable image with hover zoom indicator */}
                      <button
                        type="button"
                        onClick={() => setPreviewPart(part)}
                        className="group relative flex h-20 w-20 shrink-0 items-center justify-center rounded-2xl bg-muted overflow-hidden border border-border/80 focus:outline-none focus:ring-2 focus:ring-primary"
                        title="Click to zoom image & view details"
                      >
                        {(part.images && part.images.length > 0) || part.image_url ? (
                          <img 
                            src={part.images?.[0] || part.image_url || ""} 
                            alt={part.name}
                            className="h-full w-full object-cover transition duration-300 group-hover:scale-110"
                          />
                        ) : (
                          <Package className="h-8 w-8 text-muted-foreground" />
                        )}
                        <div className="absolute inset-0 bg-black/30 opacity-0 transition group-hover:opacity-100 flex items-center justify-center">
                          <span className="text-[10px] text-white font-medium bg-black/60 px-1.5 py-0.5 rounded">View</span>
                        </div>
                      </button>

                      <div className="min-w-0 flex-1">
                        <div className="flex items-start justify-between gap-3">
                          <div className="min-w-0">
                            <p className="truncate font-medium">{part.name}</p>
                            <p className="text-xs text-muted-foreground">
                              {part.part_number} - {part.category}
                            </p>
                          </div>
                          <span className="text-sm font-semibold text-primary">
                            ${part.unit_price?.toFixed(2)}
                          </span>
                        </div>

                        {part.supplier && (
                          <p className="mt-1 text-[11px] text-muted-foreground truncate">
                            Supplier: <span className="text-foreground/80">{part.supplier}</span>
                          </p>
                        )}

                        <div className="mt-2 mb-3">
                          <BarcodeGenerator value={part.part_number} width={1} height={28} displayValue={false} className="opacity-70" />
                        </div>

                        <div className="mt-2 flex flex-wrap items-center gap-2">
                          <Badge
                            variant={
                              part.stock_quantity < part.min_stock_level
                                ? "destructive"
                                : part.stock_quantity < part.min_stock_level * 2
                                  ? "warning"
                                  : "success"
                            }
                          >
                            Stock {part.stock_quantity}
                          </Badge>
                          <Badge variant="outline">Min {part.min_stock_level}</Badge>
                        </div>

                        {machineFilter && (
                          <Button size="sm" variant="outline" className="mt-3 w-full">
                            Use in current repair
                          </Button>
                        )}

                        <div className="mt-3 flex gap-2">
                          <Button
                            size="sm"
                            variant="secondary"
                            className="flex-1 text-xs"
                            onClick={() => {
                              setSelectedForPurchase([part]);
                              setPurchaseModalOpen(true);
                            }}
                          >
                            <ShoppingCart className="mr-1 h-3 w-3" />
                            Restock
                          </Button>
                          {isAdmin && (
                            <>
                              <Button size="sm" variant="ghost" className="flex-1 text-xs">
                                Edit
                              </Button>
                              <ImageManager
                                entityType="part"
                                entityId={part.id}
                                existingImages={part.images || []}
                                onImagesUpdate={async (newImages) => {
                                  const updatedParts = parts.map(p => 
                                    p.id === part.id ? { ...p, images: newImages } : p
                                  );
                                  setParts(updatedParts);
                                  
                                  try {
                                    await fetch(`/api/parts/${part.id}/images`, {
                                      method: "POST",
                                      headers: { "Content-Type": "application/json" },
                                      body: JSON.stringify({ images: [], setPrimaryIndex: 0 }),
                                    });
                                  } catch (error) {
                                    console.error("Failed to update part images:", error);
                                  }
                                }}
                              />
                            </>
                          )}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-4">
          <Card className="border-primary/20 bg-gradient-to-br from-primary/15 via-card to-card">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-base">Restock Queue</CardTitle>
                <Badge variant={lowStock.length > 0 ? "destructive" : "secondary"}>
                  {lowStock.length} items
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              {lowStock.length === 0 ? (
                <div className="rounded-xl border border-border/70 bg-background/60 p-4 text-center text-xs text-muted-foreground">
                  All inventory items are currently above safety threshold.
                </div>
              ) : (
                lowStock.slice(0, 5).map((part) => (
                  <div key={part.id} className="flex items-center justify-between gap-3 rounded-2xl border border-border/70 bg-background/60 p-2.5">
                    <div className="flex items-center gap-2.5 min-w-0">
                      <img
                        src={part.images?.[0] || part.image_url || ""}
                        alt={part.name}
                        className="h-10 w-10 shrink-0 rounded-lg object-cover border border-border bg-muted"
                      />
                      <div className="min-w-0">
                        <p className="truncate text-sm font-medium">{part.name}</p>
                        <p className="text-xs text-muted-foreground">{part.part_number}</p>
                      </div>
                    </div>
                    <Badge variant="destructive" className="shrink-0">{part.stock_quantity} left</Badge>
                  </div>
                ))
              )}
              <Button
                className="w-full orange-glow"
                onClick={() => {
                  setSelectedForPurchase(lowStock);
                  setPurchaseModalOpen(true);
                }}
              >
                <ShoppingCart className="h-4 w-4 mr-1.5" />
                Create purchase request
              </Button>
            </CardContent>
          </Card>

          <Card className="border-border/70">
            <CardHeader>
              <CardTitle className="text-base">Usage notes</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm text-muted-foreground">
              <p className="rounded-2xl border border-border/70 bg-background/60 p-3">
                Keep the machine filter on when selecting parts from a live repair flow. It reduces wrong picks.
              </p>
              <p className="rounded-2xl border border-border/70 bg-background/60 p-3">
                Low stock items are surfaced here and in the desktop workspace rail so supervisors can act quickly.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Purchase Request Modal */}
      <PurchaseRequestModal
        open={purchaseModalOpen}
        onOpenChange={setPurchaseModalOpen}
        parts={parts}
        initialSelectedParts={selectedForPurchase}
        onOrderSubmitted={(orderedItems) => {
          setParts((prev) =>
            prev.map((p) => {
              const matched = orderedItems.find((item) => item.partId === p.id);
              return matched ? { ...p, stock_quantity: matched.newStock } : p;
            })
          );
        }}
      />

      {/* Part Image & Details Lightbox Modal */}
      <Dialog open={!!previewPart} onOpenChange={(open) => !open && setPreviewPart(null)}>
        <DialogContent className="max-w-md">
          {previewPart && (
            <div className="space-y-4">
              <DialogHeader>
                <DialogTitle>{previewPart.name}</DialogTitle>
                <p className="text-xs text-muted-foreground font-mono">
                  {previewPart.part_number} • {previewPart.category}
                </p>
              </DialogHeader>

              <div className="relative aspect-square w-full overflow-hidden rounded-2xl border border-border bg-muted">
                {previewPart.images?.[0] || previewPart.image_url ? (
                  <img
                    src={previewPart.images?.[0] || previewPart.image_url || ""}
                    alt={previewPart.name}
                    className="h-full w-full object-cover"
                  />
                ) : (
                  <div className="flex h-full w-full items-center justify-center">
                    <Package className="h-16 w-16 text-muted-foreground" />
                  </div>
                )}
              </div>

              <div className="space-y-2 text-sm">
                {previewPart.description && (
                  <p className="text-muted-foreground text-xs">{previewPart.description}</p>
                )}

                <div className="grid grid-cols-2 gap-2 rounded-xl border border-border bg-muted/30 p-3 text-xs">
                  <div>
                    <span className="text-muted-foreground">Unit Price:</span>
                    <p className="font-semibold text-primary">${previewPart.unit_price?.toFixed(2)}</p>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Current Stock:</span>
                    <p className="font-semibold">{previewPart.stock_quantity} units (Min: {previewPart.min_stock_level})</p>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Supplier:</span>
                    <p className="font-semibold">{previewPart.supplier || "OEM Direct"}</p>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Lead Time:</span>
                    <p className="font-semibold">{previewPart.lead_time_days ?? 2} days</p>
                  </div>
                </div>

                <div className="pt-2 flex gap-2">
                  <Button
                    className="w-full orange-glow"
                    onClick={() => {
                      setPreviewPart(null);
                      setSelectedForPurchase([previewPart]);
                      setPurchaseModalOpen(true);
                    }}
                  >
                    <ShoppingCart className="mr-2 h-4 w-4" />
                    Order / Restock This Part
                  </Button>
                </div>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}

export default function PartsPage() {
  return (
    <AppShell title="Spare Parts">
      <Suspense fallback={<div className="p-4">Loading parts...</div>}>
        <PartsContent />
      </Suspense>
    </AppShell>
  );
}

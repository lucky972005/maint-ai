"use client";

import { useMemo, useState, Suspense, useEffect } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { AppShell } from "@/components/layout/app-shell";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { DEMO_DATA, isFirebaseConfigured } from "@/lib/demo-data";
import { getParts } from "@/lib/database";
import { useApp } from "@/components/providers";
import { toast } from "@/hooks/use-toast";
import { BarcodeGenerator } from "@/components/parts/BarcodeGenerator";
import { ImageManager } from "@/components/image-manager";
import { PurchaseRequestModal } from "@/components/parts/PurchaseRequestModal";
import type { Part } from "@/lib/types";
import {
  AlertTriangle,
  Barcode,
  Boxes,
  Building2,
  Check,
  Clock,
  Copy,
  ExternalLink,
  Eye,
  Filter,
  Layers,
  LayoutGrid,
  List,
  Package,
  PackageSearch,
  Printer,
  RotateCcw,
  Search,
  ShoppingCart,
  Sparkles,
  Truck,
  Wrench,
  X,
} from "lucide-react";

type StockFilterType = "all" | "low_stock" | "optimal";
type ViewMode = "grid" | "table";
type SortOption = "urgency" | "name_asc" | "stock_asc" | "stock_desc" | "price_asc" | "price_desc";

function PartsContent() {
  const searchParams = useSearchParams();
  const machineFilter = searchParams.get("machine");
  const machine = DEMO_DATA.machines.find((item) => item.id === machineFilter);
  const { profile } = useApp();

  // Data & Loading state
  const [parts, setParts] = useState<Part[]>(DEMO_DATA.parts);
  const [loading, setLoading] = useState(true);
  const [useRealData, setUseRealData] = useState(false);

  // Filter & Search states
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("all");
  const [stockFilter, setStockFilter] = useState<StockFilterType>("all");
  const [sortBy, setSortBy] = useState<SortOption>("urgency");
  const [viewMode, setViewMode] = useState<ViewMode>("grid");

  // Restock Queue drawer & modals state
  const [isRestockDrawerOpen, setIsRestockDrawerOpen] = useState(false);
  const [purchaseModalOpen, setPurchaseModalOpen] = useState(false);
  const [selectedForPurchase, setSelectedForPurchase] = useState<Part[]>([]);
  const [previewPart, setPreviewPart] = useState<Part | null>(null);
  const [barcodePart, setBarcodePart] = useState<Part | null>(null);
  const [copiedPartNumber, setCopiedPartNumber] = useState<string | null>(null);

  // Machine lookup map
  const machineMap = useMemo(() => {
    return new Map(DEMO_DATA.machines.map((m) => [m.id, m]));
  }, []);

  useEffect(() => {
    const loadData = async () => {
      const firebaseConfigured = isFirebaseConfigured();
      setUseRealData(firebaseConfigured);

      if (firebaseConfigured) {
        try {
          const partsData = await getParts();
          setParts(partsData);
        } catch (error) {
          console.error("Failed to load parts:", error);
        }
      }
      setLoading(false);
    };

    loadData();
  }, []);

  // Low stock list across all parts
  const lowStock = useMemo(
    () => parts.filter((part) => part.stock_quantity < part.min_stock_level),
    [parts]
  );

  // Filter and sort items
  const filteredParts = useMemo(() => {
    return parts
      .filter((part) => {
        // Category filter
        if (category !== "all" && part.category !== category) return false;

        // Machine compatibility filter
        if (machineFilter && !part.compatible_machines?.includes(machineFilter)) return false;

        // Stock status filter
        if (stockFilter === "low_stock" && part.stock_quantity >= part.min_stock_level) return false;
        if (stockFilter === "optimal" && part.stock_quantity < part.min_stock_level) return false;

        // Search filter (name, part_number, supplier, category)
        if (search.trim()) {
          const query = search.toLowerCase().trim();
          const matchName = part.name.toLowerCase().includes(query);
          const matchNumber = part.part_number.toLowerCase().includes(query);
          const matchSupplier = part.supplier?.toLowerCase().includes(query) ?? false;
          const matchCat = part.category?.toLowerCase().includes(query) ?? false;
          return matchName || matchNumber || matchSupplier || matchCat;
        }

        return true;
      })
      .sort((a, b) => {
        switch (sortBy) {
          case "urgency": {
            // Urgent: Lowest ratio of stock to min level comes first
            const ratioA = a.min_stock_level > 0 ? a.stock_quantity / a.min_stock_level : 999;
            const ratioB = b.min_stock_level > 0 ? b.stock_quantity / b.min_stock_level : 999;
            return ratioA - ratioB;
          }
          case "name_asc":
            return a.name.localeCompare(b.name);
          case "stock_asc":
            return a.stock_quantity - b.stock_quantity;
          case "stock_desc":
            return b.stock_quantity - a.stock_quantity;
          case "price_asc":
            return (a.unit_price ?? 0) - (b.unit_price ?? 0);
          case "price_desc":
            return (b.unit_price ?? 0) - (a.unit_price ?? 0);
          default:
            return 0;
        }
      });
  }, [parts, category, machineFilter, stockFilter, search, sortBy]);

  const isAdmin = profile?.role === "admin";
  const totalUnits = useMemo(() => parts.reduce((acc, p) => acc + p.stock_quantity, 0), [parts]);
  const totalValuation = useMemo(
    () => parts.reduce((acc, p) => acc + (p.stock_quantity * (p.unit_price ?? 0)), 0),
    [parts]
  );
  const categories = useMemo(() => {
    return Array.from(new Set(parts.map((p) => p.category).filter(Boolean))) as string[];
  }, [parts]);

  const copyPartNumber = (partNumber: string) => {
    navigator.clipboard.writeText(partNumber);
    setCopiedPartNumber(partNumber);
    toast({
      title: "Part Number Copied",
      description: `${partNumber} copied to clipboard`,
    });
    setTimeout(() => {
      setCopiedPartNumber(null);
    }, 2000);
  };

  const handlePrintBarcode = () => {
    window.print();
  };

  const clearAllFilters = () => {
    setSearch("");
    setCategory("all");
    setStockFilter("all");
  };

  const hasActiveFilters = search.trim() !== "" || category !== "all" || stockFilter !== "all";

  if (loading) {
    return (
      <div className="flex h-96 flex-col items-center justify-center space-y-3">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent" />
        <p className="text-sm text-muted-foreground animate-pulse">Loading parts catalog and stock levels...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 px-4 py-4 sm:px-6 lg:px-8">
      {/* Top Header & Restock Actions */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold tracking-tight text-foreground sm:text-3xl">Spare Parts Inventory</h1>
            {useRealData ? (
              <Badge variant="success" className="gap-1 text-[11px] font-medium">
                <span className="h-1.5 w-1.5 rounded-full bg-white animate-pulse" />
                Live Database
              </Badge>
            ) : (
              <Badge variant="secondary" className="text-[11px] font-medium text-muted-foreground">
                Demo Catalog
              </Badge>
            )}
          </div>
          <p className="mt-1 text-sm text-muted-foreground">
            Centralized spare parts registry, automated safety thresholds, and restock procurement.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          <Button
            variant={isRestockDrawerOpen ? "default" : "outline"}
            size="sm"
            onClick={() => setIsRestockDrawerOpen(!isRestockDrawerOpen)}
            className="gap-2 relative"
          >
            <ShoppingCart className="h-4 w-4" />
            <span>Restock Queue</span>
            {lowStock.length > 0 && (
              <span className="flex h-5 w-5 items-center justify-center rounded-full bg-rose-600 text-[11px] font-bold text-white shadow-sm">
                {lowStock.length}
              </span>
            )}
          </Button>

          {lowStock.length > 0 && (
            <Button
              size="sm"
              className="orange-glow gap-1.5 bg-primary text-primary-foreground font-medium"
              onClick={() => {
                setSelectedForPurchase(lowStock);
                setPurchaseModalOpen(true);
              }}
            >
              <Package className="h-4 w-4" />
              <span>Order All Low Stock ({lowStock.length})</span>
            </Button>
          )}
        </div>
      </div>

      {/* Repair Context Banner (if machineFilter is present) */}
      {machine && (
        <div className="relative overflow-hidden rounded-xl border border-primary/40 bg-gradient-to-r from-primary/15 via-primary/5 to-transparent p-4 sm:p-5">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-start gap-3.5">
              <div className="rounded-lg bg-primary/20 p-2.5 text-primary">
                <Wrench className="h-5 w-5" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-semibold uppercase tracking-wider text-primary">Repair Context Active</span>
                  <Badge variant="outline" className="text-[10px]">{machine.category}</Badge>
                </div>
                <h3 className="text-base font-semibold text-foreground sm:text-lg">{machine.name}</h3>
                <p className="text-xs text-muted-foreground">
                  Showing spare parts confirmed compatible with {machine.model || machine.name}.
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Link href="/parts">
                <Button size="sm" variant="ghost" className="text-xs">
                  Clear machine filter
                </Button>
              </Link>
              <Link href={`/repair/${machine.id}`}>
                <Button size="sm" variant="outline" className="text-xs gap-1.5">
                  <span>Return to repair procedure</span>
                  <ExternalLink className="h-3 w-3" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      )}

      {/* Interactive KPI Stat Cards */}
      <div className="grid grid-cols-2 gap-3 sm:gap-4 lg:grid-cols-4">
        {/* Total Catalog */}
        <Card
          className={`cursor-pointer transition-all duration-200 border-border/80 hover:border-primary/50 hover:bg-muted/30 ${
            stockFilter === "all" && !hasActiveFilters ? "ring-1 ring-primary/40 bg-muted/20" : ""
          }`}
          onClick={clearAllFilters}
          title="Click to reset filters"
        >
          <CardContent className="p-4 sm:p-5">
            <div className="flex items-center justify-between">
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Catalog Items</p>
              <div className="rounded-lg bg-primary/10 p-2 text-primary">
                <Boxes className="h-4 w-4" />
              </div>
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-2xl font-bold tracking-tight text-foreground sm:text-3xl">{parts.length}</span>
              <span className="text-xs text-muted-foreground">SKUs</span>
            </div>
            <p className="mt-1 text-[11px] text-muted-foreground">Total unique components</p>
          </CardContent>
        </Card>

        {/* Low Stock Items (Clickable filter) */}
        <Card
          className={`cursor-pointer transition-all duration-200 border-border/80 hover:border-amber-500/60 hover:bg-amber-500/5 ${
            stockFilter === "low_stock" ? "ring-2 ring-amber-500 bg-amber-500/10 border-amber-500" : ""
          }`}
          onClick={() => setStockFilter(stockFilter === "low_stock" ? "all" : "low_stock")}
          title="Click to toggle low-stock filter"
        >
          <CardContent className="p-4 sm:p-5">
            <div className="flex items-center justify-between">
              <p className="text-xs font-medium text-amber-400 uppercase tracking-wider">Low Stock Alerts</p>
              <div className="rounded-lg bg-amber-500/15 p-2 text-amber-400">
                <AlertTriangle className="h-4 w-4" />
              </div>
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-2xl font-bold tracking-tight text-amber-400 sm:text-3xl">{lowStock.length}</span>
              <span className="text-xs text-amber-400/80">under buffer</span>
            </div>
            <p className="mt-1 text-[11px] text-muted-foreground">
              {lowStock.length > 0 ? "Requires restock order" : "All levels healthy"}
            </p>
          </CardContent>
        </Card>

        {/* Total Units & Valuation */}
        <Card className="border-border/80">
          <CardContent className="p-4 sm:p-5">
            <div className="flex items-center justify-between">
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Inventory Units</p>
              <div className="rounded-lg bg-blue-500/10 p-2 text-blue-400">
                <Package className="h-4 w-4" />
              </div>
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-2xl font-bold tracking-tight text-foreground sm:text-3xl">
                {totalUnits.toLocaleString()}
              </span>
              <span className="text-xs text-muted-foreground">units</span>
            </div>
            <p className="mt-1 text-[11px] text-muted-foreground truncate">
              Est. ${totalValuation.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 0 })} value
            </p>
          </CardContent>
        </Card>

        {/* Categories */}
        <Card className="border-border/80">
          <CardContent className="p-4 sm:p-5">
            <div className="flex items-center justify-between">
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Categories</p>
              <div className="rounded-lg bg-emerald-500/10 p-2 text-emerald-400">
                <Layers className="h-4 w-4" />
              </div>
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-2xl font-bold tracking-tight text-foreground sm:text-3xl">{categories.length}</span>
              <span className="text-xs text-muted-foreground">types</span>
            </div>
            <p className="mt-1 text-[11px] text-muted-foreground truncate">
              Mechanical, Electrical, Consumables...
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Restock Queue Collapsible Sidepanel / Drawer */}
      {isRestockDrawerOpen && (
        <div className="rounded-xl border border-amber-500/30 bg-gradient-to-b from-amber-500/10 via-card to-card p-4 sm:p-5 shadow-lg">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-center gap-3">
              <div className="rounded-lg bg-amber-500/20 p-2 text-amber-400">
                <ShoppingCart className="h-5 w-5" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="font-semibold text-foreground">Restock Requisition Queue</h3>
                  <Badge variant={lowStock.length > 0 ? "destructive" : "secondary"}>
                    {lowStock.length} items
                  </Badge>
                </div>
                <p className="text-xs text-muted-foreground">
                  Quick replenishment review for items that have dropped below safety thresholds.
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              {lowStock.length > 0 && (
                <Button
                  size="sm"
                  className="orange-glow text-xs gap-1.5"
                  onClick={() => {
                    setSelectedForPurchase(lowStock);
                    setPurchaseModalOpen(true);
                  }}
                >
                  <ShoppingCart className="h-3.5 w-3.5" />
                  Create purchase request ({lowStock.length})
                </Button>
              )}
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsRestockDrawerOpen(false)}
                className="h-8 w-8 p-0"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          </div>

          <div className="mt-4">
            {lowStock.length === 0 ? (
              <div className="rounded-lg border border-border/80 bg-background/50 p-6 text-center text-xs text-muted-foreground">
                All inventory items are currently above safety thresholds. Good job!
              </div>
            ) : (
              <div className="grid grid-cols-1 gap-2.5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                {lowStock.map((part) => {
                  const needed = Math.max(part.min_stock_level * 2 - part.stock_quantity, 1);
                  return (
                    <div
                      key={part.id}
                      className="group flex items-center justify-between gap-3 rounded-lg border border-border/80 bg-background/60 p-3 hover:border-amber-500/40 transition"
                    >
                      <div className="flex items-center gap-2.5 min-w-0">
                        <img
                          src={part.images?.[0] || part.image_url || ""}
                          alt={part.name}
                          className="h-10 w-10 shrink-0 rounded-md object-cover border border-border/70 bg-muted"
                        />
                        <div className="min-w-0">
                          <p className="truncate text-xs font-semibold text-foreground">{part.name}</p>
                          <p className="text-[11px] text-muted-foreground font-mono">{part.part_number}</p>
                          <div className="mt-0.5 flex items-center gap-1.5">
                            <span className="text-[11px] text-rose-400 font-semibold">{part.stock_quantity} left</span>
                            <span className="text-[10px] text-muted-foreground">• Min {part.min_stock_level}</span>
                          </div>
                        </div>
                      </div>

                      <Button
                        size="sm"
                        variant="secondary"
                        className="h-7 px-2 text-[11px] shrink-0"
                        onClick={() => {
                          setSelectedForPurchase([part]);
                          setPurchaseModalOpen(true);
                        }}
                      >
                        + {needed}
                      </Button>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Main Filter & Search Toolbar */}
      <div className="flex flex-col gap-3 rounded-xl border border-border/80 bg-card/60 p-3.5 sm:p-4 backdrop-blur-sm">
        <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
          {/* Search bar */}
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search parts by name, SKU/part #, supplier, or category..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-9 pr-9 bg-background/70 border-border/80"
            />
            {search && (
              <button
                onClick={() => setSearch("")}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
              >
                <X className="h-4 w-4" />
              </button>
            )}
          </div>

          {/* Controls: Category, Sort, View Toggle */}
          <div className="flex flex-wrap items-center gap-2 sm:gap-2.5">
            {/* Category Select */}
            <Select value={category} onValueChange={setCategory}>
              <SelectTrigger className="w-[150px] sm:w-[170px] bg-background/70 text-xs">
                <SelectValue placeholder="Category" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Categories ({parts.length})</SelectItem>
                {categories.map((cat) => {
                  const count = parts.filter((p) => p.category === cat).length;
                  return (
                    <SelectItem key={cat} value={cat}>
                      {cat} ({count})
                    </SelectItem>
                  );
                })}
              </SelectContent>
            </Select>

            {/* Sort Select */}
            <Select value={sortBy} onValueChange={(val) => setSortBy(val as SortOption)}>
              <SelectTrigger className="w-[150px] sm:w-[180px] bg-background/70 text-xs">
                <SelectValue placeholder="Sort by" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="urgency">Urgency (Lowest Stock)</SelectItem>
                <SelectItem value="stock_asc">Stock: Low to High</SelectItem>
                <SelectItem value="stock_desc">Stock: High to Low</SelectItem>
                <SelectItem value="name_asc">Name: A to Z</SelectItem>
                <SelectItem value="price_asc">Price: Low to High</SelectItem>
                <SelectItem value="price_desc">Price: High to Low</SelectItem>
              </SelectContent>
            </Select>

            {/* View Mode Toggle */}
            <div className="flex items-center rounded-lg border border-border/80 bg-background/70 p-1">
              <button
                type="button"
                onClick={() => setViewMode("grid")}
                className={`rounded-md p-1.5 transition ${
                  viewMode === "grid"
                    ? "bg-primary text-primary-foreground shadow-xs"
                    : "text-muted-foreground hover:text-foreground"
                }`}
                title="Grid Card View"
              >
                <LayoutGrid className="h-4 w-4" />
              </button>
              <button
                type="button"
                onClick={() => setViewMode("table")}
                className={`rounded-md p-1.5 transition ${
                  viewMode === "table"
                    ? "bg-primary text-primary-foreground shadow-xs"
                    : "text-muted-foreground hover:text-foreground"
                }`}
                title="Table List View"
              >
                <List className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>

        {/* Stock Filter Pills & Results Summary */}
        <div className="flex flex-wrap items-center justify-between gap-2 border-t border-border/60 pt-3">
          <div className="flex flex-wrap items-center gap-1.5">
            <span className="text-xs text-muted-foreground mr-1">Status:</span>
            <button
              onClick={() => setStockFilter("all")}
              className={`rounded-full px-3 py-1 text-xs font-medium transition ${
                stockFilter === "all"
                  ? "bg-foreground text-background font-semibold"
                  : "bg-muted/70 text-muted-foreground hover:bg-muted"
              }`}
            >
              All ({parts.length})
            </button>
            <button
              onClick={() => setStockFilter("low_stock")}
              className={`rounded-full px-3 py-1 text-xs font-medium transition flex items-center gap-1.5 ${
                stockFilter === "low_stock"
                  ? "bg-amber-500 text-black font-semibold"
                  : "bg-muted/70 text-muted-foreground hover:bg-muted"
              }`}
            >
              <span>Low Stock</span>
              {lowStock.length > 0 && (
                <span className="rounded-full bg-black/20 px-1.5 py-0.2 text-[10px] font-bold">
                  {lowStock.length}
                </span>
              )}
            </button>
            <button
              onClick={() => setStockFilter("optimal")}
              className={`rounded-full px-3 py-1 text-xs font-medium transition ${
                stockFilter === "optimal"
                  ? "bg-emerald-600 text-white font-semibold"
                  : "bg-muted/70 text-muted-foreground hover:bg-muted"
              }`}
            >
              Optimal ({parts.length - lowStock.length})
            </button>

            {hasActiveFilters && (
              <Button
                variant="ghost"
                size="sm"
                onClick={clearAllFilters}
                className="h-7 text-xs text-muted-foreground hover:text-foreground ml-1 gap-1"
              >
                <RotateCcw className="h-3 w-3" />
                Reset filters
              </Button>
            )}
          </div>

          <div className="text-xs text-muted-foreground">
            Showing <span className="font-semibold text-foreground">{filteredParts.length}</span> of {parts.length} parts
          </div>
        </div>
      </div>

      {/* Main Content: Grid View or Table View */}
      {filteredParts.length === 0 ? (
        <Card className="border-border/80 bg-card/40 p-12 text-center">
          <div className="flex flex-col items-center justify-center space-y-3">
            <div className="rounded-full bg-muted p-4 text-muted-foreground">
              <PackageSearch className="h-8 w-8" />
            </div>
            <h3 className="text-base font-semibold text-foreground">No matching parts found</h3>
            <p className="max-w-md text-xs text-muted-foreground">
              No inventory parts match your current search and filter settings. Try adjusting your query or resetting filters.
            </p>
            <Button variant="outline" size="sm" onClick={clearAllFilters} className="mt-2">
              Clear All Filters
            </Button>
          </div>
        </Card>
      ) : viewMode === "grid" ? (
        /* GRID VIEW */
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {filteredParts.map((part) => {
            const isLow = part.stock_quantity < part.min_stock_level;
            const isOutOfStock = part.stock_quantity === 0;
            const stockPercent = Math.min(100, Math.round((part.stock_quantity / Math.max(part.min_stock_level, 1)) * 100));

            return (
              <Card
                key={part.id}
                className="group relative flex flex-col justify-between overflow-hidden border-border/80 bg-card/70 transition-all duration-200 hover:border-primary/50 hover:shadow-lg hover:shadow-primary/5"
              >
                <div>
                  {/* Card Header & Image */}
                  <div className="relative aspect-[16/10] w-full overflow-hidden bg-muted border-b border-border/60">
                    {part.images?.[0] || part.image_url ? (
                      <img
                        src={part.images?.[0] || part.image_url || ""}
                        alt={part.name}
                        className="h-full w-full object-cover transition duration-300 group-hover:scale-105"
                      />
                    ) : (
                      <div className="flex h-full w-full items-center justify-center text-muted-foreground">
                        <Package className="h-10 w-10 opacity-40" />
                      </div>
                    )}

                    {/* Floating Category Pill */}
                    <div className="absolute left-2.5 top-2.5">
                      <Badge variant="secondary" className="bg-black/60 backdrop-blur-md text-[11px] font-medium text-white border-white/10">
                        {part.category || "General"}
                      </Badge>
                    </div>

                    {/* Floating Status Badge */}
                    <div className="absolute right-2.5 top-2.5">
                      {isOutOfStock ? (
                        <Badge variant="destructive" className="text-[11px] font-semibold">
                          Out of stock
                        </Badge>
                      ) : isLow ? (
                        <Badge variant="warning" className="text-[11px] font-semibold bg-amber-500 text-black">
                          Low: {part.stock_quantity}
                        </Badge>
                      ) : (
                        <Badge variant="success" className="text-[11px] font-semibold bg-emerald-600/90 backdrop-blur-md text-white">
                          In stock: {part.stock_quantity}
                        </Badge>
                      )}
                    </div>

                    {/* Quick Action Overlay on hover */}
                    <div className="absolute inset-0 bg-black/40 opacity-0 transition-opacity duration-200 group-hover:opacity-100 flex items-center justify-center gap-2">
                      <Button
                        size="sm"
                        variant="secondary"
                        className="h-8 bg-black/75 hover:bg-black text-white text-xs gap-1.5 backdrop-blur-sm border border-white/20"
                        onClick={() => setPreviewPart(part)}
                      >
                        <Eye className="h-3.5 w-3.5" />
                        Details
                      </Button>
                      <Button
                        size="sm"
                        variant="secondary"
                        className="h-8 bg-black/75 hover:bg-black text-white text-xs gap-1.5 backdrop-blur-sm border border-white/20"
                        onClick={() => setBarcodePart(part)}
                      >
                        <Barcode className="h-3.5 w-3.5" />
                        Barcode
                      </Button>
                    </div>
                  </div>

                  {/* Card Body */}
                  <div className="p-4 space-y-3">
                    {/* Title & SKU */}
                    <div>
                      <div className="flex items-start justify-between gap-2">
                        <h3
                          onClick={() => setPreviewPart(part)}
                          className="font-semibold text-sm text-foreground line-clamp-1 hover:text-primary cursor-pointer"
                          title={part.name}
                        >
                          {part.name}
                        </h3>
                        <span className="text-sm font-bold text-primary shrink-0">
                          ${part.unit_price?.toFixed(2)}
                        </span>
                      </div>

                      <div className="mt-1 flex items-center gap-2 text-xs text-muted-foreground font-mono">
                        <span>{part.part_number}</span>
                        <button
                          onClick={() => copyPartNumber(part.part_number)}
                          className="text-muted-foreground/70 hover:text-foreground transition"
                          title="Copy part number"
                        >
                          {copiedPartNumber === part.part_number ? (
                            <Check className="h-3 w-3 text-emerald-400" />
                          ) : (
                            <Copy className="h-3 w-3" />
                          )}
                        </button>
                      </div>
                    </div>

                    {/* Supplier info */}
                    {part.supplier && (
                      <div className="flex items-center gap-1.5 text-xs text-muted-foreground truncate">
                        <Building2 className="h-3.5 w-3.5 shrink-0 opacity-70" />
                        <span className="truncate">{part.supplier}</span>
                      </div>
                    )}

                    {/* Stock Health Visual Meter */}
                    <div className="space-y-1.5 pt-1">
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-muted-foreground text-[11px]">Stock Level</span>
                        <span className={`font-semibold text-[11px] ${isLow ? "text-amber-400" : "text-emerald-400"}`}>
                          {part.stock_quantity} / {part.min_stock_level} min
                        </span>
                      </div>
                      <div className="h-2 w-full overflow-hidden rounded-full bg-secondary/80">
                        <div
                          className={`h-full transition-all duration-300 ${
                            isOutOfStock
                              ? "bg-rose-500"
                              : isLow
                              ? "bg-amber-500"
                              : "bg-emerald-500"
                          }`}
                          style={{ width: `${Math.min(stockPercent, 100)}%` }}
                        />
                      </div>
                    </div>
                  </div>
                </div>

                {/* Card Actions Footer */}
                <div className="p-4 pt-0 space-y-2">
                  {machineFilter && (
                    <Button size="sm" variant="outline" className="w-full text-xs gap-1 border-primary/40 text-primary hover:bg-primary/10">
                      <Wrench className="h-3.5 w-3.5" />
                      Use in current repair
                    </Button>
                  )}

                  <div className="flex items-center gap-2">
                    <Button
                      size="sm"
                      variant="secondary"
                      className="flex-1 text-xs gap-1.5 bg-secondary hover:bg-secondary/80 font-medium"
                      onClick={() => {
                        setSelectedForPurchase([part]);
                        setPurchaseModalOpen(true);
                      }}
                    >
                      <ShoppingCart className="h-3.5 w-3.5" />
                      Restock
                    </Button>

                    <Button
                      size="sm"
                      variant="outline"
                      className="px-2.5 text-xs text-muted-foreground hover:text-foreground"
                      onClick={() => setBarcodePart(part)}
                      title="Generate and view barcode label"
                    >
                      <Barcode className="h-4 w-4" />
                    </Button>

                    {isAdmin && (
                      <div title="Manage photos">
                        <ImageManager
                          entityType="part"
                          entityId={part.id}
                          existingImages={part.images || []}
                          onImagesUpdate={async (newImages) => {
                            const updatedParts = parts.map((p) =>
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
                      </div>
                    )}
                  </div>
                </div>
              </Card>
            );
          })}
        </div>
      ) : (
        /* TABLE / LIST VIEW */
        <div className="overflow-x-auto rounded-xl border border-border/80 bg-card/60 backdrop-blur-sm">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-border/80 bg-muted/40 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              <tr>
                <th className="py-3.5 pl-4 pr-3">Part Details</th>
                <th className="px-3 py-3.5">Category</th>
                <th className="px-3 py-3.5 min-w-[140px]">Stock Level</th>
                <th className="px-3 py-3.5">Status</th>
                <th className="px-3 py-3.5">Unit Price</th>
                <th className="px-3 py-3.5">Supplier</th>
                <th className="py-3.5 pl-3 pr-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/60">
              {filteredParts.map((part) => {
                const isLow = part.stock_quantity < part.min_stock_level;
                const isOutOfStock = part.stock_quantity === 0;
                const stockPercent = Math.min(100, Math.round((part.stock_quantity / Math.max(part.min_stock_level, 1)) * 100));

                return (
                  <tr
                    key={part.id}
                    className="hover:bg-muted/20 transition-colors"
                  >
                    {/* Part Details (Image + Name + SKU) */}
                    <td className="py-3 pl-4 pr-3">
                      <div className="flex items-center gap-3">
                        <button
                          type="button"
                          onClick={() => setPreviewPart(part)}
                          className="h-10 w-10 shrink-0 overflow-hidden rounded-lg border border-border/80 bg-muted focus:outline-none focus:ring-1 focus:ring-primary"
                        >
                          <img
                            src={part.images?.[0] || part.image_url || ""}
                            alt={part.name}
                            className="h-full w-full object-cover"
                          />
                        </button>
                        <div className="min-w-0">
                          <p
                            onClick={() => setPreviewPart(part)}
                            className="font-medium text-foreground hover:text-primary cursor-pointer truncate max-w-[220px]"
                            title={part.name}
                          >
                            {part.name}
                          </p>
                          <div className="flex items-center gap-1.5 text-xs text-muted-foreground font-mono">
                            <span>{part.part_number}</span>
                            <button
                              onClick={() => copyPartNumber(part.part_number)}
                              className="text-muted-foreground hover:text-foreground"
                              title="Copy SKU"
                            >
                              {copiedPartNumber === part.part_number ? (
                                <Check className="h-3 w-3 text-emerald-400" />
                              ) : (
                                <Copy className="h-3 w-3" />
                              )}
                            </button>
                          </div>
                        </div>
                      </div>
                    </td>

                    {/* Category */}
                    <td className="px-3 py-3 text-xs text-muted-foreground whitespace-nowrap">
                      <Badge variant="outline" className="font-normal">
                        {part.category || "General"}
                      </Badge>
                    </td>

                    {/* Stock Level Bar */}
                    <td className="px-3 py-3 whitespace-nowrap">
                      <div className="space-y-1">
                        <div className="flex items-center justify-between text-xs">
                          <span className="font-semibold text-foreground">{part.stock_quantity}</span>
                          <span className="text-muted-foreground text-[11px]">/ {part.min_stock_level} min</span>
                        </div>
                        <div className="h-1.5 w-28 overflow-hidden rounded-full bg-secondary">
                          <div
                            className={`h-full ${
                              isOutOfStock
                                ? "bg-rose-500"
                                : isLow
                                ? "bg-amber-500"
                                : "bg-emerald-500"
                            }`}
                            style={{ width: `${Math.min(stockPercent, 100)}%` }}
                          />
                        </div>
                      </div>
                    </td>

                    {/* Status Badge */}
                    <td className="px-3 py-3 whitespace-nowrap">
                      {isOutOfStock ? (
                        <Badge variant="destructive" className="text-[11px]">Out of stock</Badge>
                      ) : isLow ? (
                        <Badge variant="warning" className="text-[11px] bg-amber-500 text-black">Low stock</Badge>
                      ) : (
                        <Badge variant="success" className="text-[11px] bg-emerald-600 text-white">Optimal</Badge>
                      )}
                    </td>

                    {/* Unit Price */}
                    <td className="px-3 py-3 whitespace-nowrap text-sm font-semibold text-foreground">
                      ${part.unit_price?.toFixed(2)}
                    </td>

                    {/* Supplier */}
                    <td className="px-3 py-3 text-xs text-muted-foreground whitespace-nowrap">
                      <div>
                        <p className="truncate max-w-[140px] text-foreground">{part.supplier || "Standard OEM"}</p>
                        <p className="text-[10px] text-muted-foreground">{part.lead_time_days ?? 2}d lead time</p>
                      </div>
                    </td>

                    {/* Actions */}
                    <td className="py-3 pl-3 pr-4 text-right whitespace-nowrap">
                      <div className="flex items-center justify-end gap-1.5">
                        <Button
                          size="sm"
                          variant="secondary"
                          className="h-8 text-xs gap-1"
                          onClick={() => {
                            setSelectedForPurchase([part]);
                            setPurchaseModalOpen(true);
                          }}
                        >
                          <ShoppingCart className="h-3 w-3" />
                          Restock
                        </Button>

                        <Button
                          size="sm"
                          variant="outline"
                          className="h-8 px-2 text-xs"
                          onClick={() => setBarcodePart(part)}
                          title="View Barcode"
                        >
                          <Barcode className="h-3.5 w-3.5" />
                        </Button>

                        <Button
                          size="sm"
                          variant="ghost"
                          className="h-8 px-2 text-xs"
                          onClick={() => setPreviewPart(part)}
                          title="View Technical Details"
                        >
                          <Eye className="h-3.5 w-3.5" />
                        </Button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

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

      {/* Dedicated Barcode Generator & Bin Label Modal */}
      <Dialog open={!!barcodePart} onOpenChange={(open) => !open && setBarcodePart(null)}>
        <DialogContent className="max-w-md">
          {barcodePart && (
            <div className="space-y-4">
              <DialogHeader>
                <DialogTitle className="flex items-center gap-2">
                  <Barcode className="h-5 w-5 text-primary" />
                  <span>Barcode & Asset Tag</span>
                </DialogTitle>
                <DialogDescription>
                  Standard Code128 barcode format for warehouse shelving, scanning, and bins.
                </DialogDescription>
              </DialogHeader>

              {/* Printable Physical Label Card */}
              <div
                id="printable-barcode-card"
                className="rounded-xl border border-border bg-white text-black p-5 shadow-sm space-y-3 text-center"
              >
                <div className="flex items-center justify-between border-b border-gray-200 pb-2 text-[10px] font-bold tracking-widest text-gray-500 uppercase">
                  <span>MAINT-AI INVENTORY ASSET</span>
                  <span>{barcodePart.category || "PART"}</span>
                </div>

                <div>
                  <h4 className="font-bold text-base text-gray-900 leading-tight">{barcodePart.name}</h4>
                  <p className="text-xs text-gray-600 font-mono mt-0.5">{barcodePart.part_number}</p>
                </div>

                {/* Real JsBarcode Canvas */}
                <div className="py-2 flex items-center justify-center">
                  <BarcodeGenerator
                    value={barcodePart.part_number}
                    width={2}
                    height={55}
                    displayValue={true}
                    className="overflow-hidden"
                  />
                </div>

                <div className="flex items-center justify-between border-t border-gray-200 pt-2 text-[10px] text-gray-500">
                  <span>Supplier: {barcodePart.supplier || "OEM Direct"}</span>
                  <span>Unit: ${barcodePart.unit_price?.toFixed(2)}</span>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center justify-between gap-2 pt-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => copyPartNumber(barcodePart.part_number)}
                  className="flex-1 text-xs gap-1.5"
                >
                  <Copy className="h-3.5 w-3.5" />
                  Copy Part #
                </Button>

                <Button
                  variant="default"
                  size="sm"
                  onClick={handlePrintBarcode}
                  className="flex-1 text-xs gap-1.5 orange-glow"
                >
                  <Printer className="h-3.5 w-3.5" />
                  Print Label
                </Button>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>

      {/* Part Image & Details Lightbox Modal */}
      <Dialog open={!!previewPart} onOpenChange={(open) => !open && setPreviewPart(null)}>
        <DialogContent className="max-w-lg">
          {previewPart && (
            <div className="space-y-4">
              <DialogHeader>
                <div className="flex items-start justify-between gap-2 pr-6">
                  <div>
                    <DialogTitle className="text-lg font-bold">{previewPart.name}</DialogTitle>
                    <p className="text-xs text-muted-foreground font-mono mt-0.5">
                      SKU: {previewPart.part_number} • {previewPart.category}
                    </p>
                  </div>
                  <span className="text-lg font-bold text-primary">
                    ${previewPart.unit_price?.toFixed(2)}
                  </span>
                </div>
              </DialogHeader>

              {/* Photo Box */}
              <div className="relative aspect-video w-full overflow-hidden rounded-xl border border-border/80 bg-muted">
                {previewPart.images?.[0] || previewPart.image_url ? (
                  <img
                    src={previewPart.images?.[0] || previewPart.image_url || ""}
                    alt={previewPart.name}
                    className="h-full w-full object-cover"
                  />
                ) : (
                  <div className="flex h-full w-full items-center justify-center text-muted-foreground">
                    <Package className="h-16 w-16 opacity-30" />
                  </div>
                )}
                <div className="absolute bottom-2.5 right-2.5">
                  <Button
                    size="sm"
                    variant="secondary"
                    className="h-7 text-xs bg-black/75 hover:bg-black text-white gap-1 backdrop-blur-md"
                    onClick={() => {
                      setBarcodePart(previewPart);
                    }}
                  >
                    <Barcode className="h-3 w-3" />
                    View Barcode
                  </Button>
                </div>
              </div>

              {/* Description */}
              {previewPart.description && (
                <p className="text-xs text-muted-foreground leading-relaxed">
                  {previewPart.description}
                </p>
              )}

              {/* Specs Grid */}
              <div className="grid grid-cols-2 gap-2.5 rounded-xl border border-border/80 bg-muted/30 p-3.5 text-xs">
                <div>
                  <span className="text-muted-foreground text-[11px]">Current Stock</span>
                  <p className={`font-semibold ${previewPart.stock_quantity < previewPart.min_stock_level ? "text-amber-400" : "text-foreground"}`}>
                    {previewPart.stock_quantity} units
                  </p>
                </div>
                <div>
                  <span className="text-muted-foreground text-[11px]">Minimum Safety Level</span>
                  <p className="font-semibold text-foreground">{previewPart.min_stock_level} units</p>
                </div>
                <div>
                  <span className="text-muted-foreground text-[11px]">Supplier / Vendor</span>
                  <p className="font-semibold text-foreground truncate">{previewPart.supplier || "OEM Direct"}</p>
                </div>
                <div>
                  <span className="text-muted-foreground text-[11px]">Lead Time</span>
                  <p className="font-semibold text-foreground">{previewPart.lead_time_days ?? 2} business days</p>
                </div>
              </div>

              {/* Compatible Machines */}
              {previewPart.compatible_machines && previewPart.compatible_machines.length > 0 && (
                <div className="space-y-1.5">
                  <span className="text-xs font-medium text-muted-foreground">Compatible Equipment:</span>
                  <div className="flex flex-wrap gap-1.5">
                    {previewPart.compatible_machines.map((id) => {
                      const matchedMachine = machineMap.get(id);
                      return (
                        <Badge key={id} variant="outline" className="text-[11px] bg-background/60">
                          {matchedMachine?.name || id.slice(0, 8)}
                        </Badge>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* Modal Actions */}
              <div className="pt-2 flex gap-2">
                <Button
                  className="flex-1 orange-glow"
                  onClick={() => {
                    const toOrder = previewPart;
                    setPreviewPart(null);
                    setSelectedForPurchase([toOrder]);
                    setPurchaseModalOpen(true);
                  }}
                >
                  <ShoppingCart className="mr-2 h-4 w-4" />
                  Order / Restock This Part
                </Button>
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
      <Suspense fallback={<div className="p-8 text-center text-sm text-muted-foreground">Loading parts catalog...</div>}>
        <PartsContent />
      </Suspense>
    </AppShell>
  );
}

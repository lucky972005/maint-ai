"use client";

import { useState, useMemo, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import {
  CheckCircle2,
  Clock,
  Minus,
  Package,
  Plus,
  Printer,
  ShoppingCart,
  Trash2,
  Truck,
  Building2,
} from "lucide-react";
import type { Part } from "@/lib/types";
import { toast } from "@/hooks/use-toast";

interface PurchaseRequestModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  parts: Part[];
  initialSelectedParts?: Part[];
  onOrderSubmitted?: (orderedItems: { partId: string; quantity: number; newStock: number }[]) => void;
}

interface OrderItem {
  part: Part;
  quantity: number;
}

export function PurchaseRequestModal({
  open,
  onOpenChange,
  parts,
  initialSelectedParts = [],
  onOrderSubmitted,
}: PurchaseRequestModalProps) {
  const [orderItems, setOrderItems] = useState<OrderItem[]>([]);
  const [poNumber, setPoNumber] = useState("");
  const [notes, setNotes] = useState("");
  const [orderSubmitted, setOrderSubmitted] = useState(false);
  const [submittedPoDetails, setSubmittedPoDetails] = useState<{
    poNumber: string;
    items: OrderItem[];
    total: number;
    date: string;
  } | null>(null);

  // Initialize order items when modal opens or initialSelectedParts changes
  useEffect(() => {
    if (open) {
      setOrderSubmitted(false);
      setPoNumber(`PO-2026-${Math.floor(1000 + Math.random() * 9000)}`);
      
      const defaultItems: Part[] = initialSelectedParts.length > 0 
        ? initialSelectedParts 
        : parts.filter((p) => p.stock_quantity < p.min_stock_level);

      const items: OrderItem[] = defaultItems.map((part) => {
        const needed = Math.max(1, (part.min_stock_level * 2) - part.stock_quantity);
        return {
          part,
          quantity: needed,
        };
      });

      setOrderItems(items);
    }
  }, [open, initialSelectedParts, parts]);

  const updateQuantity = (partId: string, newQty: number) => {
    if (newQty <= 0) {
      removeItem(partId);
      return;
    }
    setOrderItems((prev) =>
      prev.map((item) =>
        item.part.id === partId ? { ...item, quantity: newQty } : item
      )
    );
  };

  const removeItem = (partId: string) => {
    setOrderItems((prev) => prev.filter((item) => item.part.id !== partId));
  };

  const addPartToOrder = (part: Part) => {
    const existing = orderItems.find((item) => item.part.id === part.id);
    if (existing) {
      updateQuantity(part.id, existing.quantity + 1);
    } else {
      const needed = Math.max(1, (part.min_stock_level * 2) - part.stock_quantity);
      setOrderItems((prev) => [...prev, { part, quantity: needed }]);
    }
  };

  const subtotal = useMemo(() => {
    return orderItems.reduce(
      (sum, item) => sum + (item.part.unit_price ?? 0) * item.quantity,
      0
    );
  }, [orderItems]);

  const estTax = useMemo(() => subtotal * 0.08, [subtotal]);
  const shipping = useMemo(() => (orderItems.length > 0 ? 35.0 : 0), [orderItems]);
  const totalAmount = useMemo(() => subtotal + estTax + shipping, [subtotal, estTax, shipping]);

  const availableToAdd = useMemo(() => {
    const orderedIds = new Set(orderItems.map((i) => i.part.id));
    return parts.filter((p) => !orderedIds.has(p.id));
  }, [parts, orderItems]);

  const handleSubmitOrder = () => {
    if (orderItems.length === 0) {
      toast({
        title: "Empty Purchase Order",
        description: "Please add at least one part to purchase.",
        variant: "destructive",
      });
      return;
    }

    const payload = orderItems.map((item) => ({
      partId: item.part.id,
      quantity: item.quantity,
      newStock: item.part.stock_quantity + item.quantity,
    }));

    setSubmittedPoDetails({
      poNumber,
      items: [...orderItems],
      total: totalAmount,
      date: new Date().toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
      }),
    });
    setOrderSubmitted(true);

    if (onOrderSubmitted) {
      onOrderSubmitted(payload);
    }

    toast({
      title: "Purchase Order Submitted",
      description: `${orderItems.length} items ordered under ${poNumber}. Inventory updated.`,
    });
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-h-[90vh] max-w-3xl overflow-y-auto">
        {!orderSubmitted ? (
          <>
            <DialogHeader>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="rounded-lg bg-primary/15 p-2 text-primary">
                    <ShoppingCart className="h-5 w-5" />
                  </div>
                  <div>
                    <DialogTitle className="text-xl">Generate Purchase Request</DialogTitle>
                    <DialogDescription>
                      Review items, verify supplier details, and create restock purchase order.
                    </DialogDescription>
                  </div>
                </div>
                <Badge variant="outline" className="font-mono text-xs">
                  {poNumber}
                </Badge>
              </div>
            </DialogHeader>

            <div className="space-y-4 py-2">
              {/* Order Items List */}
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <h4 className="text-sm font-semibold text-foreground">
                    Order Items ({orderItems.length})
                  </h4>
                  {availableToAdd.length > 0 && (
                    <select
                      className="h-8 rounded-md border border-input bg-background px-2 text-xs text-muted-foreground"
                      onChange={(e) => {
                        const selected = parts.find((p) => p.id === e.target.value);
                        if (selected) addPartToOrder(selected);
                        e.target.value = "";
                      }}
                      defaultValue=""
                    >
                      <option value="" disabled>
                        + Add other part to order...
                      </option>
                      {availableToAdd.map((p) => (
                        <option key={p.id} value={p.id}>
                          {p.name} ({p.part_number}) - ${p.unit_price?.toFixed(2)}
                        </option>
                      ))}
                    </select>
                  )}
                </div>

                {orderItems.length === 0 ? (
                  <div className="rounded-xl border border-dashed border-border p-8 text-center text-muted-foreground">
                    <Package className="mx-auto h-8 w-8 opacity-40 mb-2" />
                    <p className="text-sm">No parts in purchase queue.</p>
                    <p className="text-xs">Select from the dropdown above to add items.</p>
                  </div>
                ) : (
                  <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
                    {orderItems.map(({ part, quantity }) => {
                      const partImg = part.images?.[0] || part.image_url;
                      const lineTotal = (part.unit_price ?? 0) * quantity;
                      const isLow = part.stock_quantity < part.min_stock_level;

                      return (
                        <div
                          key={part.id}
                          className="flex items-center justify-between gap-3 rounded-xl border border-border/80 bg-card/60 p-3 transition hover:border-primary/40"
                        >
                          {/* Part Image & Details */}
                          <div className="flex items-center gap-3 min-w-0 flex-1">
                            <div className="relative h-14 w-14 shrink-0 overflow-hidden rounded-xl border border-border bg-muted">
                              {partImg ? (
                                <img
                                  src={partImg}
                                  alt={part.name}
                                  className="h-full w-full object-cover"
                                />
                              ) : (
                                <div className="flex h-full w-full items-center justify-center text-muted-foreground">
                                  <Package className="h-6 w-6" />
                                </div>
                              )}
                            </div>

                            <div className="min-w-0 flex-1">
                              <div className="flex items-center gap-2">
                                <p className="truncate font-medium text-sm text-foreground">
                                  {part.name}
                                </p>
                                <Badge
                                  variant={isLow ? "destructive" : "secondary"}
                                  className="text-[10px] px-1.5 py-0"
                                >
                                  {part.stock_quantity} in stock
                                </Badge>
                              </div>

                              <p className="text-xs text-muted-foreground truncate">
                                SKU: {part.part_number} • {part.category}
                              </p>

                              <div className="mt-1 flex items-center gap-3 text-[11px] text-muted-foreground">
                                <span className="flex items-center gap-1">
                                  <Building2 className="h-3 w-3 text-primary/70" />
                                  {part.supplier || "OEM Direct"}
                                </span>
                                <span className="flex items-center gap-1">
                                  <Clock className="h-3 w-3 text-primary/70" />
                                  {part.lead_time_days ?? 2}d lead time
                                </span>
                              </div>
                            </div>
                          </div>

                          {/* Quantity Controls & Line Total */}
                          <div className="flex items-center gap-4">
                            <div className="flex items-center rounded-lg border border-border bg-background">
                              <Button
                                variant="ghost"
                                size="sm"
                                className="h-7 w-7 p-0 rounded-l-md"
                                onClick={() => updateQuantity(part.id, quantity - 1)}
                              >
                                <Minus className="h-3 w-3" />
                              </Button>
                              <Input
                                type="number"
                                min="1"
                                value={quantity}
                                onChange={(e) =>
                                  updateQuantity(
                                    part.id,
                                    Math.max(1, parseInt(e.target.value, 10) || 1)
                                  )
                                }
                                className="h-7 w-12 border-0 bg-transparent text-center text-xs focus-visible:ring-0"
                              />
                              <Button
                                variant="ghost"
                                size="sm"
                                className="h-7 w-7 p-0 rounded-r-md"
                                onClick={() => updateQuantity(part.id, quantity + 1)}
                              >
                                <Plus className="h-3 w-3" />
                              </Button>
                            </div>

                            <div className="w-20 text-right">
                              <p className="text-sm font-semibold text-foreground">
                                ${lineTotal.toFixed(2)}
                              </p>
                              <p className="text-[10px] text-muted-foreground">
                                ${part.unit_price?.toFixed(2)} / ea
                              </p>
                            </div>

                            <Button
                              variant="ghost"
                              size="sm"
                              className="h-8 w-8 p-0 text-muted-foreground hover:text-destructive"
                              onClick={() => removeItem(part.id)}
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>

              {/* Order Cost & Delivery Summary */}
              {orderItems.length > 0 && (
                <div className="grid gap-3 sm:grid-cols-2 pt-2">
                  <div className="rounded-xl border border-border/70 bg-muted/20 p-3 space-y-2 text-xs">
                    <p className="font-semibold text-foreground flex items-center gap-1.5">
                      <Truck className="h-3.5 w-3.5 text-primary" /> Delivery & Destination
                    </p>
                    <p className="text-muted-foreground">
                      Destination: <span className="text-foreground">Apex Plant, Bay A Warehouse</span>
                    </p>
                    <p className="text-muted-foreground">
                      Requested By: <span className="text-foreground">Maintenance Supervisor</span>
                    </p>
                    <Input
                      placeholder="PO Notes / Reason (e.g. CNC line routine overhaul)"
                      value={notes}
                      onChange={(e) => setNotes(e.target.value)}
                      className="h-8 text-xs mt-1"
                    />
                  </div>

                  <div className="rounded-xl border border-border/70 bg-card p-3 space-y-1.5 text-xs">
                    <div className="flex justify-between text-muted-foreground">
                      <span>Items Subtotal:</span>
                      <span className="font-mono text-foreground">${subtotal.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between text-muted-foreground">
                      <span>Estimated Tax (8%):</span>
                      <span className="font-mono text-foreground">${estTax.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between text-muted-foreground">
                      <span>Freight / Delivery:</span>
                      <span className="font-mono text-foreground">${shipping.toFixed(2)}</span>
                    </div>
                    <div className="border-t border-border pt-1 flex justify-between text-sm font-bold text-foreground">
                      <span>Total Estimated Cost:</span>
                      <span className="text-primary font-mono">${totalAmount.toFixed(2)}</span>
                    </div>
                  </div>
                </div>
              )}
            </div>

            <DialogFooter className="gap-2 sm:gap-0">
              <Button variant="outline" onClick={() => onOpenChange(false)}>
                Cancel
              </Button>
              <Button
                onClick={handleSubmitOrder}
                disabled={orderItems.length === 0}
                className="orange-glow"
              >
                <CheckCircle2 className="mr-1.5 h-4 w-4" />
                Submit Purchase Order
              </Button>
            </DialogFooter>
          </>
        ) : (
          /* Order Confirmation View */
          <div className="space-y-6 py-4 text-center">
            <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-green-500/15 text-green-400">
              <CheckCircle2 className="h-10 w-10" />
            </div>

            <div>
              <h3 className="text-xl font-bold">Purchase Order Placed Successfully!</h3>
              <p className="mt-1 text-sm text-muted-foreground">
                PO <span className="font-mono font-semibold text-primary">{submittedPoDetails?.poNumber}</span> has been dispatched to suppliers.
              </p>
            </div>

            {/* Receipt Summary Card */}
            <Card className="text-left border-border/80 bg-muted/30">
              <CardContent className="p-4 space-y-3">
                <div className="flex justify-between items-center border-b border-border pb-2 text-xs text-muted-foreground">
                  <span>Date: {submittedPoDetails?.date}</span>
                  <span>Status: <Badge variant="success" className="text-[10px]">Approved & Issued</Badge></span>
                </div>

                <div className="space-y-2 max-h-48 overflow-y-auto">
                  {submittedPoDetails?.items.map((item) => (
                    <div key={item.part.id} className="flex items-center justify-between text-xs">
                      <div className="flex items-center gap-2">
                        <img
                          src={item.part.images?.[0] || item.part.image_url || ""}
                          alt={item.part.name}
                          className="h-7 w-7 rounded object-cover border border-border"
                        />
                        <div>
                          <p className="font-medium text-foreground">{item.part.name}</p>
                          <p className="text-[10px] text-muted-foreground">{item.part.part_number}</p>
                        </div>
                      </div>
                      <div className="text-right font-mono">
                        <p>{item.quantity} units</p>
                        <p className="text-muted-foreground">
                          ${((item.part.unit_price ?? 0) * item.quantity).toFixed(2)}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="border-t border-border pt-2 flex justify-between text-sm font-bold">
                  <span>Total Order Amount:</span>
                  <span className="text-primary font-mono">
                    ${submittedPoDetails?.total.toFixed(2)}
                  </span>
                </div>
              </CardContent>
            </Card>

            <div className="flex flex-wrap gap-2 justify-center">
              <Button variant="outline" size="sm" onClick={handlePrint}>
                <Printer className="mr-1.5 h-4 w-4" /> Print PO Slip
              </Button>
              <Button size="sm" onClick={() => onOpenChange(false)}>
                Done
              </Button>
            </div>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}

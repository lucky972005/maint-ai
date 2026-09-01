"use client";

import { useEffect, useState, useCallback } from "react";
import { AppShell } from "@/components/layout/app-shell";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Download, Printer, Search, QrCode } from "lucide-react";

import { DEMO_DATA } from "@/lib/demo-data";

interface MachineQRCode {
  machine: {
    id: string;
    name: string;
    model: string | null;
    manufacturer: string | null;
    category: string;
    location: string | null;
    qr_code: string;
    status: string;
  };
  qrCode: string;
}

export default function QRCodesPage() {
  const [qrCodes, setQrCodes] = useState<MachineQRCode[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [useRealData, setUseRealData] = useState(false);

  const loadQRCodes = useCallback(async () => {
    try {
      setLoading(true);
      
      if (useRealData) {
        const response = await fetch("/api/qr-codes");
        if (response.ok) {
          const data = await response.json();
          setQrCodes(data);
        } else {
          console.error("Failed to load QR codes from API");
          setUseRealData(false);
        }
      } else {
        // Generate QR codes for demo data
        const QRCode = (await import("qrcode")).default;
        const demoQRCodes = await Promise.all(
          DEMO_DATA.machines.map(async (machine) => {
            const qrCodeDataUrl = await QRCode.toDataURL(machine.qr_code, {
              width: 300,
              margin: 2,
              color: {
                dark: "#000000",
                light: "#FFFFFF",
              },
            });

            return {
              machine,
              qrCode: qrCodeDataUrl,
            };
          })
        );
        setQrCodes(demoQRCodes);
      }
    } catch (error) {
      console.error("Failed to load QR codes:", error);
    } finally {
      setLoading(false);
    }
  }, [useRealData]);

  useEffect(() => {
    loadQRCodes();
  }, [loadQRCodes]);

  const handlePrint = () => {
    window.print();
  };

  const handleDownloadAll = () => {
    qrCodes.forEach(({ machine, qrCode }, index) => {
      const link = document.createElement("a");
      link.href = qrCode;
      link.download = `qr-code-${machine.name.replace(/\s+/g, "-").toLowerCase()}-${index + 1}.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    });
  };

  const handleDownloadSingle = (qrCode: string, machineName: string) => {
    const link = document.createElement("a");
    link.href = qrCode;
    link.download = `qr-code-${machineName.replace(/\s+/g, "-").toLowerCase()}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const filteredQRCodes = qrCodes.filter(({ machine }) =>
    machine.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    machine.model?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    machine.manufacturer?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    machine.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
    machine.location?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (loading) {
    return (
      <AppShell title="Machine QR Codes">
        <div className="flex items-center justify-center p-8">
          <div className="animate-spin h-8 w-8 border-2 border-primary border-t-transparent rounded-full" />
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell title="Machine QR Codes">
      <div className="space-y-4 px-4 py-4 lg:px-8 lg:py-6">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search machines..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>
          <div className="flex gap-2">
            <Button
              variant="outline"
              onClick={handleDownloadAll}
              disabled={filteredQRCodes.length === 0}
            >
              <Download className="h-4 w-4 mr-2" />
              Download All
            </Button>
            <Button
              variant="outline"
              onClick={handlePrint}
              disabled={filteredQRCodes.length === 0}
            >
              <Printer className="h-4 w-4 mr-2" />
              Print
            </Button>
          </div>
        </div>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {filteredQRCodes.map(({ machine, qrCode }) => (
            <Card key={machine.id} className="overflow-hidden">
              <CardHeader className="pb-3">
                <CardTitle className="text-lg truncate">{machine.name}</CardTitle>
                <div className="flex flex-wrap gap-2 mt-2">
                  <Badge variant="secondary" className="text-xs">
                    {machine.category}
                  </Badge>
                  <Badge
                    variant={
                      machine.status === "operational"
                        ? "success"
                        : machine.status === "broken"
                          ? "destructive"
                          : "warning"
                    }
                    className="text-xs"
                  >
                    {machine.status}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex justify-center bg-white p-4 rounded-lg">
                  <img
                    src={qrCode}
                    alt={`QR Code for ${machine.name}`}
                    className="w-48 h-48 object-contain"
                  />
                </div>
                <div className="space-y-1 text-sm">
                  <p className="text-muted-foreground">
                    <span className="font-medium">Model:</span> {machine.model || "N/A"}
                  </p>
                  <p className="text-muted-foreground">
                    <span className="font-medium">Manufacturer:</span> {machine.manufacturer || "N/A"}
                  </p>
                  <p className="text-muted-foreground">
                    <span className="font-medium">Location:</span> {machine.location || "N/A"}
                  </p>
                  <p className="text-muted-foreground text-xs font-mono">
                    QR: {machine.qr_code}
                  </p>
                </div>
                <Button
                  variant="outline"
                  className="w-full"
                  onClick={() => handleDownloadSingle(qrCode, machine.name)}
                >
                  <Download className="h-4 w-4 mr-2" />
                  Download
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        {filteredQRCodes.length === 0 && (
          <div className="text-center py-12">
            <QrCode className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
            <p className="text-muted-foreground">
              {searchQuery ? "No machines found matching your search." : "No machines available."}
            </p>
          </div>
        )}
      </div>
    </AppShell>
  );
}

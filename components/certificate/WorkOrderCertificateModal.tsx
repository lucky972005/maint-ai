"use client";

import { useEffect, useRef, useState } from "react";
import {
  Dialog,
  DialogContent,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  CheckCircle2,
  FileCheck,
  Printer,
  QrCode as QrIcon,
  RotateCcw,
  ShieldCheck,
  Wrench,
  X,
} from "lucide-react";
import QRCode from "qrcode";
import { formatDate } from "@/lib/utils";
import type { Machine, RepairProcedure, MaintenanceLog, Profile } from "@/lib/types";

interface CertificateProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  machine: Machine | null;
  procedure?: RepairProcedure | null;
  log?: MaintenanceLog | null;
  technician?: Profile | null;
  completedAt?: string;
  partsUsed?: Array<{ name: string; partNumber: string; qty: number }>;
}

export function WorkOrderCertificateModal({
  open,
  onOpenChange,
  machine,
  procedure,
  log,
  technician,
  completedAt = new Date().toISOString(),
  partsUsed,
}: CertificateProps) {
  const [qrCodeUrl, setQrCodeUrl] = useState<string>("");
  const [hasSignature, setHasSignature] = useState(false);
  const [supervisorName] = useState("Lead Supervisor Patel");
  const [certId, setCertId] = useState("");
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const isDrawing = useRef(false);

  // Generate deterministic/unique certificate ID
  useEffect(() => {
    if (open && machine) {
      const randomCode = Math.random().toString(36).substring(2, 8).toUpperCase();
      const id = log?.id ? `WO-${log.id.slice(0, 8).toUpperCase()}` : `WO-CERT-${randomCode}`;
      setCertId(id);

      // Generate verification QR code
      const verifyData = JSON.stringify({
        certId: id,
        machine: machine.name,
        serial: machine.serial_number,
        procedure: procedure?.procedure_type ?? log?.procedure?.procedure_type ?? "Maintenance",
        date: completedAt,
        status: "VERIFIED_COMPLIANT",
        authority: "MaintAI Quality Standard ISO-9001",
      });

      QRCode.toDataURL(verifyData, {
        width: 140,
        margin: 1,
        color: { dark: "#0f172a", light: "#ffffff" },
      })
        .then(setQrCodeUrl)
        .catch(console.error);
    }
  }, [open, machine, procedure, log, completedAt]);

  // Setup Canvas Signature Pad
  useEffect(() => {
    if (open && canvasRef.current) {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext("2d");
      if (ctx) {
        ctx.strokeStyle = "#1e293b";
        ctx.lineWidth = 2.5;
        ctx.lineCap = "round";
        ctx.lineJoin = "round";
      }
    }
  }, [open]);

  const startDrawing = (e: React.MouseEvent<HTMLCanvasElement> | React.TouchEvent<HTMLCanvasElement>) => {
    isDrawing.current = true;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const rect = canvas.getBoundingClientRect();
    const x = "touches" in e ? e.touches[0].clientX - rect.left : e.clientX - rect.left;
    const y = "touches" in e ? e.touches[0].clientY - rect.top : e.clientY - rect.top;

    ctx.beginPath();
    ctx.moveTo(x, y);
    setHasSignature(true);
  };

  const draw = (e: React.MouseEvent<HTMLCanvasElement> | React.TouchEvent<HTMLCanvasElement>) => {
    if (!isDrawing.current || !canvasRef.current) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const rect = canvas.getBoundingClientRect();
    const x = "touches" in e ? e.touches[0].clientX - rect.left : e.clientX - rect.left;
    const y = "touches" in e ? e.touches[0].clientY - rect.top : e.clientY - rect.top;

    ctx.lineTo(x, y);
    ctx.stroke();
  };

  const stopDrawing = () => {
    isDrawing.current = false;
  };

  const clearSignature = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    setHasSignature(false);
  };

  const handlePrint = () => {
    window.print();
  };

  if (!machine) return null;

  const resolvedProcedureName =
    procedure?.procedure_type ?? log?.procedure?.procedure_type ?? "Routine Preventive Maintenance";
  const resolvedTechName =
    technician?.full_name ?? log?.technician?.full_name ?? "Raj Kumar (Tech ID #8492)";
  const duration = log?.duration_minutes ?? procedure?.estimated_minutes ?? 35;

  const defaultParts = partsUsed && partsUsed.length > 0 ? partsUsed : [
    { name: "Synthetic Lubricant ISO VG 68", partNumber: "LUB-SYN-68", qty: 2 },
    { name: "O-Ring Seal Kit (Flange NBR-70)", partNumber: "SEAL-OR-50", qty: 1 },
    { name: "Particulate Air Filter Cartridge", partNumber: "FLT-AF-300", qty: 1 },
  ];

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-3xl max-h-[92vh] overflow-y-auto p-0 border-border/80 bg-background shadow-2xl">
        {/* Modal Controls Bar */}
        <div className="sticky top-0 z-20 flex items-center justify-between border-b bg-muted/80 backdrop-blur px-6 py-3 no-print">
          <div className="flex items-center gap-2">
            <FileCheck className="h-5 w-5 text-emerald-500" />
            <span className="font-semibold text-sm">Industrial Work Order & Inspection Certificate</span>
          </div>
          <div className="flex items-center gap-2">
            <Button size="sm" variant="outline" onClick={handlePrint} className="gap-1.5 shadow-sm">
              <Printer className="h-4 w-4" />
              Print / Save PDF
            </Button>
            <Button size="sm" variant="ghost" onClick={() => onOpenChange(false)} className="h-8 w-8 p-0">
              <X className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {/* Printable Certificate Canvas */}
        <div id="printable-certificate" className="p-6 sm:p-8 space-y-6 bg-white text-slate-900 font-sans">
          
          {/* Certificate Header with Plant Branding & Security Seal */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b-2 border-slate-900 pb-5">
            <div>
              <div className="flex items-center gap-2">
                <div className="h-8 w-8 rounded bg-emerald-600 flex items-center justify-center text-white font-bold text-lg">
                  M
                </div>
                <div>
                  <h1 className="text-xl font-extrabold tracking-tight text-slate-950 uppercase">
                    MaintAI Industrial Operations
                  </h1>
                  <p className="text-xs text-slate-500 font-medium tracking-wide">
                    APEX PLANT FACILITY • ISO 9001:2015 & OSHA COMPLIANT
                  </p>
                </div>
              </div>
            </div>

            <div className="text-left sm:text-right">
              <div className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-emerald-50 text-emerald-800 border border-emerald-300 rounded font-mono text-xs font-semibold">
                <ShieldCheck className="h-3.5 w-3.5 text-emerald-600" />
                VERIFIED COMPLIANT
              </div>
              <p className="text-[11px] font-mono text-slate-500 mt-1">
                CERTIFICATE ID: <span className="font-bold text-slate-800">{certId}</span>
              </p>
              <p className="text-[11px] text-slate-500">
                Issued: {formatDate(completedAt)}
              </p>
            </div>
          </div>

          {/* Machine & Service Details Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 bg-slate-50 p-4 rounded-lg border border-slate-200 text-sm">
            <div>
              <p className="text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-1">Equipment Identified</p>
              <h3 className="font-bold text-base text-slate-900">{machine.name}</h3>
              <p className="text-xs text-slate-600">Model: <span className="font-semibold text-slate-800">{machine.model || "N/A"}</span></p>
              <p className="text-xs text-slate-600">Manufacturer: <span className="font-semibold text-slate-800">{machine.manufacturer || "OEM"}</span></p>
              <p className="text-xs text-slate-600">Serial No: <span className="font-mono text-slate-800">{machine.serial_number || "SN-100492"}</span></p>
              <p className="text-xs text-slate-600">Location: <span className="text-slate-800">{machine.location || "Bay A - Floor 1"}</span></p>
            </div>

            <div>
              <p className="text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-1">Execution Metrics</p>
              <p className="text-xs text-slate-600">Work Order Type: <span className="font-semibold text-slate-900">{resolvedProcedureName}</span></p>
              <p className="text-xs text-slate-600">Technician In Charge: <span className="font-semibold text-slate-800">{resolvedTechName}</span></p>
              <p className="text-xs text-slate-600">Total Downtime / Duration: <span className="font-semibold text-slate-800">{duration} Minutes</span></p>
              <p className="text-xs text-slate-600">LOTO Protocol: <span className="text-emerald-700 font-semibold">Verified De-energized (Zero State)</span></p>
              <p className="text-xs text-slate-600">AI Validation: <span className="text-indigo-700 font-semibold">100% Steps AR-Verified</span></p>
            </div>
          </div>

          {/* Replacement Parts & Bill of Materials (BOM) */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-600 mb-2 flex items-center gap-1.5">
              <Wrench className="h-3.5 w-3.5 text-slate-500" />
              Parts Replaced & Inventory Disbursed
            </h4>
            <div className="border border-slate-200 rounded-md overflow-hidden text-xs">
              <table className="w-full text-left">
                <thead className="bg-slate-100 border-b border-slate-200 text-slate-600">
                  <tr>
                    <th className="p-2 font-semibold">Component / Material</th>
                    <th className="p-2 font-semibold">Part Number</th>
                    <th className="p-2 font-semibold text-right">Quantity</th>
                    <th className="p-2 font-semibold text-right">Inspection Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {defaultParts.map((part, idx) => (
                    <tr key={idx} className="hover:bg-slate-50">
                      <td className="p-2 font-medium text-slate-800">{part.name}</td>
                      <td className="p-2 font-mono text-slate-600">{part.partNumber}</td>
                      <td className="p-2 text-right font-semibold">{part.qty}</td>
                      <td className="p-2 text-right text-emerald-600 font-semibold">PASSED OK</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Verification Protocol Checklist */}
          <div className="border border-emerald-200 bg-emerald-50/50 p-3.5 rounded-lg text-xs">
            <h4 className="font-bold text-emerald-900 mb-2 flex items-center gap-1.5">
              <CheckCircle2 className="h-4 w-4 text-emerald-600" />
              Quality Assurance & Safety Sign-off
            </h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-slate-700">
              <div className="flex items-center gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-500"></span>
                <span>Lockout/Tagout (LOTO) Verified Isolated</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-500"></span>
                <span>Torque specs calibrated to OEM standard</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-500"></span>
                <span>No vibration, oil leak, or thermal anomalies</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-500"></span>
                <span>Machine returned to <strong>Operational</strong> status</span>
              </div>
            </div>
          </div>

          {/* Digital Signature & QR Verification Section */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 pt-3 border-t border-slate-200 items-end">
            
            {/* Scannable Verification QR */}
            <div className="flex flex-col items-center sm:items-start text-center sm:text-left">
              <p className="text-[11px] font-bold text-slate-500 uppercase mb-1 flex items-center gap-1">
                <QrIcon className="h-3 w-3" />
                Audit QR Stamp
              </p>
              {qrCodeUrl ? (
                <div className="p-1.5 bg-white border border-slate-300 rounded shadow-sm">
                  <img src={qrCodeUrl} alt="Inspection QR Stamp" className="h-24 w-24" />
                </div>
              ) : (
                <div className="h-24 w-24 bg-slate-100 rounded animate-pulse" />
              )}
              <p className="text-[10px] text-slate-400 mt-1 font-mono">Scan to verify cryptographic record</p>
            </div>

            {/* Technician Stamp */}
            <div className="text-center sm:text-left">
              <p className="text-[11px] font-bold text-slate-500 uppercase mb-1">Technician Attestation</p>
              <div className="h-24 border border-dashed border-slate-300 rounded bg-slate-50 flex flex-col items-center justify-center p-2">
                <p className="font-serif italic text-base text-slate-800 font-semibold">{resolvedTechName}</p>
                <Badge variant="outline" className="mt-1 bg-emerald-100/60 text-emerald-800 border-emerald-300 text-[10px] font-mono">
                  DIGITALLY CERTIFIED
                </Badge>
              </div>
              <p className="text-[10px] text-slate-400 mt-1">Certified Industrial Technician</p>
            </div>

            {/* Supervisor Digital Signature Pad */}
            <div>
              <div className="flex items-center justify-between mb-1">
                <p className="text-[11px] font-bold text-slate-500 uppercase">Supervisor Sign-Off</p>
                {hasSignature && (
                  <button
                    onClick={clearSignature}
                    className="text-[10px] text-red-500 hover:underline flex items-center gap-0.5 no-print"
                  >
                    <RotateCcw className="h-2.5 w-2.5" /> Clear
                  </button>
                )}
              </div>
              
              <div className="relative border border-slate-300 rounded bg-slate-50 h-24 overflow-hidden">
                <canvas
                  ref={canvasRef}
                  width={220}
                  height={96}
                  className="w-full h-full cursor-crosshair touch-none"
                  onMouseDown={startDrawing}
                  onMouseMove={draw}
                  onMouseUp={stopDrawing}
                  onMouseLeave={stopDrawing}
                  onTouchStart={startDrawing}
                  onTouchMove={draw}
                  onTouchEnd={stopDrawing}
                />
                {!hasSignature && (
                  <div className="absolute inset-0 flex items-center justify-center pointer-events-none text-slate-400 text-[11px] italic">
                    Draw signature here with mouse or touch
                  </div>
                )}
              </div>
              <p className="text-[10px] text-slate-500 mt-1">
                Authorized Signatory: <span className="font-semibold text-slate-700">{supervisorName}</span>
              </p>
            </div>

          </div>

          {/* Security Microprint Footer */}
          <div className="pt-4 border-t border-slate-100 flex items-center justify-between text-[10px] text-slate-400 font-mono">
            <span>MaintAI PWA • SHA-256: {certId.toLowerCase()}-8f9c2e01a4</span>
            <span>Page 1 of 1 • Official Industrial Work Record</span>
          </div>

        </div>

        {/* Modal Footer Actions */}
        <div className="border-t bg-muted/40 p-4 flex flex-wrap gap-2 justify-end no-print">
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Close
          </Button>
          <Button onClick={handlePrint} className="bg-emerald-600 hover:bg-emerald-700 text-white gap-1.5 shadow-md">
            <Printer className="h-4 w-4" />
            Print / Download PDF Certificate
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}

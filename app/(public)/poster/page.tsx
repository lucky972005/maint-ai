'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { ArrowLeft, Printer, RefreshCw, Edit3 } from 'lucide-react';

export default function PosterPage() {
  const [isLandscape, setIsLandscape] = useState(false);
  const [zoom, setZoom] = useState(65);
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    const handleResize = () => {
      const w = window.innerWidth - 60;
      const targetW = isLandscape ? 2245 : 1587;
      const fitZoom = Math.min(100, Math.max(30, Math.round((w / targetW) * 100)));
      setZoom(fitZoom);
    };
    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [isLandscape]);

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="min-h-screen bg-slate-800 text-slate-900 flex flex-col items-center">
      {/* Top Controls Toolbar */}
      <nav aria-label="Poster toolbar" className="sticky top-0 z-50 w-full bg-slate-900/95 backdrop-blur border-b border-slate-700 px-6 py-3 flex flex-wrap justify-between items-center gap-4 text-white shadow-xl print:hidden">
        <div className="flex items-center gap-4">
          <Link
            href="/"
            className="flex items-center gap-2 text-xs font-semibold text-slate-300 hover:text-white bg-slate-800 px-3 py-1.5 rounded-lg border border-slate-700 transition"
          >
            <ArrowLeft className="w-4 h-4" /> Back to App
          </Link>
          <div className="flex items-center gap-2">
            <span className="font-bold text-sm tracking-wide">🎓 MaintAI Final Year UDP Scientific Poster</span>
            <span className="bg-blue-600 text-white text-[10px] font-bold px-2 py-0.5 rounded-full uppercase">
              A2 Size (42 × 59.4 cm)
            </span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {/* Orientation Toggle */}
          <button
            onClick={() => setIsLandscape(!isLandscape)}
            className="flex items-center gap-1.5 bg-slate-800 hover:bg-slate-700 border border-slate-600 px-3 py-1.5 rounded-lg text-xs font-semibold transition"
          >
            <RefreshCw className="w-3.5 h-3.5 text-blue-400" />
            {isLandscape ? 'Switch to Portrait (3-Col)' : 'Switch to Landscape (4-Col)'}
          </button>

          {/* Edit Mode Toggle */}
          <button
            onClick={() => setIsEditing(!isEditing)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold border transition ${
              isEditing
                ? 'bg-amber-600 border-amber-500 text-white shadow-lg'
                : 'bg-slate-800 hover:bg-slate-700 border-slate-600 text-slate-200'
            }`}
          >
            <Edit3 className="w-3.5 h-3.5" />
            {isEditing ? 'Save / Lock Edits' : 'Edit Text'}
          </button>

          {/* Zoom Slider */}
          <div className="flex items-center gap-2 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700 text-xs">
            <span className="text-slate-400 font-medium">Zoom:</span>
            <input
              type="range"
              min="30"
              max="120"
              value={zoom}
              onChange={(e) => setZoom(Number(e.target.value))}
              className="w-20 cursor-pointer accent-blue-500"
            />
            <span className="w-9 font-mono text-slate-300 text-right">{zoom}%</span>
          </div>

          {/* Print Button */}
          <button
            onClick={handlePrint}
            className="flex items-center gap-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs px-4 py-1.5 rounded-lg shadow-md transition"
          >
            <Printer className="w-4 h-4" /> Print / Save PDF
          </button>
        </div>
      </nav>

      {/* Main Poster Container */}
      <div className="p-5 flex justify-center w-full overflow-auto print:p-0 print:m-0 print:w-full">
        <div
          id="a2-poster-root"
          contentEditable={isEditing}
          suppressContentEditableWarning={true}
          style={{
            transform: `scale(${zoom / 100})`,
            transformOrigin: 'top center',
            fontFamily: 'Cambria, Georgia, serif'
          }}
          className={`bg-white shadow-2xl transition-transform duration-150 relative flex flex-col justify-between overflow-hidden print:shadow-none print:transform-none ${
            isLandscape
              ? 'w-[594mm] h-[420mm] min-h-[420mm] p-[8mm_11mm]'
              : 'w-[420mm] h-[594mm] min-h-[594mm] p-[9mm_12mm]'
          }`}
        >
          {/* POSTER HEADER (EXACT USER LOGOS) */}
          <header className="grid grid-cols-[145px_1fr_185px] items-center gap-4 pb-3 mb-3 border-b-[2.5px] border-[#0e2a47]">
            {/* Left: PPSU + NAAC A+ Official Image */}
            <div className="flex items-center justify-start">
              <img
                src="/official_ppsu_naac.png"
                alt="P P Savani University & NAAC A+"
                className="max-w-[140px] h-auto object-contain"
              />
            </div>

            {/* Center: Title & Authors */}
            <div className="text-center px-2">
              <h1 className="text-[34pt] font-bold text-black leading-[1.15] mb-0.5 tracking-tight">
                MaintAI — AI-Powered Industrial Maintenance Assistant
              </h1>
              <div className="text-[19.5pt] font-semibold text-[#b31b1b] mb-0.5">
                Progressive Web Application with AR Step Guidance, Multimodal Vision & Offline Synchronization
              </div>
              <div className="text-[19.5pt] font-bold text-slate-900 mb-0.5">
                Het Joshi<sup className="text-[#b31b1b] font-bold text-[13pt]">1*</sup>, Mr. Ayush Dodia<sup className="text-[#b31b1b] font-bold text-[13pt]">2</sup>
              </div>
              <div className="text-[14pt] text-slate-700 leading-snug">
                1. Student (Enrollment No: <strong>24SE09CE003</strong>), Department of Computer Engineering<br />
                2. Institute Mentor, School of Engineering, P P Savani University, Surat, Gujarat<br />
                3. P P Savani University (Industry / UDP Organization)
              </div>
            </div>

            {/* Right: School of Engineering Banner */}
            <div className="flex justify-end items-center">
              <img
                src="/official_school_of_engineering.png"
                alt="School of Engineering"
                className="max-w-[180px] h-auto object-contain rounded"
              />
            </div>
          </header>

          {/* PORTRAIT MODE (3-COLUMN SCIENTIFIC GRID) */}
          {!isLandscape && (
            <div className="grid grid-cols-[1fr_1.05fr_1fr] gap-[6.5mm] flex-1 mb-2">
              {/* COLUMN 1 */}
              <div className="flex flex-col gap-[4.5mm] justify-between">
                <div className="bg-white border-[1.5px] border-slate-300 rounded-lg p-3.5 shadow-sm flex-1 flex flex-col justify-between">
                  <div>
                    <div className="inline-block bg-gradient-to-r from-[#b31b1b] to-[#c42424] text-white text-[20pt] font-bold px-4 py-0.5 rounded-full mb-2 shadow-sm">
                      Introduction & Problem Statement
                    </div>
                    <ul className="space-y-1.5 text-[15pt] leading-[1.28] text-slate-800 text-justify list-none pl-0">
                      <li className="relative pl-4.5 before:content-['○'] before:absolute before:left-0 before:text-[#b31b1b] before:font-bold">
                        <strong>$50B+ Industrial Downtime Crisis:</strong> Unplanned machinery breakdown costs global manufacturing over <strong>$50 Billion annually</strong>. Paper manuals and monolithic CMMS cause severe repair latency and manual triage overhead.
                      </li>
                      <li className="relative pl-4.5 before:content-['○'] before:absolute before:left-0 before:text-[#b31b1b] before:font-bold">
                        <strong>Shop-Floor Realities:</strong> Factory environments exhibit intense electromagnetic interference, acoustic ambient noise (&gt;80 dB), and intermittent network dead-zones.
                      </li>
                      <li className="relative pl-4.5 before:content-['○'] before:absolute before:left-0 before:text-[#b31b1b] before:font-bold">
                        <strong>Theoretical Formulation:</strong> Mean Time to Repair is mathematically modeled as an aggregated function of step guidance latency and offline durability:
                        <div className="bg-slate-50 border border-slate-200 rounded p-1.5 my-1 text-center font-serif italic text-[14pt]">
                          MTTR = ∑(T_downtime) / N_repairs = 15.4 min (-68%)
                        </div>
                      </li>
                    </ul>
                  </div>
                </div>

                {/* DETAILED OBJECTIVES BOX */}
                <div className="bg-white border-[1.5px] border-slate-300 rounded-lg p-3.5 shadow-sm flex-1 flex flex-col justify-between">
                  <div>
                    <div className="inline-block bg-gradient-to-r from-[#b31b1b] to-[#c42424] text-white text-[20pt] font-bold px-4 py-0.5 rounded-full mb-2 shadow-sm">
                      Project Objectives
                    </div>
                    <div className="space-y-1.5 text-[14.5pt] leading-[1.24]">
                      <div className="bg-slate-50 border-l-[3.5px] border-[#0e2a47] p-2 rounded-r">
                        <strong className="text-[#0e2a47]">1. Zero-Install Edge PWA:</strong> Sub-1.8s cold boot across Android, iOS, and PC with complete offline caching.
                      </div>
                      <div className="bg-slate-50 border-l-[3.5px] border-[#0e2a47] p-2 rounded-r">
                        <strong className="text-[#0e2a47]">2. Canvas AR Guidance:</strong> Viewport-normalized pulsing target markers with hands-free voice control HUD.
                      </div>
                      <div className="bg-slate-50 border-l-[3.5px] border-[#0e2a47] p-2 rounded-r">
                        <strong className="text-[#0e2a47]">3. AI Vision Gatekeeper:</strong> Gemini 1.5 Flash / GPT-4o verifying tool selection before unlocking steps.
                      </div>
                      <div className="bg-slate-50 border-l-[3.5px] border-[#0e2a47] p-2 rounded-r">
                        <strong className="text-[#0e2a47]">4. Offline Write-Ahead Logging:</strong> Dexie.js (IndexedDB) with atomic mutation queueing and cloud auto-sync.
                      </div>
                      <div className="bg-slate-50 border-l-[3.5px] border-[#0e2a47] p-2 rounded-r">
                        <strong className="text-[#0e2a47]">5. Predictive Intelligence:</strong> Supervisor analytics tracking MTTR, downtime, and machine health indices.
                      </div>
                    </div>
                  </div>
                </div>

                {/* System Architecture */}
                <div className="bg-white border-[1.5px] border-slate-300 rounded-lg p-3.5 shadow-sm flex-1 flex flex-col justify-between">
                  <div>
                    <div className="inline-block bg-gradient-to-r from-[#b31b1b] to-[#c42424] text-white text-[20pt] font-bold px-4 py-0.5 rounded-full mb-1.5 shadow-sm">
                      3-Tier Production Architecture
                    </div>
                    <p className="text-[14pt] text-slate-700 leading-snug mb-1">
                      Decoupled architecture separating client edge caching, serverless API dispatch, and cloud persistence:
                    </p>
                  </div>
                  <div className="bg-slate-50 border border-slate-200 rounded p-1.5 text-center">
                    <img src="/updated_architecture_diagram.png" alt="Architecture" className="max-h-[125px] mx-auto object-contain" />
                    <div className="text-[12pt] italic text-slate-600 mt-1">Figure 1. MaintAI 3-Tier Production Architecture Flowchart</div>
                  </div>
                </div>
              </div>

              {/* COLUMN 2 */}
              <div className="flex flex-col gap-[4.5mm] justify-between">
                <div className="bg-white border-[1.5px] border-slate-300 rounded-lg p-3.5 shadow-sm flex-1 flex flex-col justify-between">
                  <div>
                    <div className="inline-block bg-gradient-to-r from-[#b31b1b] to-[#c42424] text-white text-[20pt] font-bold px-4 py-0.5 rounded-full mb-2 shadow-sm">
                      AR Guidance & AI Tool Gating
                    </div>
                    <ul className="space-y-1.5 text-[15pt] leading-[1.28] text-slate-800 text-justify list-none pl-0">
                      <li className="relative pl-4.5 before:content-['○'] before:absolute before:left-0 before:text-[#b31b1b] before:font-bold">
                        <strong>Canvas AR Overlays:</strong> Dynamically renders animated pulsing red crosshairs and target bounding boxes directly onto live camera feeds.
                      </li>
                      <li className="relative pl-4.5 before:content-['○'] before:absolute before:left-0 before:text-[#b31b1b] before:font-bold">
                        <strong>Acoustic Voice Control:</strong> Web Speech API pipeline with fuzzy matching enables hands-free repair navigation (<em>&quot;Next&quot;</em>, <em>&quot;Repeat&quot;</em>).
                      </li>
                      <li className="relative pl-4.5 before:content-['○'] before:absolute before:left-0 before:text-[#b31b1b] before:font-bold">
                        <strong>Multimodal Tool Gatekeeper:</strong> Gemini 1.5 Flash vision verifies mandatory tool presence before step progression.
                      </li>
                    </ul>
                  </div>
                  <div className="grid grid-cols-2 gap-2 mt-2">
                    <div className="bg-slate-50 border border-slate-200 rounded p-1 text-center">
                      <img src="/p12_img4_73.png" alt="AR Step" className="max-h-[110px] mx-auto object-contain" />
                      <div className="text-[11pt] italic text-slate-600 mt-0.5">Figure 2. AR Step Viewport</div>
                    </div>
                    <div className="bg-slate-50 border border-slate-200 rounded p-1 text-center">
                      <img src="/p13_img3_76.png" alt="Tool Check" className="max-h-[110px] mx-auto object-contain" />
                      <div className="text-[11pt] italic text-slate-600 mt-0.5">Figure 3. AI Tool Detector</div>
                    </div>
                  </div>
                </div>

                {/* REDESIGNED FIGURE 4 SVG */}
                <div className="bg-white border-[1.5px] border-slate-300 rounded-lg p-3.5 shadow-sm flex-1 flex flex-col justify-between">
                  <div>
                    <div className="inline-block bg-gradient-to-r from-[#b31b1b] to-[#c42424] text-white text-[20pt] font-bold px-4 py-0.5 rounded-full mb-2 shadow-sm">
                      Offline Sync & State Machine
                    </div>
                    <ul className="space-y-1.5 text-[15pt] leading-[1.28] text-slate-800 text-justify list-none pl-0">
                      <li className="relative pl-4.5 before:content-['○'] before:absolute before:left-0 before:text-[#b31b1b] before:font-bold">
                        <strong>IndexedDB Persistence:</strong> Complete machine specs, step procedures, and manuals cached locally via Dexie.js for 100% offline uptime.
                      </li>
                      <li className="relative pl-4.5 before:content-['○'] before:absolute before:left-0 before:text-[#b31b1b] before:font-bold">
                        <strong>Write-Ahead Logging (WAL):</strong> Offline mutation queue records work orders with idempotency UUIDs; automatically flushes on reconnect.
                      </li>
                    </ul>
                  </div>
                  <div className="bg-white border border-slate-300 rounded p-1 mt-1 text-center">
                    <img src="/fig4_redesigned_offline_sync.svg" alt="Sync Flow" className="max-h-[140px] w-full mx-auto object-contain" />
                    <div className="text-[12pt] italic text-slate-600 mt-0.5">Figure 4. Handcrafted Offline Write-Ahead Logging & Sync Engine State Machine</div>
                  </div>
                </div>

                <div className="bg-white border-[1.5px] border-slate-300 rounded-lg p-3.5 shadow-sm">
                  <div className="inline-block bg-gradient-to-r from-[#b31b1b] to-[#c42424] text-white text-[20pt] font-bold px-4 py-0.5 rounded-full mb-1.5 shadow-sm">
                    Multi-Provider AI Abstraction
                  </div>
                  <p className="text-[14pt] leading-normal text-slate-700 text-justify">
                    Unified AI wrapper with dynamic failover between <strong>Google Gemini 1.5 Flash</strong> (1.18s), <strong>OpenAI GPT-4o</strong> (1.82s), and <strong>Groq Llama 3</strong> (0.64s), backed by zero-key local mock fallback.
                  </p>
                </div>
              </div>

              {/* COLUMN 3 */}
              <div className="flex flex-col gap-[4.5mm] justify-between">
                <div className="bg-white border-[1.5px] border-slate-300 rounded-lg p-3.5 shadow-sm flex-1 flex flex-col justify-between">
                  <div>
                    <div className="inline-block bg-gradient-to-r from-[#b31b1b] to-[#c42424] text-white text-[20pt] font-bold px-4 py-0.5 rounded-full mb-2 shadow-sm">
                      Results and Discussion
                    </div>

                    <div className="grid grid-cols-4 gap-1.5 my-1.5 font-sans">
                      <div className="bg-slate-100 border rounded p-1.5 text-center"><div className="text-[19pt] font-extrabold text-[#b31b1b]">-68%</div><div className="text-[9pt] font-bold text-slate-600">MTTR</div></div>
                      <div className="bg-slate-100 border rounded p-1.5 text-center"><div className="text-[19pt] font-extrabold text-[#b31b1b]">99.4%</div><div className="text-[9pt] font-bold text-slate-600">Precision</div></div>
                      <div className="bg-slate-100 border rounded p-1.5 text-center"><div className="text-[19pt] font-extrabold text-[#b31b1b]">&lt;1.8s</div><div className="text-[9pt] font-bold text-slate-600">Load</div></div>
                      <div className="bg-slate-100 border rounded p-1.5 text-center"><div className="text-[19pt] font-extrabold text-[#b31b1b]">100%</div><div className="text-[9pt] font-bold text-slate-600">Offline</div></div>
                    </div>

                    <table className="w-full text-[12.5pt] border-collapse my-1.5">
                      <thead>
                        <tr className="bg-[#0e2a47] text-white">
                          <th className="p-1.5 text-left">Metric</th>
                          <th className="p-1.5 text-left">Legacy CMMS</th>
                          <th className="p-1.5 text-left">MaintAI</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr className="border-b"><td className="p-1 font-semibold">MTTR</td><td className="p-1">48.0 min</td><td className="p-1 font-bold text-emerald-700">15.4 min</td></tr>
                        <tr className="border-b bg-slate-50"><td className="p-1 font-semibold">Tool Check</td><td className="p-1">Manual</td><td className="p-1 font-bold text-emerald-700">1.24s (AI)</td></tr>
                        <tr className="border-b"><td className="p-1 font-semibold">Offline Uptime</td><td className="p-1">0%</td><td className="p-1 font-bold text-emerald-700">100%</td></tr>
                        <tr className="bg-slate-50"><td className="p-1 font-semibold">Test Suites</td><td className="p-1">Manual</td><td className="p-1 font-bold text-emerald-700">74/74 (100%)</td></tr>
                      </tbody>
                    </table>
                  </div>

                  <div className="grid grid-cols-2 gap-2 mt-1">
                    <div className="bg-slate-50 border border-slate-200 rounded p-1 text-center">
                      <img src="/p15_img3_84.png" alt="Analytics" className="max-h-[105px] mx-auto object-contain" />
                      <div className="text-[10.5pt] italic text-slate-600 mt-0.5">Figure 5. Supervisor Analytics</div>
                    </div>
                    <div className="bg-slate-50 border border-slate-200 rounded p-1 text-center">
                      <img src="/p14_img4_81.png" alt="Fleet QR" className="max-h-[105px] mx-auto object-contain" />
                      <div className="text-[10.5pt] italic text-slate-600 mt-0.5">Figure 6. Fleet QR Tagging</div>
                    </div>
                  </div>
                </div>

                <div className="bg-white border-[1.5px] border-slate-300 rounded-lg p-3.5 shadow-sm flex-1 flex flex-col justify-between">
                  <div>
                    <div className="inline-block bg-gradient-to-r from-[#b31b1b] to-[#c42424] text-white text-[20pt] font-bold px-4 py-0.5 rounded-full mb-2 shadow-sm">
                      Conclusions & Future Scope
                    </div>
                    <ul className="space-y-1.5 text-[14pt] leading-[1.28] text-slate-800 text-justify list-none pl-0">
                      <li className="relative pl-4.5 before:content-['○'] before:absolute before:left-0 before:text-[#b31b1b] before:font-bold">
                        <strong>System Validation:</strong> Demonstrates that combining edge PWAs with multimodal AI drastically cuts maintenance latency.
                      </li>
                      <li className="relative pl-4.5 before:content-['○'] before:absolute before:left-0 before:text-[#b31b1b] before:font-bold">
                        <strong>Applications:</strong> Automotive assembly, CNC machining, chemical plants, and wind turbine fleets.
                      </li>
                      <li className="relative pl-4.5 before:content-['○'] before:absolute before:left-0 before:text-[#b31b1b] before:font-bold">
                        <strong>Future Scope:</strong> WebXR spatial anchors, edge WASM YOLOv8, and IoT OPC-UA telemetry.
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* POSTER FOOTER */}
          <footer className="pt-2.5 border-t-2 border-[#0e2a47] grid grid-cols-[1fr_105px] gap-3 items-center">
            <div className="text-[11pt] text-slate-700 leading-snug">
              <strong className="text-[#0e2a47] font-bold block mb-0.5">References (APA 7th Edition):</strong>
              <ol className="list-decimal pl-4 space-y-0.5">
                <li>Palmarini, R., et al. (2018). <em>A systematic review of augmented reality in maintenance.</em> RCIM, 49, 215–228.</li>
                <li>Ismail, L., et al. (2025). <em>Digital twin predictive maintenance in industrial engineering.</em> arXiv:2509.24443.</li>
                <li>Vercel Inc. (2026). <em>Next.js 14 Documentation: App Router & Serverless Functions.</em> https://nextjs.org/docs</li>
                <li>Supabase Inc. (2026). <em>PostgreSQL Row Level Security and Realtime Engine.</em> https://supabase.com/docs</li>
                <li>Google DeepMind. (2026). <em>Gemini API: Multimodal Computer Vision for Enterprise.</em> https://ai.google.dev</li>
              </ol>
            </div>

            <div className="flex flex-col items-center text-center font-sans">
              <div className="w-[86px] h-[86px] bg-slate-100 border border-slate-300 rounded p-1 flex items-center justify-center font-mono text-[8pt] text-slate-600">
                [QR Code]
              </div>
              <div className="text-[8.5pt] font-bold text-[#0e2a47] mt-0.5">
                Scan for Demo
              </div>
            </div>
          </footer>
        </div>
      </div>
    </div>
  );
}

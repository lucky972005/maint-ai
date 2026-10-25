const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

async function exportPdf() {
  const baseDir = path.resolve(__dirname, '..');
  const posterHtmlPath = path.join(baseDir, 'poster.html');
  const posterUrl = `file:///${posterHtmlPath.replace(/\\\\/g, '/')}`;

  // Check for Edge or Chrome executable
  const chromePaths = [
    'C:\\\\Program Files\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe',
    'C:\\\\Program Files (x86)\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe',
    'C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe',
    'C:\\\\Program Files\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe'
  ];

  let browserPath = null;
  for (const p of chromePaths) {
    if (fs.existsSync(p)) {
      browserPath = p;
      break;
    }
  }

  if (!browserPath) {
    console.error('No Chrome or Edge browser found for headless PDF generation.');
    return;
  }

  console.log(`Using browser for PDF compilation: ${browserPath}`);

  // 1. Export Portrait A2 PDF
  const portraitPdfOutput = path.join(baseDir, 'MaintAI_Poster_A2_Portrait.pdf');
  const portraitCmd = `"${browserPath}" --headless --disable-gpu --run-all-compositor-stages-before-draw --no-pdf-header-footer --print-to-pdf="${portraitPdfOutput}" "${posterUrl}"`;
  
  console.log('Generating Portrait A2 PDF...');
  try {
    execSync(portraitCmd, { stdio: 'inherit' });
    console.log(`✅ Successfully generated: ${portraitPdfOutput} (${fs.statSync(portraitPdfOutput).size} bytes)`);
  } catch (err) {
    console.error('Error generating portrait PDF:', err);
  }

  // 2. Export Landscape HTML and Landscape A2 PDF
  // We create a temporary landscape html file with landscape-mode class pre-applied
  let html = fs.readFileSync(posterHtmlPath, 'utf-8');
  html = html.replace('<article class="poster-canvas" id="posterCanvas">', '<article class="poster-canvas landscape-mode" id="posterCanvas">');
  html = html.replace('@page {\n        size: A2 portrait;\n        margin: 0;\n      }', '@page {\n        size: A2 landscape;\n        margin: 0;\n      }');
  
  const landscapeHtmlPath = path.join(baseDir, 'poster_landscape.html');
  fs.writeFileSync(landscapeHtmlPath, html, 'utf-8');
  const landscapeUrl = `file:///${landscapeHtmlPath.replace(/\\\\/g, '/')}`;

  const landscapePdfOutput = path.join(baseDir, 'MaintAI_Poster_A2_Landscape.pdf');
  const landscapeCmd = `"${browserPath}" --headless --disable-gpu --run-all-compositor-stages-before-draw --no-pdf-header-footer --print-to-pdf="${landscapePdfOutput}" "${landscapeUrl}"`;

  console.log('Generating Landscape A2 PDF...');
  try {
    execSync(landscapeCmd, { stdio: 'inherit' });
    console.log(`✅ Successfully generated: ${landscapePdfOutput} (${fs.statSync(landscapePdfOutput).size} bytes)`);
  } catch (err) {
    console.error('Error generating landscape PDF:', err);
  }
}

exportPdf().catch(console.error);

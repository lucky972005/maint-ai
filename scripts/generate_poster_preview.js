const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

async function exportScreenshot() {
  const baseDir = path.resolve(__dirname, '..');
  const posterHtmlPath = path.join(baseDir, 'poster.html');
  const posterUrl = `file:///${posterHtmlPath.replace(/\\\\/g, '/')}`;

  const chromePaths = [
    'C:\\\\Program Files\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe',
    'C:\\\\Program Files (x86)\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe',
    'C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe'
  ];

  let browserPath = null;
  for (const p of chromePaths) {
    if (fs.existsSync(p)) {
      browserPath = p;
      break;
    }
  }

  if (!browserPath) return;

  const previewOutput = path.join(baseDir, 'MaintAI_Poster_Preview.png');
  // High-res preview capture
  const cmd = `"${browserPath}" --headless --disable-gpu --window-size=1650,2334 --screenshot="${previewOutput}" "${posterUrl}"`;
  
  console.log('Generating preview screenshot...');
  try {
    execSync(cmd, { stdio: 'inherit' });
    console.log(`✅ Generated preview image: ${previewOutput} (${fs.statSync(previewOutput).size} bytes)`);
  } catch (err) {
    console.error('Error generating preview screenshot:', err);
  }
}

exportScreenshot().catch(console.error);

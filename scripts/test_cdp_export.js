const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

async function exportLandscapePdf() {
  const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const port = 9333;
  
  // Launch Chrome with remote debugging
  const chromeProc = spawn(chromePath, [
    '--headless=new',
    `--remote-debugging-port=${port}`,
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    '--run-all-compositor-stages-before-draw'
  ]);

  // Wait for Chrome to initialize
  await new Promise(r => setTimeout(r, 1500));

  try {
    // Get version / browser ws url
    const versionData = await new Promise((resolve, reject) => {
      http.get(`http://127.0.0.1:${port}/json/version`, res => {
        let body = '';
        res.on('data', c => body += c);
        res.on('end', () => resolve(JSON.parse(body)));
      }).on('error', reject);
    });

    console.log('Connected to Chrome version:', versionData.Browser);

    // Get existing targets
    const targetData = await new Promise((resolve, reject) => {
      http.get(`http://127.0.0.1:${port}/json/list`, res => {
        let body = '';
        res.on('data', c => body += c);
        res.on('end', () => resolve(JSON.parse(body)));
      }).on('error', reject);
    });

    const pageWsUrl = targetData[0].webSocketDebuggerUrl;
    console.log('Page WebSocket URL:', pageWsUrl);

    // Connect via native WebSocket
    const ws = new WebSocket(pageWsUrl);
    await new Promise((resolve, reject) => {
      ws.onopen = resolve;
      ws.onerror = reject;
    });

    let msgId = 1;
    function sendCommand(method, params = {}) {
      return new Promise((resolve, reject) => {
        const id = msgId++;
        const handler = (evt) => {
          const resp = JSON.parse(evt.data);
          if (resp.id === id) {
            ws.removeEventListener('message', handler);
            if (resp.error) reject(resp.error);
            else resolve(resp.result);
          }
        };
        ws.addEventListener('message', handler);
        ws.send(JSON.stringify({ id, method, params }));
      });
    }

    // Enable Page
    await sendCommand('Page.enable');

    // Navigate to poster_landscape.html
    const htmlPath = path.resolve(__dirname, '..', 'poster_landscape.html');
    const fileUrl = 'file:///' + htmlPath.replace(/\\/g, '/');
    console.log('Navigating to:', fileUrl);
    await sendCommand('Page.navigate', { url: fileUrl });

    // Wait 2.5 seconds for all images, fonts, styles to render
    await new Promise(r => setTimeout(r, 2500));

    // Print to PDF with exact A2 Landscape settings (594mm x 420mm = 23.3858 x 16.5354 inches)
    console.log('Printing to PDF via CDP...');
    const pdfResult = await sendCommand('Page.printToPDF', {
      paperWidth: 23.3858,
      paperHeight: 16.5354,
      landscape: true,
      preferCSSPageSize: true,
      printBackground: true,
      marginTop: 0,
      marginBottom: 0,
      marginLeft: 0,
      marginRight: 0,
      scale: 1.0
    });

    const pdfBuffer = Buffer.from(pdfResult.data, 'base64');
    const outputPath = path.resolve(__dirname, '..', 'test_cdp_landscape.pdf');
    fs.writeFileSync(outputPath, pdfBuffer);
    console.log(`✅ Success! Generated PDF (${pdfBuffer.length} bytes): ${outputPath}`);

    ws.close();
  } catch (err) {
    console.error('CDP Error:', err);
  } finally {
    chromeProc.kill();
  }
}

exportLandscapePdf();

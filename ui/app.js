const statusText = document.getElementById('statusText');
const diagnostics = document.getElementById('diagnostics');
const previewFrame = document.getElementById('previewFrame');
const downloadPdf = document.getElementById('downloadPdf');
const downloadTex = document.getElementById('downloadTex');
const downloadLog = document.getElementById('downloadLog');

const setStatus = (value) => {
  statusText.textContent = value;
};

const setDownloads = (downloads = null) => {
  const entries = [
    [downloadPdf, downloads?.pdf],
    [downloadTex, downloads?.tex],
    [downloadLog, downloads?.log],
  ];

  for (const [el, url] of entries) {
    if (url) {
      el.href = url;
      el.classList.remove('disabled');
    } else {
      el.href = '#';
      el.classList.add('disabled');
    }
  }
};

const showFailure = (payload) => {
  setStatus('failed');
  diagnostics.textContent = JSON.stringify(payload, null, 2);
  setDownloads(null);
};

const showSuccess = (payload) => {
  setStatus('compiled');
  diagnostics.textContent = JSON.stringify(payload, null, 2);
  if (payload.previewUrl) {
    previewFrame.src = payload.previewUrl;
  }
  setDownloads(payload.downloads);
};

async function generateFromApi() {
  setStatus('submitting');
  diagnostics.textContent = 'Calling /latex/render ...';

  const apiBase = document.getElementById('apiBase').value.trim();
  const body = {
    userId: document.getElementById('userId').value.trim(),
    documentType: document.getElementById('documentType').value,
    templateId: document.getElementById('templateId').value.trim(),
    latexSource: document.getElementById('latexSource').value,
  };

  try {
    setStatus('compiling');
    const response = await fetch(`${apiBase}/latex/render`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    const payload = await response.json();
    if (!response.ok || payload.status === 'failed') {
      showFailure(payload);
      return;
    }
    showSuccess(payload);
  } catch (error) {
    showFailure({
      status: 'failed',
      errorSummary: 'Unable to reach API. Use mock buttons or start backend.',
      detail: String(error),
    });
  }
}

document.getElementById('generateBtn').addEventListener('click', generateFromApi);

document.getElementById('mockSuccessBtn').addEventListener('click', () => {
  showSuccess({
    docId: 'demo-123',
    status: 'compiled',
    previewUrl: 'https://mozilla.github.io/pdf.js/web/compressed.tracemonkey-pldi-09.pdf',
    downloads: {
      pdf: '#',
      tex: '#',
      log: '#',
    },
  });
});

document.getElementById('mockFailBtn').addEventListener('click', () => {
  showFailure({
    status: 'failed',
    errorSummary: 'Undefined control sequence',
    errors: [
      { line: 17, message: 'Undefined control sequence \\foo', severity: 'error' },
      { line: 18, message: 'Missing $ inserted', severity: 'warning' },
    ],
  });
});

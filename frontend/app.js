const THEMES = {
  dark: {
    bg:          '#1a1a1e',
    surface:     '#2a2a2e',
    text:        '#e2e2e2',
    subtext:     '#888888',
    accent:      '#e05252',
    border:      'rgba(255,255,255,0.08)',
    overlay:     'transparent',
    'accent-bg': 'rgba(224,82,82,0.12)',
    'accent-brd':'rgba(224,82,82,0.25)',
  },
  light: {
    bg:          'rgba(242,242,240,0.88)',
    surface:     'rgba(255,255,255,0.60)',
    text:        '#333333',
    subtext:     '#aaaaaa',
    accent:      '#d04040',
    border:      'rgba(0,0,0,0.08)',
    overlay:     'rgba(0,0,0,0.18)',
    'accent-bg': 'rgba(208,64,64,0.10)',
    'accent-brd':'rgba(208,64,64,0.22)',
  },
};

function applyTheme(themeCfg) {
  const root = document.documentElement.style;
  const palette = THEMES[themeCfg.name] ?? THEMES['dark'];
  const merged = { ...palette, ...themeCfg };
  for (const [key, val] of Object.entries(merged)) {
    if (key === 'name') continue;
    root.setProperty(`--${key}`, val);
  }
}

// State machine: idle | recording | processing | done
let state = 'idle';
let timerInterval = null;
let timerSeconds = 0;
let api = null;
let partialChunks = [];

// DOM refs
const recBtn = document.getElementById('rec-btn');
const recIcon = document.getElementById('rec-icon');
const statusEl = document.getElementById('status');
const timerEl = document.getElementById('timer');
const transcriptEl = document.getElementById('transcript');
const placeholderEl = document.getElementById('placeholder');
const checkIcon = document.getElementById('check-icon');
const waveformEl = document.getElementById('waveform');

// Generate 40 waveform bars with random CSS vars
(function buildWaveform() {
  for (let i = 0; i < 40; i++) {
    const bar = document.createElement('div');
    bar.className = 'bar';
    bar.style.setProperty('--hi', (0.4 + Math.random() * 0.6).toFixed(2));
    bar.style.setProperty('--hlo', (0.1 + Math.random() * 0.3).toFixed(2));
    bar.style.setProperty('--d', (Math.random() * 0.8).toFixed(2) + 's');
    waveformEl.appendChild(bar);
  }
})();

function setStatus(text) {
  statusEl.textContent = text;
}

function setBars(mode) {
  waveformEl.className = mode;
}

function resetUi() {
  transcriptEl.textContent = '';
  placeholderEl.style.display = '';
  checkIcon.style.display = 'none';
  timerEl.textContent = '';
  setStatus('');
  setBars('idle');
  recBtn.disabled = false;
  recIcon.className = 'ti ti-microphone';
}

function startTimer() {
  timerSeconds = 0;
  timerEl.textContent = '00:00';
  timerInterval = setInterval(() => {
    timerSeconds++;
    const m = String(Math.floor(timerSeconds / 60)).padStart(2, '0');
    const s = String(timerSeconds % 60).padStart(2, '0');
    timerEl.textContent = `${m}:${s}`;
  }, 1000);
}

function stopTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
  timerEl.textContent = '';
}

function typeText(text, onDone) {
  transcriptEl.textContent = '';
  placeholderEl.style.display = 'none';
  let i = 0;
  function next() {
    if (i < text.length) {
      transcriptEl.textContent += text[i++];
      setTimeout(next, 22);
    } else if (onDone) {
      onDone();
    }
  }
  next();
}

function showCheck() {
  checkIcon.style.display = '';
  setTimeout(() => { checkIcon.style.display = 'none'; }, 2000);
}

async function scheduleClose() {
  const res = await api.get_config();
  if (!res.ok) return;
  const delay = res.data.auto_close_after;
  if (delay === 0) return;
  setTimeout(() => api.close(), delay * 1000);
}

window.onPartialTranscript = function(text) {
  if (state !== 'recording') return;
  partialChunks.push(text);
  placeholderEl.style.display = 'none';
  transcriptEl.textContent = partialChunks.join(' ');
};

async function startRecording() {
  state = 'recording';
  partialChunks = [];
  setBars('active');
  setStatus('gravando');
  recIcon.className = 'ti ti-player-stop';
  placeholderEl.style.display = 'none';
  transcriptEl.textContent = '';
  checkIcon.style.display = 'none';
  startTimer();
  await api.start_recording();
}

async function stopRecording() {
  state = 'processing';
  stopTimer();
  setStatus(partialChunks.length ? 'finalizando...' : 'processando');
  setBars('idle');
  recBtn.disabled = true;
  recIcon.className = 'ti ti-microphone';

  const res = await api.stop_recording();
  recBtn.disabled = false;

  if (!res.ok) {
    setStatus('erro: ' + res.error);
    state = 'idle';
    return;
  }

  const text = res.data.text.trim();
  if (!text) {
    setStatus('nenhum áudio detectado');
    state = 'idle';
    setBars('idle');
    placeholderEl.style.display = '';
    return;
  }

  state = 'done';
  setBars('done');
  setStatus('concluído');
  if (partialChunks.length) {
    placeholderEl.style.display = 'none';
    transcriptEl.textContent = text;
    showCheck();
    scheduleClose();
  } else {
    typeText(text, () => {
      showCheck();
      scheduleClose();
    });
  }
}

function toggleRecord() {
  if (state === 'idle' || state === 'done') startRecording();
  else if (state === 'recording') stopRecording();
}

function handleHotkey() {
  if (state === 'idle') startRecording();
  else if (state === 'recording') stopRecording();
  else if (state === 'done') startRecording();
  // processing → ignore
}

recBtn.addEventListener('click', toggleRecord);

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') api && api.close();
});

// Wait for pywebview to be ready
window.addEventListener('pywebviewready', async () => {
  api = window.pywebview.api;
  const res = await api.get_config();
  if (res.ok) {
    applyTheme(res.data.theme ?? { name: 'dark' });
  }
});

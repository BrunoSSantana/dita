// State machine: idle | recording | processing | done
let state = 'idle';
let timerInterval = null;
let timerSeconds = 0;
let api = null;

const LANGS = ['pt', 'en', 'es', 'fr', 'de', 'auto'];
let langIndex = 0;

// DOM refs
const recBtn = document.getElementById('rec-btn');
const recIcon = document.getElementById('rec-icon');
const clearBtn = document.getElementById('clear-btn');
const copyBtn = document.getElementById('copy-btn');
const langBtn = document.getElementById('lang-btn');
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

async function startRecording() {
  state = 'recording';
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
  setStatus('processando');
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
  typeText(text, () => {
    showCheck();
    scheduleClose();
  });
}

function clearAll() {
  state = 'idle';
  stopTimer();
  resetUi();
}

function toggleRecord() {
  if (state === 'idle' || state === 'done') startRecording();
  else if (state === 'recording') stopRecording();
}

function cycleLang() {
  langIndex = (langIndex + 1) % LANGS.length;
  const lang = LANGS[langIndex];
  langBtn.textContent = lang.toUpperCase();
  api.save_language(lang);
}

function copyManual() {
  const text = transcriptEl.textContent;
  if (!text) return;
  navigator.clipboard.writeText(text).then(() => showCheck());
}

function handleHotkey() {
  if (state === 'idle') startRecording();
  else if (state === 'recording') stopRecording();
  else if (state === 'done') startRecording();
  // processing → ignore
}

// Wire up buttons
recBtn.addEventListener('click', toggleRecord);
clearBtn.addEventListener('click', clearAll);
copyBtn.addEventListener('click', copyManual);
langBtn.addEventListener('click', cycleLang);

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') api && api.close();
});

// Wait for pywebview to be ready
window.addEventListener('pywebviewready', async () => {
  api = window.pywebview.api;
  const res = await api.get_config();
  if (res.ok) {
    const lang = res.data.language || 'pt';
    langIndex = LANGS.indexOf(lang);
    if (langIndex === -1) langIndex = 0;
    langBtn.textContent = LANGS[langIndex].toUpperCase();
  }
});

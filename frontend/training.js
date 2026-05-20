/* ============================================================
   ErenShop Eğitim Platformu — training.js
   ============================================================ */

const API = "/api";
const state = {
  users: [],
  currentUser: null,
  currentRequest: null,
  currentTest: null,
};

// ---------- Yardımcılar ----------
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

function toast(msg, type = "") {
  const el = $("#toast");
  el.textContent = msg;
  el.className = "toast show " + type;
  setTimeout(() => (el.className = "toast"), 3000);
}

async function api(path, opts = {}) {
  const res = await fetch(API + path, opts);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg = (data && data.detail && data.detail.message) || data.message || "İşlem başarısız";
    throw new Error(msg);
  }
  return data;
}

function scoreBadgeClass(score) {
  if (score >= 75) return "score-badge high";
  if (score >= 50) return "score-badge mid";
  return "score-badge low";
}
function diffBadgeClass(d) {
  if (d === "easy") return "diff-easy";
  if (d === "medium") return "diff-medium";
  return "diff-hard";
}
function diffLabel(d) {
  return d === "easy" ? "Kolay" : d === "medium" ? "Orta" : "Zor";
}
function fmtDate(s) {
  if (!s) return "—";
  const d = new Date(s);
  return d.toLocaleString("tr-TR", { day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit" });
}

// ---------- Tab ----------
$$(".tab-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    $$(".tab-btn").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    const tab = btn.dataset.tab;
    $$(".tab-pane").forEach((p) => p.classList.remove("active"));
    $("#tab-" + tab).classList.add("active");
    if (tab === "hub") loadHub();
    if (tab === "analysis") loadMySubmissions();
    if (tab === "sql") loadMyTests();
    if (tab === "admin") loadAdminSubmissions();
  });
});

// ---------- Kullanıcı seçimi ----------
async function loadUsers() {
  try {
    const res = await api("/training/users");
    state.users = res.data || [];
    const sel = $("#userSelect");
    sel.innerHTML = "";
    state.users.forEach((u) => {
      const opt = document.createElement("option");
      opt.value = u.Id;
      opt.textContent = `${u.FullName} (${u.Role})`;
      sel.appendChild(opt);
    });
    // Default: trainee (Eren)
    const eren = state.users.find((u) => u.Role === "trainee") || state.users[0];
    if (eren) {
      sel.value = eren.Id;
      setCurrentUser(eren);
    }
    sel.addEventListener("change", () => {
      const u = state.users.find((x) => String(x.Id) === sel.value);
      if (u) setCurrentUser(u);
    });
  } catch (e) {
    toast("Kullanıcılar yüklenemedi. Veritabanını kontrol et.", "error");
  }
}

function setCurrentUser(user) {
  state.currentUser = user;
  const label = `👤 ${user.FullName}`;
  $("#userTag").textContent = label;
  const headerUser = $("#headerUser");
  if (headerUser) headerUser.textContent = label;
  // Admin tabını sadece admin için göster
  const adminTab = document.querySelector('[data-tab="admin"]');
  adminTab.style.display = user.Role === "admin" ? "" : "none";

  loadHub();
  loadMySubmissions();
  loadMyTests();
}

// ============================================================
// SIDE NAV (sol açılır menü)
// ============================================================
const sideNav = $("#sideNav");
const sideNavOverlay = $("#sideNavOverlay");
function openSideNav() {
  sideNav.classList.add("open");
  sideNavOverlay.classList.add("open");
}
function closeSideNav() {
  sideNav.classList.remove("open");
  sideNavOverlay.classList.remove("open");
}
$("#menuToggle").addEventListener("click", openSideNav);
$("#menuClose").addEventListener("click", closeSideNav);
sideNavOverlay.addEventListener("click", closeSideNav);
// ESC ile kapat
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && sideNav.classList.contains("open")) closeSideNav();
});

// ============================================================
// HUB / ÖZET
// ============================================================
async function loadHub() {
  if (!state.currentUser) return;
  const uid = state.currentUser.Id;
  try {
    const [subRes, testRes] = await Promise.all([
      api(`/training/submissions/user/${uid}`),
      api(`/training/sql-tests/user/${uid}`),
    ]);
    const subs = subRes.data || [];
    const tests = (testRes.data || []).filter((t) => t.Status === "completed");

    $("#statSubmissions").textContent = subs.length;
    $("#statApproved").textContent = subs.filter((s) => s.Status === "approved").length;
    $("#statPending").textContent = subs.filter((s) => s.Status === "pending").length;
    const avg = subs.length ? subs.reduce((a, s) => a + Number(s.TotalScore || 0), 0) / subs.length : 0;
    $("#statAvgScore").textContent = subs.length ? avg.toFixed(1) : "—";

    $("#statTests").textContent = tests.length;
    const sqlAvg = tests.length ? tests.reduce((a, t) => a + Number(t.Score || 0), 0) / tests.length : 0;
    const sqlBest = tests.length ? Math.max(...tests.map((t) => Number(t.Score || 0))) : 0;
    $("#statAvgSqlScore").textContent = tests.length ? sqlAvg.toFixed(1) : "—";
    $("#statBestSqlScore").textContent = tests.length ? sqlBest.toFixed(1) : "—";

    // Son aktivite
    const recent = [
      ...subs.map((s) => ({
        type: "Analiz Dokümanı",
        title: s.RequestTitle,
        score: s.TotalScore,
        date: s.SubmittedAt,
        status: s.Status,
      })),
      ...tests.map((t) => ({
        type: "SQL Testi",
        title: `Test #${t.Id} (${t.TotalQuestions} soru)`,
        score: t.Score,
        date: t.CompletedAt || t.StartedAt,
        status: "completed",
      })),
    ];
    recent.sort((a, b) => new Date(b.date) - new Date(a.date));
    const div = $("#recentActivity");
    if (recent.length === 0) {
      div.innerHTML = '<p class="muted">Henüz aktivite yok. Hadi başlayalım! 🚀</p>';
    } else {
      div.innerHTML = recent
        .slice(0, 10)
        .map(
          (r) => `
        <div class="row">
          <div>
            <strong>${r.type}</strong> — ${r.title}
            <div class="sub-meta" style="font-size:0.78rem;color:#888;">${fmtDate(r.date)}</div>
          </div>
          <span class="${scoreBadgeClass(r.score)}">${Number(r.score).toFixed(1)}</span>
        </div>
      `
        )
        .join("");
    }
  } catch (e) {
    toast(e.message, "error");
  }
}

// ============================================================
// ANALİZ EGZERSİZİ
// ============================================================
$("#getRequestBtn").addEventListener("click", async () => {
  if (!state.currentUser) return;
  try {
    const res = await api(`/training/requests/random?user_id=${state.currentUser.Id}`);
    state.currentRequest = res.data;
    renderCurrentRequest(res.data);
  } catch (e) {
    toast(e.message, "error");
  }
});

function renderCurrentRequest(req) {
  const div = $("#currentRequest");
  div.classList.remove("hidden");
  div.innerHTML = `
    <span class="difficulty ${diffBadgeClass(req.Difficulty)}">${diffLabel(req.Difficulty)}</span>
    <h3>${req.Title}</h3>
    <div class="description">${req.Description}</div>
    <div class="actions">
      <a class="btn-primary" href="/api/training/template?request_id=${req.Id}" target="_blank">
        📥 Şablonu İndir (.docx)
      </a>
      <button class="btn-secondary" id="newReqBtn">🎲 Başka Talep</button>
    </div>
  `;
  $("#uploadArea").classList.remove("hidden");
  $("#evaluationResult").classList.add("hidden");
  $("#newReqBtn").addEventListener("click", () => $("#getRequestBtn").click());
}

$("#uploadBtn").addEventListener("click", async () => {
  if (!state.currentUser || !state.currentRequest) {
    toast("Önce bir talep al.", "error");
    return;
  }
  const fileInput = $("#docFile");
  if (!fileInput.files.length) {
    toast("Bir .docx dosyası seç.", "error");
    return;
  }
  const fd = new FormData();
  fd.append("user_id", state.currentUser.Id);
  fd.append("request_id", state.currentRequest.Id);
  fd.append("file", fileInput.files[0]);
  $("#uploadBtn").disabled = true;
  try {
    const res = await api("/training/submissions", { method: "POST", body: fd });
    renderEvaluation(res.data);
    loadMySubmissions();
    toast("Doküman değerlendirildi!", "success");
    fileInput.value = "";
  } catch (e) {
    toast(e.message, "error");
  } finally {
    $("#uploadBtn").disabled = false;
  }
});

function renderEvaluation(sub) {
  const div = $("#evaluationResult");
  div.classList.remove("hidden");
  div.classList.toggle("failed", sub.TotalScore < 50);
  const detail = sub.EvaluationDetail || {};
  const sections = detail.sections || [];
  const keywords = detail.keywords || [];

  div.innerHTML = `
    <div style="text-align:center;">
      <div class="score-big">${Number(sub.TotalScore).toFixed(1)}</div>
      <div class="muted">Toplam Puan / 100</div>
    </div>

    <div class="score-row">
      <div class="score-item">
        <div class="label">Yapısal</div>
        <div class="value">${Number(sub.StructuralScore).toFixed(1)}</div>
      </div>
      <div class="score-item">
        <div class="label">İçerik</div>
        <div class="value">${Number(sub.ContentScore).toFixed(1)}</div>
      </div>
      <div class="score-item">
        <div class="label">Toplam Kelime</div>
        <div class="value">${detail.total_words || 0}</div>
      </div>
      <div class="score-item">
        <div class="label">Durum</div>
        <div class="value"><span class="status-badge status-${sub.Status}">${sub.Status}</span></div>
      </div>
    </div>

    <h3>Bölüm Detayı</h3>
    <div class="section-detail">
      <div class="sec-row" style="font-weight:700;color:#666;">
        <span>Bölüm</span><span>Kelime</span><span>Durum</span>
      </div>
      ${sections
        .map(
          (s) => `
        <div class="sec-row">
          <span>${s.title}${s.required ? "" : " <small style='color:#aaa'>(opsiyonel)</small>"}</span>
          <span>${s.words} / ${s.min_words}</span>
          <span class="status-${s.status}">${labelForStatus(s.status)}</span>
        </div>
      `
        )
        .join("")}
    </div>

    ${
      keywords.length
        ? `
      <h3>Beklenen Anahtar Kelimeler</h3>
      <div class="kw-list">
        ${keywords.map((k) => `<span class="kw ${k.found ? "found" : "miss"}">${k.found ? "✓" : "✗"} ${k.keyword}</span>`).join("")}
      </div>
    `
        : ""
    }
  `;
}

function labelForStatus(s) {
  return (
    {
      ok: "✓ Yeterli",
      short: "⚠ Kısa",
      very_short: "⚠ Çok kısa",
      placeholder_only: "✗ Placeholder duruyor",
      missing: "✗ Eksik",
    }[s] || s
  );
}

async function loadMySubmissions() {
  if (!state.currentUser) return;
  try {
    const res = await api(`/training/submissions/user/${state.currentUser.Id}`);
    const list = res.data || [];
    const div = $("#mySubmissions");
    if (list.length === 0) {
      div.innerHTML = '<p class="muted">Henüz gönderim yok. İlk talebini al ve başla! 📝</p>';
      return;
    }
    div.innerHTML = list
      .map(
        (s) => `
      <div class="sub-row">
        <div>
          <div class="title">${s.RequestTitle}</div>
          <div class="sub-meta">${fmtDate(s.SubmittedAt)} • ${s.FileName}</div>
        </div>
        <span class="status-badge status-${s.Status}">${s.Status}</span>
        <span class="${scoreBadgeClass(s.TotalScore)}">${Number(s.TotalScore).toFixed(1)}</span>
        <button class="btn-secondary" onclick="showSubmissionDetail(${s.Id})">Detay</button>
        <a class="btn-secondary" href="/api/training/submissions/${s.Id}/download" target="_blank">İndir</a>
      </div>
    `
      )
      .join("");
  } catch (e) {
    toast(e.message, "error");
  }
}

window.showSubmissionDetail = async function (id) {
  try {
    const res = await api(`/training/submissions/${id}`);
    const sub = res.data;
    const detail = sub.EvaluationDetail || {};
    const sections = detail.sections || [];
    const keywords = detail.keywords || [];

    $("#detailContent").innerHTML = `
      <h2>${sub.RequestTitle}</h2>
      <p class="muted">Gönderim #${sub.Id} • ${fmtDate(sub.SubmittedAt)} • ${sub.UserName}</p>
      <div class="score-row" style="margin: 14px 0;">
        <div class="score-item">
          <div class="label">Yapısal</div>
          <div class="value">${Number(sub.StructuralScore).toFixed(1)}</div>
        </div>
        <div class="score-item">
          <div class="label">İçerik</div>
          <div class="value">${Number(sub.ContentScore).toFixed(1)}</div>
        </div>
        <div class="score-item">
          <div class="label">Toplam</div>
          <div class="value">${Number(sub.TotalScore).toFixed(1)}</div>
        </div>
        <div class="score-item">
          <div class="label">Durum</div>
          <div class="value"><span class="status-badge status-${sub.Status}">${sub.Status}</span></div>
        </div>
      </div>

      ${
        sub.ReviewNote
          ? `<div class="eval-result"><strong>Yönetici Notu:</strong> ${sub.ReviewNote}</div>`
          : ""
      }

      <h3>Bölüm Detayı</h3>
      <div class="section-detail">
        ${sections
          .map(
            (s) => `
          <div class="sec-row">
            <span>${s.title}</span>
            <span>${s.words} / ${s.min_words}</span>
            <span class="status-${s.status}">${labelForStatus(s.status)}</span>
          </div>
        `
          )
          .join("")}
      </div>

      ${
        keywords.length
          ? `
        <h3>Anahtar Kelimeler</h3>
        <div class="kw-list">
          ${keywords.map((k) => `<span class="kw ${k.found ? "found" : "miss"}">${k.found ? "✓" : "✗"} ${k.keyword}</span>`).join("")}
        </div>`
          : ""
      }

      <p style="margin-top:18px;">
        <a class="btn-primary" href="/api/training/submissions/${sub.Id}/download" target="_blank">📥 Word Dosyasını İndir</a>
      </p>
    `;
    $("#detailOverlay").classList.add("active");
  } catch (e) {
    toast(e.message, "error");
  }
};

$("#closeDetailBtn").addEventListener("click", () => $("#detailOverlay").classList.remove("active"));
$("#detailOverlay").addEventListener("click", (e) => {
  if (e.target.id === "detailOverlay") $("#detailOverlay").classList.remove("active");
});

// ============================================================
// SQL TESTİ
// ============================================================
$("#startTestBtn").addEventListener("click", async () => {
  if (!state.currentUser) return;
  const easy = parseInt($("#cfgEasy").value || 0);
  const medium = parseInt($("#cfgMedium").value || 0);
  const hard = parseInt($("#cfgHard").value || 0);
  if (easy + medium + hard === 0) {
    toast("En az bir soru seç.", "error");
    return;
  }
  try {
    const res = await api("/training/sql-tests/start", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: state.currentUser.Id,
        easy_count: easy,
        medium_count: medium,
        hard_count: hard,
      }),
    });
    state.currentTest = res.data;
    showTest(res.data);
  } catch (e) {
    toast(e.message, "error");
  }
});

function showTest(test) {
  $("#sqlStartPanel").classList.add("hidden");
  $("#sqlResultPanel").classList.add("hidden");
  $("#sqlTestPanel").classList.remove("hidden");
  $("#testTitle").textContent = `Test #${test.Id}`;
  $("#testProgress").textContent = `${test.TotalQuestions} soru • ${test.TotalPoints} puan`;

  const div = $("#testQuestions");
  div.innerHTML = test.Questions.map((q, i) => renderQuestion(q, i + 1)).join("");

  // Cevap dinleyicileri
  test.Questions.forEach((q) => {
    if (q.QuestionType === "multiple_choice") {
      $$(`input[name="q-${q.TestQuestionId}"]`).forEach((inp) => {
        inp.addEventListener("change", () => submitAnswer(q.TestQuestionId, inp.value));
      });
    } else {
      const inp = document.getElementById(`q-${q.TestQuestionId}`);
      if (inp) {
        let timer;
        inp.addEventListener("input", () => {
          clearTimeout(timer);
          timer = setTimeout(() => submitAnswer(q.TestQuestionId, inp.value), 600);
        });
      }
    }
  });
}

function renderQuestion(q, order) {
  let input = "";
  if (q.QuestionType === "multiple_choice") {
    let opts = [];
    try { opts = JSON.parse(q.OptionsJson || "[]"); } catch {}
    input = `<div class="options">
      ${opts
        .map(
          (o, i) => `<label>
            <input type="radio" name="q-${q.TestQuestionId}" value="${i}" />
            <strong>${String.fromCharCode(65 + i)})</strong> ${escapeHtml(o)}
          </label>`
        )
        .join("")}
    </div>`;
  } else if (q.QuestionType === "fill_in_blank") {
    input = `<input type="text" id="q-${q.TestQuestionId}" placeholder="Cevabını yaz..." />`;
  } else {
    input = `<textarea id="q-${q.TestQuestionId}" placeholder="SQL kodunu yaz..."></textarea>`;
  }
  return `
    <div class="question-card" id="qc-${q.TestQuestionId}">
      <span class="q-num">${order}</span>
      <strong>${q.Points} puan</strong>
      <span class="q-diff ${diffBadgeClass(q.Difficulty)}">${diffLabel(q.Difficulty)}</span>
      <span style="color:#aaa; font-size:0.78rem; margin-left:8px;">${qTypeLabel(q.QuestionType)}</span>
      <div class="q-text">${escapeHtml(q.QuestionText)}</div>
      ${input}
      <div class="q-feedback hidden" id="fb-${q.TestQuestionId}"></div>
    </div>
  `;
}

function qTypeLabel(t) {
  return { multiple_choice: "Çoktan seçmeli", fill_in_blank: "Boşluk doldurma", short_code: "SQL yaz" }[t] || t;
}

function escapeHtml(s) {
  return String(s || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

async function submitAnswer(testQuestionId, answer) {
  try {
    await api("/training/sql-tests/answer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ test_question_id: testQuestionId, user_answer: answer }),
    });
    // Otomatik feedback göstermiyoruz; test tamamlanınca gösterilecek
  } catch (e) {
    toast(e.message, "error");
  }
}

$("#completeTestBtn").addEventListener("click", async () => {
  if (!state.currentTest) return;
  try {
    const res = await api(`/training/sql-tests/${state.currentTest.Id}/complete`, { method: "POST" });
    showTestResult(res.data);
    loadMyTests();
    loadHub();
  } catch (e) {
    toast(e.message, "error");
  }
});

function showTestResult(test) {
  $("#sqlTestPanel").classList.add("hidden");
  $("#sqlResultPanel").classList.remove("hidden");
  const div = $("#testResult");
  div.innerHTML = `
    <div style="text-align:center;">
      <div class="score-big">${Number(test.Score).toFixed(1)}</div>
      <div class="muted">${test.CorrectCount} / ${test.TotalQuestions} doğru • ${test.EarnedPoints} / ${test.TotalPoints} puan</div>
    </div>

    <h3 style="margin-top:24px;">Soru Bazlı Sonuç</h3>
    ${test.Questions.map((q, i) => renderResultQuestion(q, i + 1)).join("")}
  `;
}

function renderResultQuestion(q, order) {
  const correctSign = q.IsCorrect ? "✓" : "✗";
  const cls = q.IsCorrect ? "correct" : "wrong";
  let opts = [];
  try { opts = JSON.parse(q.OptionsJson || "[]"); } catch {}

  // Kullanıcının cevabını oku
  let userAnsDisplay = q.UserAnswer || "<em>(cevapsız)</em>";
  if (q.QuestionType === "multiple_choice" && opts.length) {
    const idx = parseInt(q.UserAnswer);
    userAnsDisplay = (!isNaN(idx) && opts[idx])
      ? `${String.fromCharCode(65 + idx)}) ${escapeHtml(opts[idx])}`
      : (q.UserAnswer ? escapeHtml(q.UserAnswer) : "<em>(cevapsız)</em>");
  } else {
    userAnsDisplay = q.UserAnswer ? escapeHtml(q.UserAnswer) : "<em>(cevapsız)</em>";
  }

  // Doğru cevabı oku
  let correctAnsDisplay = "—";
  if (q.CorrectAnswer != null) {
    if (q.QuestionType === "multiple_choice" && opts.length) {
      const cidx = parseInt(q.CorrectAnswer);
      correctAnsDisplay = (!isNaN(cidx) && opts[cidx])
        ? `${String.fromCharCode(65 + cidx)}) ${escapeHtml(opts[cidx])}`
        : escapeHtml(String(q.CorrectAnswer));
    } else {
      correctAnsDisplay = escapeHtml(String(q.CorrectAnswer));
    }
  }

  return `
    <div class="question-card">
      <span class="q-num">${order}</span>
      <span class="q-diff ${diffBadgeClass(q.Difficulty)}">${diffLabel(q.Difficulty)}</span>
      <span class="${cls === "correct" ? "status-ok" : "status-missing"}" style="margin-left:8px;">${correctSign} ${q.PointsEarned}/${q.Points} puan</span>
      <div class="q-text">${escapeHtml(q.QuestionText)}</div>
      <div class="q-feedback ${cls}">
        <div><strong>Senin cevabın:</strong> ${userAnsDisplay}</div>
        ${!q.IsCorrect ? `<div style="margin-top:6px;"><strong>✓ Doğru cevap:</strong> <code class="answer-code">${correctAnsDisplay}</code></div>` : ""}
        ${q.Explanation ? `<div style="margin-top:8px;"><strong>💡 Açıklama:</strong> ${escapeHtml(q.Explanation)}</div>` : ""}
      </div>
    </div>
  `;
}

$("#backToStartBtn").addEventListener("click", () => {
  $("#sqlResultPanel").classList.add("hidden");
  $("#sqlStartPanel").classList.remove("hidden");
  state.currentTest = null;
});

async function loadMyTests() {
  if (!state.currentUser) return;
  try {
    const res = await api(`/training/sql-tests/user/${state.currentUser.Id}`);
    const tests = res.data || [];
    const div = $("#myTests");
    if (!tests.length) {
      div.innerHTML = '<p class="muted">Henüz test yok. Yeni test başlat ve dene! 💪</p>';
      return;
    }
    div.innerHTML = tests.map((t) => `
      <div class="sub-row">
        <div>
          <div class="title">Test #${t.Id}</div>
          <div class="sub-meta">${fmtDate(t.StartedAt)} • ${t.TotalQuestions} soru</div>
        </div>
        <span class="status-badge status-${t.Status === "completed" ? "approved" : "pending"}">${t.Status === "completed" ? "tamamlandı" : "devam ediyor"}</span>
        <span class="${scoreBadgeClass(t.Score)}">${Number(t.Score).toFixed(1)}</span>
        <button class="btn-secondary" onclick="showTestDetail(${t.Id})">Detay</button>
        <span></span>
      </div>
    `).join("");
  } catch (e) {
    toast(e.message, "error");
  }
}

window.showTestDetail = async function (id) {
  console.log("[showTestDetail] called with id:", id);
  try {
    const res = await api(`/training/sql-tests/${id}`);
    const test = res.data;
    console.log("[showTestDetail] got test:", test);

    if (test.Status !== "completed") {
      state.currentTest = test;
      showTest(test);
      $$(".tab-btn").forEach((b) => b.classList.remove("active"));
      document.querySelector('[data-tab="sql"]').classList.add("active");
      $$(".tab-pane").forEach((p) => p.classList.remove("active"));
      $("#tab-sql").classList.add("active");
      return;
    }

    // Soru kartlarını ayrı render et — hatayı izole etmek için
    let questionsHtml = "";
    try {
      questionsHtml = test.Questions.map((q, i) => renderResultQuestion(q, i + 1)).join("");
    } catch (renderErr) {
      console.error("[showTestDetail] renderResultQuestion error:", renderErr);
      questionsHtml = `<div class="q-feedback wrong">Sorular render edilemedi: ${escapeHtml(renderErr.message)}</div>`;
    }

    $("#detailContent").innerHTML = `
      <h2>SQL Test #${test.Id} — ${escapeHtml(test.UserName || "")}</h2>
      <p class="muted">${fmtDate(test.StartedAt)} - ${fmtDate(test.CompletedAt)}</p>
      <div class="score-row">
        <div class="score-item"><div class="label">Skor</div><div class="value">${Number(test.Score || 0).toFixed(1)}</div></div>
        <div class="score-item"><div class="label">Doğru</div><div class="value">${test.CorrectCount || 0}/${test.TotalQuestions || 0}</div></div>
        <div class="score-item"><div class="label">Puan</div><div class="value">${test.EarnedPoints || 0}/${test.TotalPoints || 0}</div></div>
      </div>
      ${questionsHtml}
    `;
    $("#detailOverlay").classList.add("active");
    console.log("[showTestDetail] modal opened");
  } catch (e) {
    console.error("[showTestDetail] error:", e);
    toast("Detay açılamadı: " + e.message, "error");
  }
};

// ============================================================
// ADMIN PANELİ
// ============================================================
let adminFilter = "pending";
$$(".filter-btn").forEach((b) => {
  b.addEventListener("click", () => {
    $$(".filter-btn").forEach((x) => x.classList.remove("active"));
    b.classList.add("active");
    adminFilter = b.dataset.filter;
    loadAdminSubmissions();
  });
});

async function loadAdminSubmissions() {
  if (!state.currentUser || state.currentUser.Role !== "admin") return;
  try {
    const path = adminFilter ? `/training/submissions?status=${adminFilter}` : "/training/submissions";
    const res = await api(path);
    const list = res.data || [];
    const div = $("#adminSubmissions");
    if (!list.length) {
      div.innerHTML = '<p class="muted">Bu filtrede gönderim yok.</p>';
      return;
    }
    div.innerHTML = list
      .map(
        (s) => `
      <div class="sub-row">
        <div>
          <div class="title">${s.RequestTitle}</div>
          <div class="sub-meta">${s.UserName} • ${fmtDate(s.SubmittedAt)} • ${s.FileName}</div>
        </div>
        <span class="status-badge status-${s.Status}">${s.Status}</span>
        <span class="${scoreBadgeClass(s.TotalScore)}">${Number(s.TotalScore).toFixed(1)}</span>
        <button class="btn-secondary" onclick="showSubmissionDetail(${s.Id})">Detay</button>
        ${
          s.Status === "pending"
            ? `<span>
                <button class="btn-success" onclick="reviewSub(${s.Id}, 'approved')">✓ Onayla</button>
                <button class="btn-danger" onclick="reviewSub(${s.Id}, 'rejected')">✗ Reddet</button>
              </span>`
            : "<span></span>"
        }
      </div>
    `
      )
      .join("");
  } catch (e) {
    toast(e.message, "error");
  }
}

window.reviewSub = async function (id, status) {
  const note = prompt(status === "approved" ? "İsteğe bağlı not:" : "Red sebebini yaz:") || "";
  try {
    await api(`/training/submissions/${id}/review`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status, review_note: note }),
    });
    toast("İnceleme kaydedildi.", "success");
    loadAdminSubmissions();
  } catch (e) {
    toast(e.message, "error");
  }
};

// ============================================================
// BAŞLANGIÇ
// ============================================================
loadUsers();

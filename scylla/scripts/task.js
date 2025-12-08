import { showToast } from "./utils/notification.js";

const API_STATUS_URL = "http://localhost:8000/api/schedule/status";
const API_LIST_URL   = "http://localhost:8000/api";
const LS_KEY         = "scheduled_task_ids";

const statusMap = {
  running:   { text: "Running",   dot: "blue"  },
  rejected:  { text: "Rejected",  dot: "gray"  },
  pending:   { text: "Pending",   dot: "blue"  },
  completed: { text: "Completed", dot: "green" },
  scheduled: { text: "Scheduled", dot: "yellow"},
  canceled:  { text: "Canceled",  dot: "orange"},
  error:     { text: "Error",     dot: "red"   },
};

function esc(s) {
  return String(s).replace(/[&<>"']/g, m => (
    { "&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;" }[m]
  ));
}
function normalizeStatus(s) {
  return String(s ?? "").trim().toLowerCase().replace(/\s+/g, " ");
}

function getSavedTasks() {
  try {
    const raw = JSON.parse(localStorage.getItem(LS_KEY) || "[]");
    if (!Array.isArray(raw)) return [];
    if (!raw.length) return [];

    if (typeof raw[0] === "string") {
      return raw.map(task_id => ({ task_id, approach: null, savedAt: Date.now() }));
    }
    return raw.map(it => ({
      task_id: it.task_id,
      approach: it.approach ?? null,
      savedAt: it.savedAt ?? Date.now(),
    }));
  } catch {
    return [];
  }
}

function getApproachForTask(taskId) {
  const list = getSavedTasks();
  const item = list.find(x => x.task_id === taskId);
  return item?.approach;
}

function getSavedTaskIdsSorted() {
  return getSavedTasks()
    .sort((a,b) => (b.savedAt || 0) - (a.savedAt || 0))
    .map(x => x.task_id)
    .filter(Boolean);
}

async function fetchTaskStatusGET(taskId) {
  const url = new URL(API_STATUS_URL);
  url.searchParams.set("task_id", taskId);
  const res = await fetch(url.toString(), {
    method: "GET",
    headers: { Accept: "application/json" },
    cache: "no-cache",
  });
  if (!res.ok) {
    let err; try { err = await res.json(); } catch { err = await res.text(); }
    throw new Error(`HTTP ${res.status}`);
  }

  const data = await res.json();
  return Array.isArray(data) ? data[0] : data;
}

function buildCodesUrl(taskId, taskType) {
  const tt = (taskType ?? "").toString().trim().toLowerCase();
  if (!tt) throw new Error(`Não foi possível determinar o tipo (approach/task_type) para task_id=${taskId}.`);
  const u = new URL(`${API_LIST_URL}/${encodeURIComponent(tt)}/codes`);
  u.searchParams.set("task_id", taskId);
  return u.toString();
}


function rowTemplate(item) {
  const s = statusMap[item.status] || { text: esc(item.status), dot: "gray" };
  const isCompleted = item.status === "completed";
  const hasType = Boolean(item.type);
  const rowClass = isCompleted ? " row-muted" : "";

  const actions = (isCompleted && hasType)
    ? `<button class="icon-btn download-btn" data-task-id="${esc(item.id)}" data-task-type="${esc(item.type)}" title="Download CSV">
         <i class="fas fa-download"></i>
       </button>`
    : `<button class="icon-btn" disabled title="${hasType ? 'No file' : 'without (approach)'}">
         <i class="fas fa-download"></i>
       </button>`;

  return `
  <tr class="${rowClass}">
    <td>
      <div class="cell-id">
      <!---
          <label class="checkbox">
              <input type="checkbox" />
               <span class="checkmark"></span>
            </label>  
        ---!>
        <span class="file-badge csv">CSV</span>
        <span class="id-text">${esc(item.id)}</span>
      </div>
    </td>
    <td>${esc((item.type || "").toUpperCase() || "—")}</td>
    <td><span class="status"><i class="dot ${s.dot}"></i>${s.text}</span></td>
    <td class="actions">${actions}</td>
  </tr>`;
}

function toRowItem(api) {
  const statusNorm = normalizeStatus(api.status);
  const id         = api.task_id ?? api.taskId ?? api.id;
  const fallback   = getApproachForTask(id);
  const taskType   = String(api.task_type).toLowerCase();

  return { id, type: taskType, status: statusNorm };
}

function flattenObject(obj, prefix = "", out = {}) {
  if (obj && typeof obj === "object" && !Array.isArray(obj)) {
    for (const [k, v] of Object.entries(obj)) {
      flattenObject(v, prefix ? `${prefix}.${k}` : k, out);
    }
  } else {
    out[prefix] = obj;
  }
  return out;
}

function objectsToCsv(rows) {
  if (!rows?.length) return "";
  const flat = rows.map(r => flattenObject(r));
  const headers = Array.from(flat.reduce((set, r) => {
    Object.keys(r).forEach(k => set.add(k));
    return set;
  }, new Set()));
  const escapeCsv = (v) => {
    const s = v == null ? "" : String(v);
    return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
    };
  const headerLine = headers.map(escapeCsv).join(",");
  const lines = flat.map(r => headers.map(h => escapeCsv(r[h])).join(","));
  return [headerLine, ...lines].join("\n");
}

async function handleDownloadCsv(taskId, taskType) {
  try {
    const url = buildCodesUrl(taskId, taskType);
    const res = await fetch(url, { method: "GET", headers: { Accept: "application/json" }});
    if (!res.ok) {
      let err; try { err = await res.json(); } catch { err = await res.text(); }

      showToast("error", "Error", "Fail to obtain data for CSV.");
      return;
    }
    const data = await res.json();
    const csv  = objectsToCsv(Array.isArray(data) ? data : [data]);
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `codes_${taskType || 'unknown'}_${taskId}.csv`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(a.href);
  } catch (e) {
    showToast("error", "Error", "Generate CSV");
  }
}

async function loadTasks() {
  const tbody = document.getElementById("tasks-tbody");
  tbody.innerHTML = `<tr><td colspan="4" style="padding:20px;color:#94a3b8">Loading…</td></tr>`;

  const ids = getSavedTaskIdsSorted();
  if (!ids.length) {
    tbody.innerHTML = `<tr><td colspan="4" style="padding:20px;color:#94a3b8">No tasks available</td></tr>`;
    return;
  }

  try {
    const results = await Promise.allSettled(ids.map(id => fetchTaskStatusGET(id)));
    const okItems = results
      .filter(r => r.status === "fulfilled" && r.value && (r.value.task_id || r.value.taskId || r.value.id))
      .map(r => toRowItem(r.value));

    tbody.innerHTML = okItems.length
      ? okItems.map(rowTemplate).join("")
      : `<tr><td colspan="4" style="padding:20px;color:#94a3b8">Tasks not found</td></tr>`;

    tbody.querySelectorAll(".download-btn").forEach(btn => {
      btn.addEventListener("click", async (e) => {
        const taskId   = e.currentTarget.getAttribute("data-task-id");
        const taskType = e.currentTarget.getAttribute("data-task-type");
        await handleDownloadCsv(taskId, taskType);
      });
    });
  } catch (e) {
    tbody.innerHTML = `<tr><td colspan="4" style="padding:20px;color:#64748b">Tasks not found</td></tr>`;
  }
}

document.addEventListener("DOMContentLoaded", loadTasks);
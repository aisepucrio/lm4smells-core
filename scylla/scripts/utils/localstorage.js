const LS_KEY = "scheduled_task_ids";

export function getSavedTasks() {
  try {
    const raw = JSON.parse(localStorage.getItem(LS_KEY) || "[]");
    if (!Array.isArray(raw)) return [];
    if (!raw.length) return [];

    if (typeof raw[0] === "string")
      return raw.map(task_id => ({ task_id, approach: null, savedAt: Date.now() }));

    return raw.map(it => ({
      task_id: it.task_id,
      approach: it.approach,
      savedAt: it.savedAt ?? Date.now(),
    }));
  } catch {
    return [];
  }
}

function setSavedTasks(list) {
  localStorage.setItem(LS_KEY, JSON.stringify(list));
}

export function saveTaskId(task_id, approach, when = Date.now()) {
  const list = getSavedTasks();
  const i = list.findIndex(x => x.task_id === task_id);
  if (i >= 0) {
    list[i].savedAt = when;
    list[i].approach = approach ?? list[i].approach;
  } else {
    list.push({ task_id, approach: approach ?? null, savedAt: when });
  }
  setSavedTasks(list);
}

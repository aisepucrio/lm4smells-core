import { showToast } from "./notification.js";

/**
 * @param {Object} cfg
 * @param {string} cfg.endpoint                 
 * @param {string} cfg.dropZoneId               
 * @param {string} cfg.fileInputId              
 * @param {string} cfg.fileListContainerId      
 * @param {string} cfg.fileListId               
 * @param {string} cfg.fileCountId              
 * @param {string} cfg.submitButtonId          
 * @param {Array<{id:string, name:string}>} cfg.fields
 * @param {(result:any)=>void} [cfg.onSuccess] 
 * @param {(err:any)=>void}   [cfg.onError]    
 * @param {(fd:FormData)=>void} [cfg.beforeSend]
 */
export function createUploader(cfg) {

  const dropZone          = byId(cfg.dropZoneId);
  const fileInput         = byId(cfg.fileInputId);
  const fileListContainer = byId(cfg.fileListContainerId);
  const fileList          = byId(cfg.fileListId);
  const fileCount         = byId(cfg.fileCountId);
  const submitButton      = byId(cfg.submitButtonId);

  const fieldEls = (cfg.fields || []).map(f => ({
    ...f,
    el: byId(f.id)
  }));

  let files = [];
  let submitting = false;

  // ---- Wiring
  dropZone.addEventListener("dragover", e => { e.preventDefault(); dropZone.classList.add("dragging"); });
  dropZone.addEventListener("dragleave", e => { e.preventDefault(); dropZone.classList.remove("dragging"); });
  dropZone.addEventListener("drop", e => {
    e.preventDefault(); dropZone.classList.remove("dragging");
    if (e.dataTransfer.files?.length) { setFiles(Array.from(e.dataTransfer.files)); e.dataTransfer.clearData(); }
  });
  dropZone.addEventListener("click", () => fileInput.click());
  fileInput.addEventListener("change", e => {
    if (e.target.files?.length) setFiles(Array.from(e.target.files));
  });
  submitButton.addEventListener("click", handleSubmit);

  function byId(id) {
    const el = document.getElementById(id);
    if (!el) throw new Error(`Element not found: #${id}`);
    return el;
  }

  function setFiles(newFiles) {
    files = newFiles;
    renderFiles();
    showToast("success", "Files Added", `${files.length} file(s) ready to upload.`);
  }

  function renderFiles() {
    if (files.length) {
      fileListContainer.classList.remove("hidden");
      fileCount.textContent = String(files.length);
      fileList.innerHTML = "";
      files.forEach((file, idx) => {
        const div = document.createElement("div");
        div.className = "file-item";
        const sizeKB = (file.size / 1024).toFixed(1);
        div.innerHTML = `
          <div class="file-info">
            <i class="fas fa-file-alt file-icon"></i>
            <span class="file-name">${file.name}</span>
            <span class="file-size">(${sizeKB} KB)</span>
          </div>
          <button type="button" class="remove-file" data-index="${idx}">
            <i class="fas fa-times"></i>
          </button>`;
        fileList.appendChild(div);
      });
      fileList.querySelectorAll(".remove-file").forEach(btn => {
        btn.addEventListener("click", function () {
          const i = Number(this.getAttribute("data-index"));
          files.splice(i, 1);
          renderFiles();
          if (!files.length) fileInput.value = "";
        });
      });
    } else {
      fileListContainer.classList.add("hidden");
      fileList.innerHTML = "";
      fileCount.textContent = "0";
    }
  }

  function setSubmitting(v) {
    submitting = v;
    if (v) {
      submitButton.disabled = true;
      submitButton.innerHTML = `<i class="fas fa-spinner spinner icon-button"></i> Processing...`;
    } else {
      submitButton.disabled = false;
      submitButton.innerHTML = `<i class="fas fa-check icon-button"></i> Submit Request`;
    }
  }

  function validate() {
    for (const f of fieldEls) {
      if (!f.el?.value) return `Please fill the field: ${f.id}`;
    }
    if (files.length === 0) return "Please upload at least one file.";
    return null;
  }

  async function handleSubmit() {
    const err = validate();
    if (err) { showToast("error", "Validation Error", err); return; }

    setSubmitting(true);
    try {
      const fd = new FormData();
      files.forEach(file => fd.append("files", file));

      fieldEls.forEach(f => {
        if (f.el.type === "checkbox") {
          fd.append(f.name, f.el.checked ? "true" : "false");
        } else {
          fd.append(f.name, f.el.value);
        }
      });

      if (typeof cfg.beforeSend === "function") cfg.beforeSend(fd);

      const resp = await fetch(cfg.endpoint, { method: "POST", body: fd });
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const result = await resp.json();

      if (typeof cfg.onSuccess === "function") cfg.onSuccess(result);
      showToast("success", "Success", "Your request has been processed successfully.");
    } catch (e) {
      if (typeof cfg.onError === "function") cfg.onError(e);
      console.error(e);
      showToast("error", "Error", "There was an error sending your files");
    } finally {
      setSubmitting(false);
    }
  }

  return {
    setFiles,
    submit: handleSubmit
  };
}

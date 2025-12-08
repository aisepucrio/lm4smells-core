import { createUploader } from "./utils/uploader.js";
import { saveTaskId } from "./utils/localstorage.js";

document.addEventListener("DOMContentLoaded", () => {
  createUploader({
    endpoint: "http://localhost:8000/api/schedule/ml",
    dropZoneId: "drop-zone",
    fileInputId: "file-upload",
    fileListContainerId: "file-list-container",
    fileListId: "file-list",
    fileCountId: "file-count",
    submitButtonId: "submit-button",
    fields: [
      { id: "extract-type",  name: "extract_type" },
      { id: "analyse-type",  name: "analyse_type" },
      { id: "ml_model",      name: "ml_model" },
    ],
    onSuccess: (result) => {
      if (result?.task_id) saveTaskId(result.task_id, result.approach);
    }
  });
});
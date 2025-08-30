document.addEventListener('DOMContentLoaded', function() {
  // Elements
  const dropZone = document.getElementById('drop-zone');
  const fileInput = document.getElementById('file-upload');
  const fileListContainer = document.getElementById('file-list-container');
  const fileList = document.getElementById('file-list');
  const fileCount = document.getElementById('file-count');
  const submitButton = document.getElementById('submit-button');
  const toastContainer = document.getElementById('toast-container');
  
  // Form elements
  const extractTypeSelect = document.getElementById('extract-type');
  const analyseTypeSelect = document.getElementById('analyse-type');
  const modelSelect = document.getElementById('model');
  const promptTypeSelect = document.getElementById('prompt-type');
  const promptTextarea = document.getElementById('prompt');
  const compositePromptCheckbox = document.getElementById('composite-prompt');
  
  // State
  let files = [];
  let isSubmitting = false;
  
  // Event Listeners
  dropZone.addEventListener('dragover', handleDragOver);
  dropZone.addEventListener('dragleave', handleDragLeave);
  dropZone.addEventListener('drop', handleDrop);
  dropZone.addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', handleFileChange);
  submitButton.addEventListener('click', handleSubmit);
  
  // Drag and Drop Handlers
  function handleDragOver(e) {
    e.preventDefault();
    dropZone.classList.add('dragging');
  }
  
  function handleDragLeave(e) {
    e.preventDefault();
    dropZone.classList.remove('dragging');
  }
  
  function handleDrop(e) {
    e.preventDefault();
    dropZone.classList.remove('dragging');
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFiles(Array.from(e.dataTransfer.files));
    }
  }
  
  function handleFileChange(e) {
    if (e.target.files && e.target.files.length > 0) {
      handleFiles(Array.from(e.target.files));
    }
  }
  
  function handleFiles(newFiles) {
    files = newFiles;
    updateFileList();
    showToast('success', 'Arquivos adicionados', `${files.length} arquivo(s) pronto(s) para upload.`);
  }
  
  function updateFileList() {
    if (files.length > 0) {
      fileListContainer.classList.remove('hidden');
      fileCount.textContent = files.length;
      fileList.innerHTML = '';
      
      files.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        
        const fileSize = (file.size / 1024).toFixed(1);
        
        fileItem.innerHTML = `
          <div class="file-info">
            <i class="fas fa-file-alt file-icon"></i>
            <span class="file-name">${file.name}</span>
            <span class="file-size">(${fileSize} KB)</span>
          </div>
          <button type="button" class="remove-file" data-index="${index}">
            <i class="fas fa-times"></i>
          </button>
        `;
        
        fileList.appendChild(fileItem);
      });
      
      // Add event listeners to remove buttons
      document.querySelectorAll('.remove-file').forEach(button => {
        button.addEventListener('click', function() {
          const index = parseInt(this.getAttribute('data-index'));
          removeFile(index);
        });
      });
    } else {
      fileListContainer.classList.add('hidden');
    }
  }
  
  function removeFile(index) {
    files.splice(index, 1);
    updateFileList();
  }
  
  // Form Submission
  async function handleSubmit() {
    // Validate form
    if (!extractTypeSelect.value || !analyseTypeSelect.value || !modelSelect.value || 
        !promptTypeSelect.value || !promptTextarea.value) {
      showToast('error', 'Erro de Validação', 'Por favor, preencha todos os campos obrigatórios.');
      return;
    }
    
    if (files.length === 0) {
      showToast('error', 'Erro de Validação', 'Por favor, faça upload de pelo menos um arquivo.');
      return;
    }
    
    setSubmitting(true);
    
    try {
      const formData = new FormData();
      
      // Append files
      files.forEach(file => {
        formData.append('files', file);
      });
      
      // Append form data
      formData.append('extract_type', extractTypeSelect.value);
      formData.append('analyse_type', analyseTypeSelect.value);
      formData.append('model', modelSelect.value);
      formData.append('prompt_type', promptTypeSelect.value);
      formData.append('prompt', promptTextarea.value);
      formData.append('is_composite_prompt', compositePromptCheckbox.checked.toString());
      
      
      // Send POST request
      const response = await fetch('http://localhost:8000/', {
        method: 'POST',
        body: formData
      });
      
      if (!response.ok) {
        throw new Error(`O servidor respondeu com status: ${response.status}`);
      }
      
      const result = await response.json();
      
      showToast('success', 'Sucesso', 'Sua requisição foi processada com sucesso.');
      console.log('Resposta do servidor:', result);
    } catch (error) {
      console.error('Erro ao enviar formulário:', error);
      showToast('error', 'Erro', error.message || 'Falha ao enviar o formulário.');
    } finally {
      setSubmitting(false);
    }
  }
  
  function setSubmitting(submitting) {
    isSubmitting = submitting;
    
    if (isSubmitting) {
      submitButton.disabled = true;
      submitButton.innerHTML = `
        <i class="fas fa-spinner spinner icon-button"></i>
        Processando...
      `;
    } else {
      submitButton.disabled = false;
      submitButton.innerHTML = `
        <i class="fas fa-check icon-button"></i>
        Enviar Requisição
      `;
    }
  }
  
  // Toast Notifications
  function showToast(type, title, description) {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const icon = type === 'success' ? 'check-circle' : 'exclamation-circle';
    
    toast.innerHTML = `
      <i class="fas fa-${icon} toast-icon"></i>
      <div class="toast-content">
        <div class="toast-title">${title}</div>
        <div class="toast-description">${description}</div>
      </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
      toast.style.animation = 'fadeOut 0.5s forwards';
      setTimeout(() => {
        toastContainer.removeChild(toast);
      }, 500);
    }, 5000);
  }
});
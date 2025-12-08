document.addEventListener('DOMContentLoaded', () => {
  const classSel   = document.getElementById('extract-type');
  const analyseSel = document.getElementById('analyse-type');
  const modelSel   = document.getElementById('ml_model');

  const ALL_MODELS = [
    { value: 'LGBM', label: 'LGBM' },
    { value: 'KNN', label: 'KNN' },
    { value: 'LDA', label: 'LDA' },
    { value: 'RIDGE', label: 'RIDGE' },
    { value: 'SGD', label: 'SGD' },
    { value: 'GAUSSIAN', label: 'GAUSSIAN' },
    { value: 'QDA', label: 'QDA' },
    { value: 'IR', label: 'IR' },
  ];


  const MODELS_BY_SMELL = {
    'long-method':         ['LGBM', 'KNN', 'LDA', 'RIDGE', 'SGD'],
    'long-parameter-list': ['KNN', 'SGD', 'GAUSSIAN', 'LGBM', 'QDA'],
    'large-class':         ['LGBM', 'KNN', 'LDA', 'RIDGE', 'IR'],
  };

  // 1 = Class, 2 = Method
  const SMELLS_BY_EXTRACT = {
    '1': ['large-class'],                           // Classe
    '2': ['long-method', 'long-parameter-list'],    // Método
  };

  const SMELL_LABELS = {
    'long-method': 'Long Method',
    'long-parameter-list': 'Long Parameter List',
    'large-class': 'Large Class',
  };

  function fillSelect(selectEl, options, placeholderText = 'Select an option') {
    const prev = selectEl.value;
    selectEl.innerHTML = '';
    selectEl.append(new Option(placeholderText, '', true, false));
    options.forEach(opt => selectEl.append(new Option(opt.label, opt.value)));
    const hasPrev = options.some(o => o.value === prev);
    selectEl.value = hasPrev ? prev : '';
  }

  function fillModelOptions(allowedValues) {
    const opts = ALL_MODELS.filter(m => allowedValues.includes(m.value));
    fillSelect(modelSel, opts, 'Select model');
    modelSel.disabled = opts.length === 0;
  }

  function resetAnalyse() {
    analyseSel.innerHTML = '';
    analyseSel.append(new Option('Select smell type', '', true, false));
    analyseSel.value = '';
    analyseSel.disabled = true;
  }
  function resetModel() {
    modelSel.innerHTML = '';
    modelSel.append(new Option('Select model', '', true, false));
    modelSel.value = '';
    modelSel.disabled = true;
  }

  classSel.addEventListener('change', () => {
    const extract = classSel.value; // '1' ou '2'
    const allowedSmells = SMELLS_BY_EXTRACT[extract] || [];

    if (allowedSmells.length === 0) {
      resetAnalyse();
      resetModel();
      return;
    }

    const smellOptions = allowedSmells.map(v => ({ value: v, label: SMELL_LABELS[v] }));
    fillSelect(analyseSel, smellOptions, 'Select smell type');
    analyseSel.disabled = false;

    resetModel();

    if (smellOptions.length === 1) {
      analyseSel.value = smellOptions[0].value;
      analyseSel.dispatchEvent(new Event('change'));
    }
  });

  analyseSel.addEventListener('change', () => {
    const smell = analyseSel.value;
    const allowedModels = MODELS_BY_SMELL[smell];
    if (allowedModels) fillModelOptions(allowedModels);
    else resetModel();
  });

  resetAnalyse();
  resetModel();
});
document.addEventListener('DOMContentLoaded', () => {
  const extractSel = document.getElementById('extract-type');
  const smellSel   = document.getElementById('analyse-type');

  const SMELL_LABELS = {
    'large-class':         'Large Class',
    'long-method':         'Long Method',
    'long-parameter-list': 'Long Parameter List',
    'data-class':          'Data Class',
    'lazy-class':          'Lazy Class',
    'magic-numbers':       'Magic Numbers',
  };

  const SMELLS_BY_EXTRACT = {
    '1': ['large-class', 'data-class', 'lazy-class'],                     // Class
    '2': ['long-method', 'long-parameter-list', 'magic-numbers'],         // Method
  };

  function fillSelect(selectEl, values, placeholder) {
    const prev = selectEl.value;
    selectEl.innerHTML = '';
    selectEl.append(new Option(placeholder, '', true, false));
    values.forEach(v => selectEl.append(new Option(SMELL_LABELS[v], v)));

    if (values.includes(prev)) {
      selectEl.value = prev;
    } else {
      selectEl.value = '';
    }
  }

  extractSel.addEventListener('change', () => {
    const extract = extractSel.value; // '1' ou '2'
    const allowed = SMELLS_BY_EXTRACT[extract] || [];
    fillSelect(smellSel, allowed, 'Select smell type');

    smellSel.disabled = allowed.length === 0;

    if (allowed.length === 1) {
      smellSel.value = allowed[0];
      smellSel.dispatchEvent(new Event('change'));
    }
  });

  smellSel.disabled = true;
});

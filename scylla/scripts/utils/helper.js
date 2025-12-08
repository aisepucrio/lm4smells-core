(function () {
  const HELP_CONTENTS = {
    extract: {
      title: 'Extraction Type',
      html: `
        <p>Choose whether the extraction will be at the <b>Class</b> or <b>Method</b> level.</p>
        <ul>
          <li><b>Class</b>: Parses class declarations and attributes.</li>
          <li><b>Method</b>: Focuses on function bodies and signatures.</li>
        </ul>
      `
    },

    extract_method: {
      title: 'Extraction Type',
      html: `
        <p>Choose whether the extraction will be at the <b>Method</b> level.</p>
        <ul>
          <li><b>Method</b>: Focuses on function bodies and signatures.</li>
        </ul>
      `
    },

    extract_class: {
      title: 'Extraction Type',
      html: `
        <p>Choose whether the extraction will be at the <b>Class</b> level.</p>
        <ul>
          <li><b>Class</b>: Parses class declarations and attributes.</li>
        </ul>
      `
    },


     dl_smell_type: {
      title: 'Model Information (Deep Learning)',
      html: `
        <p><b>Dataset Reference:</b> Deep Learning</p>
        <br/>
        <table class="help-table">
          <thead>
            <tr>
              <th>Smell Type</th>
              <th>Model Name</th>
              <th>Description</th>
              <th>Score (Top‑5)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><b>Long Method</b></td>
              <td>Keras / AutoKeras</td>
              <td>Top‑5 architectures discovered (MLP/CNN/LSTM/GRU variants)</td>
              <td>Macro‑F1 of Top‑5 (experiments)</td>
            </tr>
            <tr>
              <td><b>Long Parameter List</b></td>
              <td>Keras / AutoKeras</td>
              <td>Top‑5 architectures discovered (structured data)</td>
              <td>Macro‑F1 of Top‑5 (experiments)</td>
            </tr>
            <!-- <tr>
              <td><b>Large Class</b></td>
              <td>Keras / AutoKeras</td>
              <td>Top‑5 architectures discovered (structured data)</td>
              <td>Macro‑F1 of Top‑5 (experiments)</td>
            </tr> -->
          </tbody>
        </table>
        <p style="margin-top:.5rem;color:#444">Top‑5 refers to the best trials from AutoKeras; see artifacts for the detailed scores and hyperparameters.</p>
      `
     },

     ml_smell_type: {
      title: 'Model Information (Machine Learning)',
      html: `
       <p><b>Dataset Reference:</b> Machine Learning</p>
        <br/>
        <table class="help-table">
          <thead>
            <tr>
              <th>Smell Type</th>
              <th>Model Name</th>
              <th>Description</th>
              <th>Score (Top‑5)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td rowspan="5"><b>Long Method</b></td>
              <td>LGBM</td>
              <td>Gradient Boosting (LightGBM)</td>
              <td>Top‑5 scores vary by dataset</td>
            </tr>
            <tr>
              <td>KNN</td>
              <td>k‑Nearest Neighbors classifier</td>
              <td>—</td>
            </tr>
            <tr>
              <td>LDA</td>
              <td>Linear Discriminant Analysis</td>
              <td>—</td>
            </tr>
            <tr>
              <td>RIDGE</td>
              <td>Ridge Classifier (linear)</td>
              <td>—</td>
            </tr>
            <tr>
              <td>SGD</td>
              <td>Linear classifier trained with SGD</td>
              <td>—</td>
            </tr>

            <tr>
              <td rowspan="5"><b>Long Parameter List</b></td>
              <td>KNN</td>
              <td>k‑Nearest Neighbors classifier</td>
              <td>—</td>
            </tr>
            <tr>
              <td>SGD</td>
              <td>Linear classifier trained with SGD</td>
              <td>—</td>
            </tr>
            <tr>
              <td>GAUSSIAN</td>
              <td>Gaussian Naive Bayes</td>
              <td>—</td>
            </tr>
            <tr>
              <td>IGB</td>
              <td>Boosting‑based classifier</td>
              <td>—</td>
            </tr>
            <tr>
              <td>QDA</td>
              <td>Quadratic Discriminant Analysis</td>
              <td>—</td>
            </tr>

            <tr>
              <td rowspan="5"><b>Large Class</b></td>
              <td>LGBM</td>
              <td>Gradient Boosting (LightGBM)</td>
              <td>Top‑5 scores vary by dataset</td>
            </tr>
            <tr>
              <td>KNN</td>
              <td>k‑Nearest Neighbors classifier</td>
              <td>—</td>
            </tr>
            <tr>
              <td>LDA</td>
              <td>Linear Discriminant Analysis</td>
              <td>—</td>
            </tr>
            <tr>
              <td>RIDGE</td>
              <td>Ridge Classifier (linear)</td>
              <td>—</td>
            </tr>
            <tr>
              <td>IR</td>
              <td>Linear model</td>
              <td>—</td>
            </tr>
          </tbody>
        </table>
        <p style="margin-top:.5rem;color:#444">Scores correspond to Top‑5 models from recent experiments; refer to your experiment logs/artifacts.</p>
      `
    },

    ast_smell_type: {
    title: 'Smell Type',
    html: `
      <br/>
      <table class="help-table">
        <thead>
          <tr>
            <th>Code Smell</th>
            <th>Main Metric</th>
            <th>Detection Heuristics</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><b>Long Method</b></td>
            <td>Method with too many lines of code or high cyclomatic complexity, making maintenance and understanding difficult</td>
            <td>LOC > 67 lines or high cyclomatic complexity (AST traversal + flow analysis)</td>
          </tr>
          <tr>
            <td><b>Large Class</b></td>
            <td>Class with too many methods, attributes or lines of code, indicating excessive responsibilities</td>
            <td>LOC > 200 or total methods + attributes > 40 (AST + Pylint R0902, R0904 messages)</td>
          </tr>
          <tr>
            <td><b>Long Parameter List</b></td>
            <td>Method or function with too many parameters, making the signature difficult to understand and maintain</td>
            <td>> 5 parameters (Pylint R0913 + cross-check with AST)</td>
          </tr>
          <tr>
            <td><b>Lazy Class</b></td>
            <td>Class with few methods and attributes or low usage, signaling an underutilized or unnecessary abstraction</td>
            <td>< 5 methods and < 5 attributes or inheritance depth < 2 (AST analysis)</td>
          </tr>
          <tr>
            <td><b>Data Class</b></td>
            <td>Class used only to store data, without associated behaviors</td>
            <td>Many attributes and few or no functional methods. LWMC > 50 or LCOM > 0.8 (Radon)</td>
          </tr>
          <tr>
            <td><b>Magic Number</b></td>
            <td>Use of literal numbers directly in code without symbolic name, impairing clarity and maintenance</td>
            <td>Any literal ≠ 0, 1, -1 not assigned to variable (AST traversal)</td>
          </tr>
        </tbody>
      </table>
    `
  },
    smell_definition: {
      title: 'Smell Definition',
      html: `
        <p>Classifying Code Smells Using Business Rules from Prior Research.</p>
        </br>
        <ul>
          <li><b>Dpy</b>: is based in this paper: <a href="https://tusharma.in/preprints/MSR2025_DPy.pdf" target="_blank">https://tusharma.in/preprints/MSR2025_DPy.pdf</a></li>
          <li><b>Scylla</b>: Our study</a></li>
        </ul>
      `
    },
    prompt_technique: {
      title: 'Prompt Technique',
      html: `
      <br/>
      <table class="help-table">
        <thead>
          <tr>
            <th>Technique</th>
            <th>Description - examples</th>
            <th>The Best Model</th>
            <th>F1-Score</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td rowspan="1"><b>Zero-Shot</b></td>
            <td>
              Classify the code as smelly or non-smelly </br>
              Code: add code </br>
              Metric: <add AST metric> (only used for Prompt with context) </br>
              return the result as one of the following JSONs: "smelly" OR "non-smelly" AND your explication about this code
            </td>
            <td>Mistral</td>
             <td>59</td>
          </tr>
          <tr>
            <td><b>Chain of Thought</b></td>
            <td>
              LMs make code difficult to understand, test, and maintain. When a method grows too large, it can exhibit high complexity, excessive conditional statements, nested loops, and 
              multiple responsibilities, violating the Single Responsibility Principle (SRP). Additionally, LMs often mix different levels of abstraction, making the code harder to read 
              and reuse. Changes in this type of code are more prone to errors, affecting multiple parts of the system. Based on these characteristics, the provided code may show signs 
              of this code smell if it has too many lines, a high level of coupling, excessive parameters or local variables, and performs multiple operations that could be extracted 
              into smaller, more cohesive functions. Does the provided code exhibit signs of a LM? </br>
              
              Code: add code </br>
              Metric: <add AST metric> (only used for Prompt with context) </br>
              return the result as one of the following JSONs: "smelly" OR "non-smelly" AND your explication about this code
            </td>
            <td>Mistral</td>
            <td>87</td>
          </tr>
        </tbody>
      </table>
      `
    },
    composite_prompt: {
      title: 'Composite Prompt',
      html: `
      <p>
        <b>AST metrics complement</b> used to enhance the code classification process.
      </p>
      <br/>

      <p>
        When this option is selected, <b>AST-based metrics</b> are included in the prompt to enrich the context used by the model.
      </p>
      <br/>

      <p>
        <b>Example</b>: Long Parameter List.</p>
        
        <br/>
        
        Classify the code as a <b>long-parameter-list</b> or a <b>non-long-parameter-list</b>.<br/>

        <b>Code:</b> def example_function(param1, param2, param3, param4, param5, param6): pass<br/>
        
        <b>Metrics:</b> JSON representation of the extracted AST metrics.
        
        </br>
        return the result as one of the following JSONs: long parameter list OR non-long parameter list AND your explication about this code.

         </br>
         </br>
        When not selected, the Metrics field is not included in the prompt.
      `
    },

    smell: {
      title: 'Smell Type',
      html: `
        <p>Choose the type of smell you need to classify.</p>
      `
    },



    slm_models: {
    title: 'Small Language Models',
    html: `
      <br/>
      <table class="help-table">
        <thead>
          <tr>
            <th>Model Name</th>
            <th>Parameters</th>
            <th>Provider</th>
            <th>Context</th>
            <th>Quantization</th>
            <th>Tags</th>
            <th>Model Size</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><b>Deepseek-r1</b></td>
            <td>1.5 billion</td>
            <td>Ollama</td>
            <td>128K</td>
            <td>Q4_K_M</td>
            <td>a42b25d8c10a</td>
            <td>1.1 GB</td>
          </tr>
          <tr>
            <td><b>Qwen2.5-coder</b></td>
            <td>1.5 billion</td>
            <td>Ollama</td>
            <td>32K</td>
            <td>Q4_K_M</td>
            <td>6d3abb8d2d53</td>
            <td>986 MB</td>
          </tr>
          <tr>
            <td><b>Mistral</b></td>
            <td>7.25 billion</td>
            <td>Ollama</td>
            <td>32K</td>
            <td>Q4_0</td>
            <td>f974a74358d6</td>
            <td>4.1 GB</td>
          </tr>
          <tr>
            <td><b>Gemma2</b></td>
            <td>2.61 billion</td>
            <td>Ollama</td>
            <td>8K</td>
            <td>Q4_0</td>
            <td>8ccf136fdd52</td>
            <td>1.6 GB</td>
          </tr>
          <tr>
            <td><b>Codellama</b></td>
            <td>6.74 billion</td>
            <td>Ollama</td>
            <td>16K</td>
            <td>Q4_0</td>
            <td>8fdf8f752f6e</td>
            <td>3.8 GB</td>
          </tr>
        </tbody>
      </table>
    `}

  };

  function openHelpById(id) {
    const content = HELP_CONTENTS[id];
    if (!content) return;
    openHelp(content.title, content.html);
  }

  function openHelp(title, html) {
    const modal   = document.getElementById('help-modal');
    if (!modal) { console.error('[help] #help-modal não encontrado'); return; }

    const titleEl = modal.querySelector('#hm-title');
    const bodyEl  = modal.querySelector('#hm-body');

    if (!titleEl || !bodyEl) {
      console.error('[help] Elementos internos não encontrados', { titleEl, bodyEl });
      return;
    }

    titleEl.textContent = title || 'Help';
    bodyEl.innerHTML    = html   || 'Ajuda do campo selecionado.';

    modal.hidden = false;
    modal.setAttribute('aria-hidden', 'false');
  }

  function closeHelp() {
    const modal  = document.getElementById('help-modal');
    if (!modal) return;
    const bodyEl = modal.querySelector('#hm-body');
    if (bodyEl) bodyEl.innerHTML = '';
    modal.hidden = true;
    modal.setAttribute('aria-hidden', 'true');
  }

  function init() {
    document.addEventListener('click', (e) => {
      const icon = e.target.closest('.info-icon');
      if (icon) {
        const id = icon.dataset.helpId;
        if (id) { openHelpById(id); return; }
        const title = icon.getAttribute('data-help-title') || 'Help';
        const html  = icon.getAttribute('data-help-text')  || 'Ajuda do campo selecionado.';
        openHelp(title, html);
        return;
      }

      const modal = document.getElementById('help-modal');
      if (!modal) return;
      if (e.target.matches('[data-hm-close]') || e.target === modal) closeHelp();
    });

    document.addEventListener('keydown', (e) => {
      const modal = document.getElementById('help-modal');
      if (modal && !modal.hidden && e.key === 'Escape') closeHelp();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

### 🧩 General Metadata


| **Field**             | **Type** | **Description**                                                                                 |
| --------------------- | -------- | ----------------------------------------------------------------------------------------------- |
| `task_id`             | str      | Identifier for the scheduled code classification or analysis task.                              |
| `file_name`           | str      | Name of the source code file.                                                                   |
| `file`                | list     | Reference or list of files containing the code to be analyzed.                                  |
| `programming_language`| str      | Programming language used (e.g., Python, Java).                                                 |
| `class_name`          | str      | Name of the class where the method or function is defined.                                      |
| `method_name`         | str      | Name of the analyzed method or function.                                                        |
| `extract_type`        | int      | Type of extract (e.g., class, method).                                                          |
| `analyse_type`        | str      | Type of analysis (e.g., smell, metric).                                                         |
| `smell_definition`    | enum     | Defines which study approach or taxonomy is used to classify code smells.                       |
| `ml_model`            | enum     | Indicates which machine learning model is used for code classification.                         |
| `dl_model`            | enum     | Indicates which deep learning model is used for code classification.                            |
| `code`                | str      | Raw source code being analyzed.                                                                 |
| `prompt_type`         | str      | Type of prompt used with the language model (e.g., LM, LPL).                                    |
| `prompt`              | str      | Prompt text provided to the model.                                                              |
| `model`               | str      | Name of the model used for the analysis (e.g., GPT-4, Claude, Mistral, Gemma, CodeLlama).       |
| `is_composite_prompt` | bool     | Indicates whether the prompt combines multiple components or includes AST/contextual data.       |

---

### Code Metrics – Field `code_metric`

#### Basic Metrics

| **Field** | **Type** | **Description**              |
| ---------- | -------- | ---------------------------- |
| `loc`      | int      | Total lines of code.          |
| `lloc`     | int      | Logical lines of code.        |
| `sloc`     | int      | Source lines of code.         |
| `comments` | int      | Number of comment lines.      |
| `multi`    | int      | Number of multi-line comments.|
| `blanks`   | int      | Number of blank lines.        |

---

#### Cyclomatic Complexity (`cc`)

| **Field**    | **Type** | **Description**                        |
| ------------- | -------- | -------------------------------------- |
| `type`        | str      | Type of entity (e.g., method, function). |
| `rank`        | str      | Complexity rank.                        |
| `lineno`      | int      | Start line of the entity.               |
| `endline`     | int      | End line of the entity.                 |
| `name`        | str      | Function or method name.                |
| `complexity`  | int      | Cyclomatic complexity value.            |
| `col_offset`  | int      | Starting column position.               |
| `closures`    | list     | Nested closures, if any.                |

---

#### Maintainability Index (`MI`)

| **Field** | **Type** | **Description**                   |
| ---------- | -------- | --------------------------------- |
| `mi`       | float    | Maintainability Index score.      |
| `rank`     | str      | Maintainability rank.             |

---

#### Halstead Metrics – Subfield `total`

| **Field**            | **Type** | **Description**                          |
| -------------------- | -------- | ---------------------------------------- |
| `h1`, `h2`           | int      | Distinct operators and operands.         |
| `n1`, `n2`           | int      | Total occurrences of operators and operands. |
| `vocabulary`         | int      | Code vocabulary size.                    |
| `length`             | int      | Program length.                          |
| `calculated_length`  | float    | Estimated length.                        |
| `volume`             | float    | Implementation volume.                   |
| `difficulty`         | float    | Estimated difficulty.                    |
| `effort`             | float    | Estimated implementation effort.         |
| `time`               | float    | Estimated time (in seconds).             |
| `bugs`               | float    | Estimated number of potential bugs.      |

---
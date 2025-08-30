## Code Contract to Send to API – Field Descriptions

### General Metadata

| **Field**             | **Type** | **Description**                                                        |
| --------------------- | -------- | ---------------------------------------------------------------------- |
| `is_composite_prompt` | bool     | Indicates if the prompt includes AST context.                          |
| `model`               | str      | Name of the model (e.g., Mistral, Gemma, codellama).                    |
| `prompt_type`         | str      | Type of prompt used with the LM (e.g., LM, LPL).                       |
| `prompt`              | str      | Prompt text provided to the model.                                      |
| `analyse_type`        | str      | Type of analysis (e.g., smell, metric).                                 |
| `extract_type`        | int      | Type of extract (e.g., class, method).                                  |
| `file`                | list     | Refers to the file containing the code to be analyzed.                  |

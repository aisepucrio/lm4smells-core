# Code-smell-analysis

## Brief Description

The developed program is a fully functional utility tool with an integrated front-end interface, designed to enable the analysis and extraction of structural information from user-submitted source code, with a specific focus on identifying classes and methods.

The application allows users to submit their code for processing and specify additional parameters that guide the extraction behavior. Among these options is the ability to define custom prompts, which help Small Language Models (SLMs) correctly interpret the context or intent of the desired analysis.

Additionally, users can select the most suitable SLM for their use case, choose the type of extraction (e.g., limiting it to class or method identification), and receive immediate feedback regarding the start and progress of the processing, providing greater clarity, predictability, and ease of monitoring throughout the execution of the task.

The program was primarily designed to serve researchers and professionals in the fields of Software Engineering, Computer Science, and related disciplines who need to perform automated structural analysis of large volumes of source code. Furthermore, the tool can be highly useful for Computer Science students, especially those involved in software analysis projects, reverse engineering, or research in automatic source code processing.

The nature of the project is that of a production-ready solution, already delivered, fully functional, and available to end users. It was developed with a distributed architecture, where the front-end communicates efficiently with the back-end, ensuring scalability, modularity, and the ability to support different use scenarios in the context of source code analysis with specialized language model support.

## Project Vision – Scenarios
Below are four scenarios that reflect both the creators' intentions for the project and the expected and unexpected usage by end users. These scenarios serve as a guide for the development, maintenance, and future evolution of the application.

### Positive Scenario 1 – Use by a Researcher for Code Smell Detection in Large Codebases

Renata is a Software Engineering researcher studying the occurrence of code smells in open-source projects. She accesses the application via a web browser and uploads a set of Python files from a repository she wants to analyze. In the "Extraction Type" field, she selects the "Method" option and chooses the type of smell she wants to identify (e.g., "Long Method"). She selects an available SLM model to analyze the code and defines a custom prompt to refine the model’s interpretation. Upon starting the process, the application displays a notification indicating that the processing has begun. Shortly after, Renata is able to view the results in the database, with detailed outputs for each submitted code file. The workflow fully meets her research expectations.


### Positive Scenario 2 – Use by a Student for Didactic Code Smell Analysis

Carlos, a Computer Science student, is learning about code smells and wants to practice identifying these issues in his own Python projects. He accesses the application, uploads a small set of files from a university assignment, selects "Smell Type: Long Method," chooses a predefined prompt offered by the interface, and selects a language model. Carlos runs the process and, at the end, uses the database to retrieve the results about his submitted algorithms for possible corrections. The experience is straightforward and educational, fully within the expected use of the tool.


### Negative Scenario 1 – User Trying to Submit Code in an Unsupported Language

Fernanda, a PHP developer, attempts to use the application to analyze a project written in PHP. She uploads the PHP files, configures the smell type and language model, but upon starting the process, the system returns inconsistent and irrelevant results. After reviewing the tool’s documentation, she realizes that the application currently supports only Python code analysis, with the inclusion of other languages planned for future versions. Fernanda then decides to wait for the tool's evolution.


### Negative Scenario 2 – User Attempting to Submit Invalid or Nonexistent Values in Interface Fields

André, a curious developer, decides to test the application's limits. While filling out the form, instead of using the predefined options in the selection fields (such as "Extraction Type," "Smell Type," "Model," and "Prompt Type"), he tries to manually inject nonexistent values directly into the page's source code using browser inspection tools or by manipulating backend API requests.

For example, he attempts to submit a smell type called "Nonexistent Smell" and a model named "fake-model," which are not part of the valid options. Upon sending the request, the backend performs validation and returns an error indicating that something is wrong.

Additionally, the interface displays a warning message to the user, informing that there was an error in the submission. André realizes that the application has robust validation mechanisms to prevent this kind of improper input and decides to follow the standard workflow in his next attempts.


## Project Technical Documentation

This section presents the technical details necessary for other developers to understand, reuse, or evolve the program.

* Specification of Functional and Non-Functional Requirements
    * **Functional:** File upload, prompt configuration, model selection, request submission to the backend, processing status display. 

    * **Non-Functional:** Usability, interface response time, compatibility with modern browsers.

* About the Code

    The front-end of the "Code Smell Analysis" application was developed using basic web technologies: HTML5, CSS3, and pure JavaScript (Vanilla JS). The choice of these technologies aimed to ensure simplicity, ease of maintenance, and a low learning curve for future contributors.

    * Programming Language and Technique Used:
        * **HTML5:** Responsible for structuring the application interface, defining the file upload fields, option selection menus, and the overall page layout.

        * **CSS3:** Used for styling the interface, with a focus on responsiveness, readability, and providing a pleasant visual experience for the user.

        * **JavaScript (Vanilla JS):** Responsible for all user interaction logic, including:
            * DOM manipulation (e.g., displaying status messages, capturing form data).
            * Basic input field validation.
            * Sending HTTP requests to the application backend using fetch().


## User Manual for Target Users

```
The "Code Smell Analysis" application was developed for two main user profiles:

- Researchers and Software Engineering professionals
- Computer Science students and related fields

Below are detailed instruction guides for each task that the user can perform:

---

Instruction Guide - Analyzing Source Code for Code Smell Detection
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

To **analyze source code for code smell detection**, follow these steps:

Step 1: Open your web browser and access the application interface.

Step 2: In the **"File Upload"** section, drag and drop the desired Python files or click the area to select them manually.

Step 3: Under **"Extraction Type"**, select the desired option (e.g., `Class`, `Method`).

Step 4: In **"Smell Type"**, choose the type of smell you want to analyze (e.g., `Large Class`, `Long Method`, `Long Parameter List`).

Step 5: Under **"Model"**, select one of the available language models (e.g., `gemma2:2b`, `deepseek-r1:1.5b`, etc.).

Step 6: In **"Prompt Type"**, choose the desired prompt type (e.g., `Zero-shot`, `Zero-shot Chain of Thought`).

Step 7: In the **"Prompt"** field, enter the text you want to send to the model.

Step 8: If you want to extract information from the code using AST, check the **"Composite Prompt"** option.

Step 9: Click the **"Submit Request"** button to start processing.

Step 10: Wait until the **Submit Request** button finishes loading and the success notification appears, indicating that the process has been completed.

---

## Exceptions or Potential Issues:

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

If **no file is selected**  
Action: Select at least one file before submitting.

If **the Extraction Type is not selected**  
Action: Choose a valid option before submitting.

If **the Model is not selected**  
Action: Select a model before proceeding.

If **the Smell Type does not apply to the selected Extraction Type**  
Action: Review the fields and adjust the configuration accordingly.

If **non-Python files are uploaded**  
Reason: The application currently supports analysis of Python files only.

---

## Instruction Guide – Using the Prompt:

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

To **use the prompt**, follow these steps:

Step 1: In the **"Prompt Type"** field, choose the option most appropriate for the analysis context.

Step 2: In the **"Prompt"** field, enter the text that will guide the SLM.

Step 3: If desired, enable the **"Composite Prompt"** option to combine the AST technique with your prompt.

Step 4: Fill in the remaining fields (file upload, model, extraction type).

Step 5: Click **"Submit Request"**.


---

## Exceptions or Potential Issues:

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

If **the prompt is vague or poorly formulated**  
Reason: The result may be generic or out of context.  
Action: Rewrite the prompt to be clearer and more objective.

If **the prompt is on a topic outside the tool's scope**  
Reason: The SLM may generate an unexpected response.  
Action: Limit the prompt to instructions related to code smell analysis.


---

## Instruction Guide – Selecting the Appropriate Language Model:

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

To **select the appropriate language model**, follow these steps:

Step 1: In the **"Model"** field, select one of the available options.

Step 2: Refer to the Ollama documentation, if necessary, to understand the differences between models.

Step 3: Complete the remaining fields in the interface.

Step 4: Click **"Submit Request"**.


---

## Exceptions or Potential Issues:

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

If **no model is selected**  
Action:Select a model before submitting the request.

If **the model is unavailable in the execution environment**  
Reason: The backend could not locate or activate the requested model.  
Action: Choose another available model.


---

Instruction Guide – Avoiding the Use of Invalid Values in Interface Fields:
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

To **avoid using invalid values in interface fields**, follow these steps:

Step 1: Fill in only with the values provided in the interface dropdown menus.

Step 2: Do not attempt to modify values directly in the page source code or in network requests.

Step 3: Before submitting, review all fields to ensure they are within the valid options.

---

Exceptions or Potential Issues:
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

If the user tries to submit invalid or nonexistent values (e.g., a smell type that doesn't exist or an invalid model)**  
Reason: The application performs validations and blocks requests with parameters outside the allowed scope.  
Action: Review the fields and select only the options displayed by the interface.
```
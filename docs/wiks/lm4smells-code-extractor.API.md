# Lm4smells-code-extractor.API

## Brief Description

The developed program is a fully functional and ready-to-use utility tool designed to extract structural characteristics from Python source code using the Abstract Syntax Tree (AST) technique. Its main function is to operate as an intermediate module within an Anti-Corruption Layer (ACL), receiving requests from the frontend service, processing the submitted files, and extracting relevant information such as the classes and methods present in the code, along with their respective properties.

Key functionalities include static code analysis for structural extraction (including the identification of classes and methods), the generation of events containing the extracted data for consumption by other system services (such as the lm4smells-lm-integrator), and the export of analysis results in a standardized JSONL format, facilitating integration with research workflows, reports, or other analysis tools.

This tool was primarily designed to support researchers and professionals in the fields of Software Engineering and Software Quality, especially those involved in empirical studies, automated code analysis, and software metrics research. It is also intended for university students enrolled in Computer Science or Software Engineering programs, particularly those engaged in projects or research focused on source code quality assessment.

The nature of this project is that of a finalized, modular, and fully operational utility tool, already in use within the context of a distributed software analysis system powered by Small Language Models (SLMs).


## Project Vision – Scenarios
Below are four scenarios that reflect both the creators' intentions for the project and the expected and unexpected usage by end users. These scenarios serve as a guide for the development, maintenance, and future evolution of the application.


### Positive Scenario 1 (Successful Use)

Marina is a researcher in Software Engineering and is conducting a study on the source code structure in Python projects. Her goal is to analyze the number of classes, methods, and other structural characteristics based on the AST (Abstract Syntax Tree) representation. To do this, she prepares a set of Python files and makes a direct request to the tool's API, sending the files for processing. The application extracts the structural information and returns the results in JSONL format, with all the details of classes, methods, and their properties. With the data in hand, Marina is able to efficiently advance her research.


### Positive Scenario 2 (Successful Use)

Lucas, an undergraduate student in Computer Science, is developing his Final Year Project (FYP) on code quality. One of the stages of his research involves evaluating the quality of the names used in the classes and methods of his Python project. To perform this analysis, Lucas needs a quick way to extract all the names present in the code. He then sends his files to the tool’s API, which processes the data using the AST technique and returns a structured list with all the identified classes and methods. With this information, Lucas is able to review the names, assess their clarity and adherence to best practices, and include this analysis in his final report.


### Negative Scenario 1 (Unexpected Use / Improper Interaction)
Carla, a beginner programming instructor, tries to use the tool to analyze a set of Java files. She doesn’t realize that the application was designed only for Python code. After submitting the files, the system returns a syntax analysis error. Not understanding the cause, Carla tries again with another Java project but receives the same error message. This usage error highlights the importance of the tool clearly stating on the frontend which programming languages are supported and improving error handling to better guide the user.

### Negative Scenario 2 (Expected Technical Limitation)
Rafael, a developer at a startup, is using the tool to analyze a Python project that contains comments and identifiers written in Arabic. During processing, while trying to extract structural characteristics based on AST, the system throws an exception related to character encoding. The failure occurs because the tool is not yet prepared to handle some languages that use character sets very different from standard UTF-8. Rafael realizes that the limitation is related to the tool’s language support and decides to adjust the files to use only compatible characters before trying again.


## Project Technical Documentation

This section presents the technical details necessary for other developers to understand, reuse, or evolve the program.

* Functional and Non-Functional Requirements Specification
    * **Functional:** 
        * **Receiving Requests via REST API:** The application exposes REST endpoints to receive Python files sent by users.

        * **AST Processing:** It performs parsing of the files to extract the code structure (classes, methods, and their properties) using the Abstract Syntax Tree (AST) technique.

        * **Event Publishing:** After extraction, the system publishes the processed data to a messaging queue, allowing other services (e.g., SLM integrator) to consume the results.

        * **Result Export:** The results can be exported in JSONL format, making integration with other tools and workflows.

    * **Non-Functional Requirements:** 
        * **Modular Architecture:** The project follows a modular organization inspired by Domain-Driven Design (DDD), facilitating maintenance, scalability, and component reuse.

        * **Asynchronous Communication:** Interaction between microservices is done via messaging, ensuring decoupling between modules and increasing fault tolerance.

        * **Performance and Scalability:** The system was developed to handle multiple simultaneous requests, with queue control to avoid memory overload during AST processing.

        * **Error Handling:** Includes mechanisms for capturing and logging exceptions, such as parsing issues, corrupted files, or unsupported characters.

* Architecture Description

    The application follows a microservices-based architecture with the following main components:

    * **AST Extraction API:** The core service of this project, responsible for processing Python files, performing AST extraction, and publishing events.

    * **Messaging Broker:** Enables asynchronous communication between the extraction API and other consumer microservices, such as the SLM integration service.


## User Manual for Target Users

This manual is intended for researchers, developers, and students who wish to use the program as part of a software quality analysis system supported by language models.

```
## User Instructions Guide
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

To extract classes and methods from Python files, follow these steps:

Step 1: Prepare the Python (.py) files you want to analyze.  
Step 2: Access the tool's API using an HTTP client (such as Postman, Insomnia, or programmatically using libraries like `requests` in Python).  
Step 3: Make a POST request to the `/extract-ast` endpoint, attaching the files in the request body.  
Step 4: Wait for processing. The application will perform the structural extraction using AST.  
Step 5: The application will publish the analysis to the event bus.  
Step 6: Receive the response in JSON format with the list of classes or methods and their properties.  
Step 7 (Optional): Save the response as a JSONL file for later use in reports or further analysis.

---

## Exceptions or Potential Issues
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

If: Non-Python files (.py) are sent  
Then: The API will return an error indicating an invalid file type.  
Solution: Make sure you are sending only Python files.

If: Files contain incompatible characters (e.g., Arabic text or other languages with unsupported encoding)  
Then: A parsing exception may occur during AST processing.  
Solution: Check the file encoding. Recommended: use UTF-8.

If: The project size is too large, exceeding memory limits during processing  
Then: The system may interrupt the analysis and return a processing failure.  
Solution: Split the files into smaller batches and send them separately.

---

## Instructions for AST Extraction with Event Publishing
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

To perform AST extraction with event publishing for other services via messaging, follow these steps:

Step 1: Ensure the messaging service (e.g., RabbitMQ, Kafka) is running and accessible by the extraction application.  
Step 2: Verify that the connection settings (host, port, credentials) are correct in the application's configuration file.  
Step 3: Send the Python files to the tool's API using a POST request to the `/` endpoint.  
Step 4: After processing, the application will automatically publish an event containing the extracted information to the configured topic or queue.  
Step 5: Ensure that downstream consumer services (e.g., the SLM integration service) are listening to the queue to receive the events.  
Step 6: If needed, monitor the logs to check the status of event publishing and consumption.

---

## Exceptions or Potential Issues
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

If: The messaging service is down or inaccessible at the time of event publishing  
Then: The application may throw a connection or publish failure exception.  
Solution:
- Verify that the messaging service is active.
- Confirm the connection credentials and address.
- Restart the messaging service if necessary.
- Try resending the request after restoring the environment.

If: The destination queue or topic is not properly configured  
Then: The event may be lost or not delivered.  
Solution: Review the topic/queue configuration before execution.
```
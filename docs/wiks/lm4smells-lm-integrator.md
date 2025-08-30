# Lm4smells-lm-integrator

## Brief Description

The developed program is a fully functional utility tool designed to act as an event consumer within a distributed software quality analysis system. Its main function is to receive event messages from the central router, process the data according to the attributes defined in each event payload, and interact with Small Language Models (SLMs) to perform specialized code analysis tasks.

Among its key features, the application offers dynamic interaction with SLMs, either through direct execution using an Ollama instance, depending on configuration. Once the analysis is completed, the application processes the operational data and stores the results in a relational database, ensuring long-term availability for reporting, research, and quality tracking.

This tool was primarily developed to serve researchers and professionals in the fields of Software Engineering and Software Quality, especially those involved in empirical studies, automated code analysis, and research on code smells and software maintainability. It can also be useful for university students engaged in research projects focused on source code quality.

The nature of this project is that of a production-ready, fully modular utility tool, operating as a key component within a distributed, event-driven architecture designed for automated software quality assessment.


## Project Vision

### Positive Scenario 1 (Successful Use)
João, a researcher in Software Engineering, is conducting a study on the effectiveness of different LMs in detecting code smells. To do this, he configures the system's router to send analysis events directly to the event consumer (the program described here). As soon as the consumer receives the event, it processes the payload, calls the configured SLM via Ollama, receives the response with the smell analysis, and stores the results in the relational database. With the data saved, João can perform SQL queries to compare the results between different models.

### Positive Scenario 2 (Successful Use)
Laura, a graduate student in Computer Science, is evaluating the code quality of an open-source project. She uses the complete system, which includes the event router and the consumer. When she submits the source code for analysis, the router generates events that reach the consumer. The consumer, in turn, queries a local Ollama model to perform the code smell analysis. After processing, Laura accesses the database and quickly retrieves the results to include comparative charts in her thesis.

### Negative Scenario 1 (Unexpected Use / Integration Error)
Carlos, a junior developer, decides to test the system and accidentally sends an event with a malformed payload, missing the required attributes expected by the application. The event consumer tries to process the message but fails due to the absence of the necessary fields to query the SLM. The system logs the error, and the message is not processed, ensuring that only well-structured events are executed.

### Negative Scenario 2 (Failure Due to External Dependency)
Fernanda, a quality analyst, runs a batch of events to analyze a large project. However, during processing, the Ollama instance goes offline. The event consumer tries to connect to the SLM via Ollama but receives a connection error. Since the application depends on the Ollama instance being operational, the event is returned to the queue and not processed. Fernanda checks the logs, identifies the issue, and after restoring Ollama, decides to reprocess the pending events.


## Project Technical Documentation

This section presents the technical details necessary for other developers to understand, reuse, or evolve the program.

* Functional and Non-Functional Requirements Specification
    * **Functional:** 
         * **Event Consumption:** The program acts as an event consumer, receiving messages from a RabbitMQ broker.

        * **Processing with SLMs:** Upon receiving an event, the application interprets the payload and performs queries to Small Language Models (SLMs), using Ollama as the SLM backend.

        * **Result Persistence:** The results of the analyses performed by the models are processed and stored in a relational SQLite database.

        * **Failure Tolerance:** If the received event is malformed or there is a failure in connecting to the SLM, the system logs the occurrence for later review and possible reprocessing.


    * **Non-Functional:**
        * **Modular Architecture:** The project is organized into layers following Domain-Driven Design (DDD) principles, with clear separation between Application, Domain, and Infrastructure.

        * **Asynchronous Communication:** All input communication is handled asynchronously through messaging (RabbitMQ), allowing decoupling between producer and consumer.

        * **Portability:** Developed in Python, the system runs easily on any environment that supports Python 3.x.

        * **Database:** The application uses SQLite as the database, providing a lightweight and easy-to-configure solution.

        * **Future Scalability:** Although SQLite is currently used, the architecture allows switching to other relational databases if needed.

* About the Code
    * **Programming Language:** The project was developed using Python 3.x.
    * **Layered Structure:** The code is organized following a layered architecture inspired by DDD:   

        * **Application Layer:** Contains the use cases of the application, responsible for orchestrating the event processing flow.

        * **Domain Layer:** Defines the domain entities used to persist data in the database.

        * **Infrastructure Layer:** Includes the concrete implementations for consuming events via RabbitMQ, integrating with Ollama, and persisting data in SQLite.

    * **Messaging Integration:** The Infrastructure layer implements a RabbitMQ consumer configured to listen to queues where the router publishes events.

    * **SLM Integration:** Communication with the SLM is performed via Ollama, sending the analysis prompts found in the event payload.

    * **Data Persistence:** The Infrastructure module also contains the repositories responsible for saving the analysis results into the SQLite database.

    * **External Dependencies:** The project uses libraries such as:
        * `pika`: For communication with RabbitMQ
        * `sqlite3`: For local result persistence
        * `.env`: To store the application’s environment variables



## User Manual for Target Users

This manual is intended for researchers, developers, and students who wish to use the program as part of a software quality analysis system supported by language models.

```
Instruction Guide:
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
To automatically process events using a language model, follow these steps:

Step 1: Make sure the messaging service (RabbitMQ) is active and accessible.
Step 2: Run the command to install dependencies (e.g., pip install -r requirements.txt) inside the app folder.
Step 3: Start the application by executing the event consumer (e.g., via python main.py).
Step 4: Check whether the configured queue is receiving events from the router (the events must contain source code and metadata).
Step 5: Once the consumer receives an event, it will interpret the payload and send the content to a language model (via Ollama).
Step 6: The model's response will be processed and automatically stored in the SQLite database, structured for future queries.
Step 7: To view or use the data, access the SQLite database using a tool of your choice (DBeaver, DB Browser for SQLite, etc.).


Exceptions or Potential Issues:
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

If: The messaging service is offline or misconfigured
Then: The application will not be able to consume events, remaining idle or throwing a connection error.
Solution: Check whether RabbitMQ is running, and review the host, port, and queue configuration.

If: The received event is malformed (e.g., missing required fields in the payload)
Then: The program may throw exceptions during event parsing.
Solution: Ensure the event producer validates the structure before sending.

If: Ollama is inactive or the client is misconfigured
Then: The application will not be able to obtain a response from the language model, resulting in an integration error.
Solution: Verify that Ollama is running locally or that the external endpoint is reachable.

If: The SQLite database is corrupted or inaccessible
Then: Data persistence will fail, possibly leading to data loss.
Solution: Check for proper read/write permissions and ensure no concurrent processes are locking the file.

```









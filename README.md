<div align="center" >
    <h1>Code Smell Classification in Python: </br> Are Small Language Models Up to the Task?</h2>
</div>

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17074239.svg)](https://doi.org/10.5281/zenodo.17074239)


The pre-print for the paper is available [here](Paper_SBES_IIER_2025.pdf)

# Citation

```bibtex
@Inproceedings{soares_de_oliveira2025:SBES,
  author = {Soares de Oliveira, Igor and Carneiro, Joanne and Ribas, Jessica and Pereira, Juliana Alves},
  title     = {Code Smell Classification in Python: Are Small Language Models Up to the Task?},
  year      = {2025},
  pages     = {1–7},
  booktitle = {Brazilian Symposium on Software Engineering, Insightful Ideas and Emerging Results Track (SBES IIER)},  
  publisher = {SOL}
}
```


# Code-smell-analysis

The application serves as a front-end interface, allowing users to submit code for processing and extraction. It also provides the option to specify additional details, such as the prompt that will help the SLM interpret the context or intended query, the selection of the SLM to be used during processing, and the definition of the extraction type, whether for classes or methods. Furthermore, the application informs the user when processing begins, ensuring clarity and ease of use throughout the execution of the task.

## Built with
* HTML
* CSS
* JavaScript

## How to run?

* 1 - Open ```index.html``` in your browser.


## Dependencies

* lm4smells-code-extractor.API

----------
</br>

# lm4smells-code-extractor.API

The application operates within an anti-corruption layer (ACL), acting as an event producer. Its main responsibility is to receive requests from the frontend service, process them, and extract relevant information, such as the classes or methods present in the submitted files. This functionality enables the identification of classes and methods, along with their respective properties. To achieve this, the application uses the Abstract Syntax Tree (AST) technique, which provides a structural representation of the input code. After extracting the information, the application sends an event to the router, allowing the lm4smells-lm-integrator service to consume it.


## Built with
* [Python 3.10](https://www.python.org/downloads/release/python-3100/)
* [RabbitMq](https://www.rabbitmq.com/)


## Project Structure

```
├──📁 lm4smells-code-extractor.API
│   ├──📁 docs
│   ├──📁 src
│   |   ├──📁 app
│   |   |   ├──📁 application
│   |   |   └──📁 infrastructure
│   ├──📄 changelog
│   ├──📄 .gitignore

```

## How to run?

* 1 - Make sure you are in the `app` folder
* 2 - Run: `pip install -r requirements.txt`
* 3 - Set up with Unix System ```export $(grep -v '^#' .env | xargs -0)```
* 3 - Set up with Windows System ``` Get-Content .env | ForEach-Object {
    if ($_ -notmatch '^#' -and $_ -match '=') {
        $parts = $_ -split '=', 2
        [System.Environment]::SetEnvironmentVariable($parts[0], $parts[1], "Process")
    }
}```

* 4 - Run: `fastapi dev main.py`
* 5 - Host: `http://localhost:8000/docs`


## Dependencies

* RabbitMq
* lm4smells-lm-integrator

----------
</br>

# lm4smells-lm-integrator

The main objective of this application is to act as an event consumer, receiving messages from the router and processing them according to the attributes defined in the event payload. To perform this processing, the application interacts with SLMs, either through an instance of Ollama or via RESTful protocols. After the processing is completed and the operational data is obtained, the results are stored in a relational database, ensuring their availability for data analysis and future research.


## Built with
* [Python 3.10](https://www.python.org/downloads/release/python-3100/)
* [Ollama](https://ollama.com/)
* [RabbitMq](https://www.rabbitmq.com/)


## Project Structure

```
├──📁 lm4smells-lm-integrator
│   ├──📁 docs
│   ├──📁 src
│   |   ├──📁 app
│   |   |   ├──📁 application
│   |   |   ├──📁 domain
│   |   |   └──📁 infrastructure
│   ├──📄 changelog
│   ├──📄 .gitignore

```

## How to run?

* 1 - Make sure you are in the `app` folder
* 2 - Run `pip install -r requirements.txt`
* 3 - Set up with Unix System ```export $(grep -v '^#' .env | xargs -0)```
* 3 - Set up with Windows System ``` Get-Content .env | ForEach-Object {
    if ($_ -notmatch '^#' -and $_ -match '=') {
        $parts = $_ -split '=', 2
        [System.Environment]::SetEnvironmentVariable($parts[0], $parts[1], "Process")
    }
}```
* 4 - Run [Ollama](lm4smells-lm-integrator/src/app/application/dtos/slm_ollama_models.py) with the models you intend to use
* 5 - Run `python main.py`


## Dependencies 

* RabbitMq
* Ollama

----------
</br>


# Contracts

This project adopts a distributed architecture, in which each service is responsible for a specific part of the system and, consequently, uses contracts to establish communication between the microservices. All contracts are organized in the [contract](docs/contracts) folder.


# Machine Learning 

This application uses machine learning techniques to enhance the classification of code smells by analyzing multiple project-related metrics. The models were developed and executed using the PyCaret library, leveraging a set of 15 widely adopted ML algorithms commonly used in defect and code smell classification tasks.


## Machine Learning Algorithms Used

| #  | Algorithm Name                         | Abbreviation | Description                                                                 |
|----|---------------------------------------- |------------- |-----------------------------------------------------------------------------|
| 1  | k-Nearest Neighbor                     | kNN          | Instance-based learning algorithm that classifies data based on proximity.  |
| 2  | Linear Regression                      | LR           | Models the relationship between variables by fitting a linear equation.     |
| 3  | Support Vector Machine                  | SVM          | Finds the hyperplane that best separates classes in high-dimensional space. |
| 4  | Decision Tree                          | DT           | Tree-based model that splits data into branches based on feature values.    |
| 5  | Random Forest                          | RF           | Ensemble of decision trees to improve predictive accuracy and control overfitting. |
| 6  | Extreme Gradient Boosting package       | XGB          | Optimized gradient boosting framework with regularization to reduce overfitting. |
| 7  | Ridge Classifier                        | RC           | Linear classifier with L2 regularization to prevent overfitting.            |
| 8  | Light Gradient Boosting                 | LGB          | Fast, efficient gradient boosting framework optimized for speed and performance. |
| 9  | Gradient Boosting                       | GB           | Ensemble method that builds models sequentially to minimize prediction errors. |
| 10 | Ada Boost                               | ADA          | Boosting method that combines weak classifiers to form a strong classifier. |
| 11 | Extra Trees                             | ET           | Ensemble of randomized decision trees that improves diversity and performance. |
| 12 | Naive Bayes                             | NB           | Probabilistic classifier based on applying Bayes' theorem with independence assumptions. |
| 13 | Linear Discriminant Analysis            | LDA          | Linear classifier that projects data to maximize class separability.        |
| 14 | Quadratic Discriminant Analysis         | QDA          | Variant of LDA that allows quadratic decision boundaries.                   |
| 15 | Dummy Classifier                        | DC           | Baseline model that makes predictions using simple rules (e.g., stratified, most frequent). |



# Deep Learning

This application uses deep learning techniques to improve the classification of code smells by capturing complex, non-linear relationships between various project-related metrics. The models were developed and executed using state-of-the-art DL architectures, including MLP, LSTM, GRU, and AutoKeras, which automates neural network design and optimization for enhanced performance.


## Deep Learning Algorithms Used

| #  | Algorithm Name                         | Abbreviation | Description                                                                |
|----|---------------------------------------- |------------- |----------------------------------------------------------------------------|
| 1  | Multi-Layer Perceptron                  | MLP          | Neural network with multiple layers, effective in modeling complex patterns.|
| 2  | Long Short-Term Memory                  | LSTM         | RNN variant specialized in capturing long-term temporal dependencies.       |
| 3  | Gated Recurrent Unit                    | GRU          | Simplified RNN variant, often with performance comparable to LSTM.          |
| 4  | AutoKeras                               | -            | Automated framework for designing and tuning deep learning models.          |

---


## Guide to the Files and Their Execution

This section provides an overview of the files used in this study, as well as instructions on how to use them effectively. The repository is organized into different folders containing datasets, scripts for code extraction and analysis, trained machine learning models, and supporting resources for the execution of the described experiments.

Each subsection explains the purpose of the files, how they contribute to the workflow, and provides step-by-step guidance on how to run the scripts or use the data. Whether you are exploring the dataset, replicating model training, performing code extraction, or analyzing the results related to explainability, the instructions provided here will help you understand and use each component of the [repository](docs/experiments/study_processes.md).




# Artifacts


This repository provides the artifacts associated with the paper, including the code used to extract the algorithms analyzed by PySmell, validating their correctness; the datasets containing the classified code samples; and the models employed in the experiments, with the aim of supporting result reproducibility and fostering further research. [Zenodo](https://zenodo.org/records/17074239)


<!-- 
# Article

[📄 Link to the Article]() -->


# License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute it as permitted under the terms of this license.

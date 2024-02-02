![](https://img.shields.io/badge/python-v3.11-blue)
![](https://img.shields.io/badge/Flask-v3.0.1-pink)
![](https://img.shields.io/badge/Docker-v24.0.5-orange)
![](https://img.shields.io/badge/flake8--black-v0.3.6-purple)

![](https://img.shields.io/badge/pytest-v8.0.0-black)
![](https://img.shields.io/badge/coverage-97%25-brightgreen)

# Elevator Prediction System

## Overview
This project aims to model an elevator system and collect data that can later be used to build a prediction engine for
determining the best floor for the elevator to rest on. The prediction engine can be based on historical demand data,
providing insights into the likely next floor the elevator will be called from. While the primary focus is on building a
foundation for data collection and storage, the system is designed to lay the groundwork for future machine 
learning applications.

## Project Structure
The project consists of several components, each serving a specific purpose:

### API Module
* Core module containing the main application.
* Provides endpoints for health checks, data generation, elevator calls, data retrieval, updates, deletions, and CSV 
exports.
* Utilizes Flask and interacts with an SQLite database.

### Docker Configuration
* Contains files for Docker image configuration.
* Specifies the Dockerfile with the base image, working directory, and essential setup commands.
* Includes the docker-compose.yml file defining container configurations.

### Source Module
* Core functionality for database interaction and elevator-related operations.
* Abstract interface defining methods for connecting to and closing the database.
* Context manager handling database connections.
* SQLite database with methods for table creation, data insertion, and updates.
* Methods for calling the elevator and interacting with the database.

## Functionality and Endpoints
### ![](https://img.shields.io/badge/GET-blue) Health Check
* **Endpoint**: `/health`
* **Description**: Checks the health of the API.

### ![](https://img.shields.io/badge/GET-blue) Generate Data
* **Endpoint**: `/generate-data`
* **Description**: Generates data for the database using the DataGenerator.

### ![](https://img.shields.io/badge/POST-green) Call Elevator
* **Endpoint**: `/call-elevator`
* **Description**: Calls the elevator from a given floor. Requires parameters `demand_floor` and `destination_floor`.

### ![](https://img.shields.io/badge/GET-blue) Get All Rows
* **Endpoint**: `/get-all-rows`
* **Description**: Retrieves all rows from the database.

###  ![](https://img.shields.io/badge/PUT-yellow) Update Row
* **Endpoint**: `/update-row`
* **Description**: Updates the values of a row in the database. Requires a JSON object with an `id` field and one or 
more fields from: `current_floor`, `demand_floor`, `destination_floor`.

### ![](https://img.shields.io/badge/DELETE-red) Delete All Rows
* **Endpoint**: `/delete-all-rows`
* **Description**: Deletes all rows from the database.

### ![](https://img.shields.io/badge/GET-blue) Export CSV
* **Endpoint**: `/export-csv`
* **Description**: Exports the data from the database into a `CSV` file.

## Database Configuration
The system utilizes SQLite as the database backend. The `ElevatorDatabase` class in `elevator_database.py` provides 
methods for creating tables, inserting calls, updating rows, fetching data, and more.

## Docker Configuration
The Docker setup includes a Dockerfile specifying the Python environment and dependencies required for the project.
The docker-compose.yml file orchestrates the services, ensuring the application runs smoothly in a containerized environment.

## How To Run
Requirements:
* [Git](https://git-scm.com/downloads)
* [Docker](https://www.docker.com/)

1. Clone the repository  
`https://github.com/salatiel6/devtest.git`


2. Open the challenge directory  
Widows/Linux:`cd devtest`  
Mac: `open devtest`


3. Build docker image  
`docker-compose build`


4. Start docker container  
`docker-compose up`

## Conclusion
This project lays the groundwork for a more comprehensive elevator prediction system. The Flask API, coupled with an 
SQLite database, provides a scalable foundation for collecting and storing data. Future iterations may involve 
incorporating machine learning models for predictive analysis based on historical demand patterns.
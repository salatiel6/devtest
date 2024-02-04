![](https://img.shields.io/badge/python-v3.11-blue)
![](https://img.shields.io/badge/Flask-v3.0.1-pink)
![](https://img.shields.io/badge/Docker-v24.0.5-orange)
![](https://img.shields.io/badge/flake8--black-v0.3.6-purple)

![](https://img.shields.io/badge/pytest-v8.0.0-black)
![](https://img.shields.io/badge/coverage-97%25-brightgreen)

# Elevator Prediction System

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Functionality and Endpoints](#functionality-and-endpoints)
- [Database Configuration](#database-configuration)
- [Docker Configuration](#docker-configuration)
- [How To Run](#how-to-run)
- [Conclusion](#conclusion)

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

1. Clone the repository:  
`git clone https://github.com/salatiel6/devtest.git`


2. Open the challenge directory:  
Widows/Linux: `cd devtest`  
Mac: `open devtest`


3. Build docker image:  
`docker-compose build`


4. Start docker container:  
`docker-compose up`

## Reporting For Prediction
The generated CSV file serves as a comprehensive report capturing all elevator calls and movements, offering valuable
insights that can significantly enhance the elevator prediction system. Here's how the collected data can aid the
prediction model:

### Historical Demand Analysis
* The CSV file contains a detailed record of every elevator demand, including the originating floor and the desired
destination.
* Analyzing historical demand patterns helps identify peak usage times, popular floors, and recurring travel routes.

### Optimal Resting Floor Identification
* By examining which floors are frequently called, the prediction engine can determine the optimal resting floor for
the elevator during idle periods.
* This data aids in predicting where the elevator is most likely to be requested next, optimizing its position for
quicker response times.

### Traffic Flow Patterns
* Understanding the traffic flow between floors over time enables the prediction model to adapt to changing usage
patterns.
* Recognizing trends in user movement facilitates more accurate predictions, ensuring the elevator is positioned
strategically.

### Peak Usage Hours
* Analysis of call frequency during different hours of the day helps identify peak usage times.
* The prediction system can adjust its strategy based on anticipated demand during specific periods, ensuring
efficient elevator allocation.


### Enhanced User Experience
* Leveraging historical data enables the prediction engine to make informed decisions, leading to improved user
experiences.
* Users are more likely to experience reduced wait times and faster elevator arrivals as the system learns and adapts
to usage patterns.

### Data-Driven Predictive Models
* The collected data serves as a foundation for developing data-driven predictive models.
* Machine learning algorithms can be trained on this dataset to create a predictive model that anticipates future
* elevator demands and optimizes the elevator's resting position.

The generated CSV file acts as a powerful tool for understanding elevator usage patterns, allowing for the development
of a robust prediction engine. By leveraging historical data, the elevator system can adapt to user behavior,
providing a more efficient and responsive service.


## Conclusion
This project lays the groundwork for a more comprehensive elevator prediction system. The Flask API, coupled with an 
SQLite database, provides a scalable foundation for collecting and storing data. Future iterations may involve 
incorporating machine learning models for predictive analysis based on historical demand patterns.

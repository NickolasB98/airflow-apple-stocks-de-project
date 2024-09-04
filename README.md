# Stock Market Data Pipeline

Welcome to the Stock Market Data Pipeline project! This project is designed to automate the process of fetching, processing, and storing stock market data using Apache Airflow. The central component of this pipeline is the stock_market.py file, which defines a Directed Acyclic Graph (DAG) that orchestrates various tasks involved in the data workflow.

## Overview

In this project, I aim to gather stock prices for a specified symbol (currently set to 'AAPL') and store the data in a PostgreSQL database. The pipeline is structured to ensure that each step is executed in a logical sequence, with built-in checks to ensure data integrity and availability.

## Project Architecture

<img width="969" alt="image" src="https://github.com/user-attachments/assets/11268523-2e56-465b-83b9-be0b07b0852f">

## Key Features

**Data Fetching:** The pipeline checks the availability of the stock API before attempting to fetch data. This ensures that we only proceed when the API is ready to respond.
**Data Processing:** Once the data is fetched, it is processed and formatted using a Docker container running a Spark application. This allows for efficient handling of large datasets.
**Data Storage:** The processed data is then stored in a PostgreSQL database, making it easily accessible for further analysis and reporting.
**Notifications:** The pipeline integrates with Slack to send notifications upon successful completion of the DAG, keeping stakeholders informed about the status of the data pipeline.

## DAG Structure

The stock_market.py file contains the following key tasks:

1. is_api_available: A sensor task that checks if the stock API is available for data fetching.
2. get_stock_prices: A PythonOperator that retrieves stock prices from the API.
3. store_prices: A PythonOperator that stores the fetched prices for further processing.
4. format_prices: A DockerOperator that formats the data using a Spark application.
5. get_formatted_csv: A PythonOperator that retrieves the formatted data from MinIO.
6. load_to_dw: A task that loads the final data into a PostgreSQL database.
   
## Getting Started

To get started with this project, ensure you have Apache Airflow set up in your environment. Clone this repository and configure the necessary connections for the stock API and PostgreSQL database. You can then trigger the DAG from the Airflow UI to see the pipeline in action! Do not forget to run Airflow with the
Astro CLI using the docker-compose.override.yml instead of Dockerfile!

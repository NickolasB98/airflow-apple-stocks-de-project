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

The stock_market.py file defines a comprehensive Directed Acyclic Graph (DAG) that orchestrates the various tasks involved in the stock market data pipeline. Each task is designed to perform a specific function, ensuring a smooth and efficient workflow. Below are the key tasks included in the DAG:

**1. is_api_available:**
Type: Sensor Task
Description: This task continuously checks the availability of the stock API before any data fetching occurs. It ensures that the API is responsive and ready to provide data, preventing unnecessary failures in subsequent tasks. If the API is not available, this task will keep polling until it becomes accessible.

**2. get_stock_prices:**
Type: PythonOperator
Description: Once the API is confirmed to be available, this task retrieves the latest stock prices for a specified symbol (e.g., 'AAPL'). It makes an API call and processes the response to extract relevant price data. This task is crucial for gathering the raw data needed for further analysis.

**3. store_prices:**
Type: PythonOperator
Description: After fetching the stock prices, this task stores the retrieved data in a temporary location for further processing. It ensures that the data is organized and accessible for the next steps in the pipeline. This task may involve data validation and transformation to ensure consistency.

**4. format_prices:**
Type: DockerOperator
Description: This task utilizes a Docker container running a Spark application to format the fetched stock prices. The formatting process may include cleaning the data, converting it into a structured format (e.g., CSV), and performing any necessary aggregations or calculations. This step is essential for preparing the data for storage and analysis.

**5. get_formatted_csv:**
Type: PythonOperator
Description: After the data has been formatted, this task retrieves the processed CSV file from MinIO, a cloud-native object storage service. This step ensures that the formatted data is accessible for loading into the final database. It may also involve error handling to manage any issues in retrieving the file.

**6. load_to_dw:**
Type: PythonOperator
Description: The final task in the DAG loads the formatted data into a PostgreSQL database, making it available for querying and analysis. This task establishes a connection to the database and executes the necessary SQL commands to insert the data. It is a critical step for ensuring that the data pipeline delivers usable insights.
   
## Getting Started

To get started with this project, ensure you have Apache Airflow set up in your environment. Clone this repository and configure the necessary connections for the stock API and PostgreSQL database. You can then trigger the DAG from the Airflow UI to see the pipeline in action! Do not forget to run Airflow with the
Astro CLI using the docker-compose.override.yml instead of Dockerfile!

# Airflow Apple Stocks Data Engineering Project

## Project Background

This project automates the process of fetching, processing, and storing stock market data for Apple Inc. (AAPL) using Apache Airflow. The pipeline fetches stock prices from an API, processes the data using Spark, and stores it in a PostgreSQL database. The processed data is then visualized using Metabase for insights and reporting.

## Key Business Metrics

* **Dataset:** Apple Inc. (AAPL) stock prices.
* **Data Sources:** Stock market API.
* **Business Goal:** Provide actionable insights into stock price trends and enable data-driven decision-making.

## Data Structure & Initial Checks

The dataset consists of the following fields:

**Source Data:**

* Date: The date of the stock price.
* Open: The opening price of the stock.
* High: The highest price of the stock during the day.
* Low: The lowest price of the stock during the day.
* Close: The closing price of the stock.
* Volume: The trading volume of the stock.

**Destination:**

* PostgreSQL Database: For storing processed stock data.
* Metabase: For visualizing insights and generating reports.

**Executive Summary**

**Overview of Findings**

This project successfully implemented a fully automated data pipeline to fetch, process, and analyze Apple Inc. stock prices. Key findings include:

* **Data Integration:** Seamless ingestion of stock data from the API into the pipeline.
* **Data Transformation:** Efficient processing of raw data using Spark.
* **Centralized Storage:** Loading of processed data into PostgreSQL for analysis.
* **Visualization:** Insights were visualized using Metabase.

<img width="1070" alt="image" src="https://github.com/user-attachments/assets/738d488a-5943-4cf2-a4ae-e74f202ccf84">

**Insights Deep Dive**

**Category 1: Overall Stock Performance**

**Main Insight 1: Average Closing Price**

* **Finding:** The average closing price for AAPL stock is $189.44.
* **Supporting Data:** The dashboard prominently displays this numerical value.
* **Implication:** This provides a general understanding of the stock's overall price level during the observed period.

**Main Insight 2: Average Trading Volume**

* **Finding:** The average trading volume for AAPL stock is 60,175,507.83 shares.
* **Supporting Data:** The dashboard prominently displays this numerical value.
* **Implication:** This indicates the average level of market activity and liquidity for AAPL stock.

**Category 2: Stock Trends Over Time**

**Main Insight 1: Closing Price Trend**

* **Finding:** The closing price of AAPL stock shows fluctuations over time, with a general upward trend towards the later part of the observed period.
* **Supporting Data:** The "Stock Volume and Closing Prices Over Time" graph shows the closing price (blue line) increasing over time, with some variations.
* **Implication:** This suggests potential growth and positive market sentiment for AAPL stock in the later part of the period.

**Main Insight 2: Trading Volume Trend**

* **Finding:** The trading volume of AAPL stock exhibits significant spikes and variations over time, indicating periods of increased market activity.
* **Supporting Data:** The "Stock Volume and Closing Prices Over Time" graph shows the trading volume (light blue bars) with noticeable spikes and changes in volume.
* **Implication:** This suggests that there were specific events or news that triggered higher trading activity for AAPL stock.

**Main Insight 3: Correlation Between Volume and Price**

* **Finding:** There appears to be some correlation between spikes in trading volume and fluctuations in the closing price.
* **Supporting Data:** By comparing the closing price line and the volume bars, we can observe that some price changes coincide with volume spikes.
* **Implication:** This suggests that trading volume can influence or be influenced by price movements, indicating potential market reactions to specific events.

**Recommendations**

Based on the insights above, we recommend the following actions:

* **Market Monitoring:** Continuously monitor stock price trends and trading volumes to identify investment opportunities.
* **Event-Driven Strategies:** Develop strategies to capitalize on high trading volume days, such as earnings announcements.
* **Long-Term Investment:** Consider long-term investment in Apple Inc. stock, given its consistent growth trend.

**Assumptions and Caveats**

* **Assumption 1:** Data from the stock market API is accurate and up-to-date.
* **Assumption 2:** The data reflects only Apple Inc. stock and may not be applicable to other stocks.
* **Assumption 3:** Market conditions and external factors may impact stock prices unpredictably.

**Tools and Technologies Used**

* **Data Orchestration:** Apache Airflow
* **Data Processing:** Apache Spark
* **Data Storage:** PostgreSQL
* **Visualization:** Metabase
* **Containerization:** Docker

**Solution Architecture**

**Overview**

The architecture involves:

* **Data Ingestion:** Fetching stock data from the API using Airflow.
* **Data Transformation:** Processing data using Spark within a Docker container.
* **Data Loading:** Storing processed data in PostgreSQL.
* **Visualization:** Creating interactive dashboards in Metabase.

<img width="969" alt="image" src="https://github.com/user-attachments/assets/11268523-2e56-465b-83b9-be0b07b0852f">

**Project Execution Flow**

* **Data Ingestion:** Airflow fetches stock data from the API.
* **Data Transformation:** Spark processes the raw data within a Docker container.
* **Data Loading:** Processed data is stored in PostgreSQL.
* **Visualization:** Insights are visualized using Metabase.

**DAG Structure**

The `stock_market.py` file defines a Directed Acyclic Graph (DAG) that orchestrates the following tasks:

* **`is_api_available`:**
    * Type: Sensor Task
    * Description: Checks the availability of the stock API before fetching data.
* **`get_stock_prices`:**
    * Type: PythonOperator
    * Description: Fetches the latest stock prices for Apple Inc. (AAPL).
* **`store_prices`:**
    * Type: PythonOperator
    * Description: Stores the fetched data in a temporary location.
* **`format_prices`:**
    * Type: DockerOperator
    * Description: Formats the data using Spark within a Docker container.
* **`get_formatted_csv`:**
    * Type: PythonOperator
    * Description: Retrieves the formatted CSV file from MinIO.
* **`load_to_dw`:**
    * Type: PythonOperator
    * Description: Loads the formatted data into PostgreSQL.


**Getting Started**

To get started with this project:

1.  Ensure you have Apache Airflow set up in your environment.
2.  Clone this repository.
3.  Configure the necessary connections for the stock API and PostgreSQL database.
4.  Trigger the DAG from the Airflow UI to see the pipeline in action.

**Note:** Run Airflow with the Astro CLI using the `docker-compose.override.yml` file instead of the `Dockerfile`.

# Automated ETL Pipeline for Real-Time Weather Data of Coldest Cities in the USA Using AWS and Snowflake

This project showcases a highly automated ETL (Extract, Transform, Load) pipeline designed for collecting, processing, and analyzing real-time weather data from the coldest cities in the USA. The architecture leverages AWS services and Snowflake to gather weather metrics at hourly intervals, ensuring the data is structured and stored efficiently for analysis.
![WeatherAPI_pipeline_diagram](https://github.com/user-attachments/assets/391bb923-8e38-4685-98cc-a13c55e48697)


## Pipeline Overview
### 1. Data Collection and Scheduling:

**Weather Data API:** The pipeline pulls data for specific weather metrics such as temperature, wind speed, wind direction, pressure, and humidity for various cities across the USA. Key parameters captured include:

**-temp_c:** Temperature in Celsius

**-wind_mph:** Wind speed in miles per hour

**-wind_dir:** Wind direction

**-pressure_mb:** Atmospheric pressure in millibars

**-humidity:** Humidity level as a percentage

**AWS EventBridge:** To automate data collection, EventBridge triggers the pipeline every hour, ensuring the latest weather information is continuously ingested.

### 2. Data Extraction and Storage:

**AWS Lambda:** Triggered by EventBridge, a Lambda function calls the Weather API, retrieves the weather metrics listed above, and structures the data for consistent downstream processing.

**Amazon DynamoDB:** The structured weather data, including fields like City, State, temp_c, wind_mph, wind_dir, pressure_mb, and humidity, is stored in a DynamoDB table. DynamoDB serves as the initial storage layer, providing efficient and scalable access to the data.

### 3. Data Streaming and Transformation:

**DynamoDB Streams:** Each time new data is ingested into the DynamoDB table, a stream event triggers, activating a Lambda function.

**AWS Lambda for S3 Storage:** This Lambda function processes the streamed data and stores it in Amazon S3 in CSV format. Each file contains weather records for individual cities, ensuring that city-specific data is easily accessible for downstream analysis. The data is organized within folders in S3, making it simple to retrieve and analyze city-level weather information as needed.

### 4. Long-Term Storage and Integration:

**Amazon S3:** The formatted CSV data is stored in S3 with folders for each state (e.g., “Alaska,” “Montana”), containing city specific weather data. This partitioned structure allows for organized, efficient data retrieval and integrates seamlessly with Snowflake.

**AWS SQS Notifications:** Upon new file uploads to S3, SQS triggers notifications to ensure Snowflake initiates data loading. This event-driven process ensures data is transferred promptly to the data warehouse.

### 5. Data Warehousing and Analytics:

**Snowflake:** Snowflake’s external staging feature is configured to connect to the S3 bucket, loading the CSV data into Snowflake tables. The data fields like City, State, temp_c, wind_mph, wind_dir, pressure_mb, and humidity are mapped into Snowflake, making the data ready for queries and analysis.

## Key Benefits

**Automated Processing:** AWS EventBridge and DynamoDB Streams, in combination with Lambda functions, provide fully automated data ingestion and transformation every hour.

**Efficient Data Partitioning:** S3 organizes data by state, optimizing access and analysis within Snowflake.

**Scalability and Cost-Effectiveness:** The serverless architecture supports scaling as data volumes increase, while controlling costs.

**Data Quality Assurance:** Consistent formatting and field mapping ensure data is structured and accurate across services, ready for use in analytical and reporting tools.

**This ETL pipeline offers a reliable, scalable solution for real-time weather data processing, utilizing AWS and Snowflake to monitor weather conditions in the coldest cities across the USA.**

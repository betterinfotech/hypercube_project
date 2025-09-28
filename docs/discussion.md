# Discussion

---

### 1. How would you do this in a production cloud environment ?
- With a Docker container I would consider pushing an image to ECS Fargate.
- If Fargate is too costly, you can run Docker on an EC2 instance but must consider maintenance costs.
- Use S3 to store the JSON/CSV files.
- Use a more heavy-weight DB than just SQLite.
- Consider transmitting progress/metrics of the ETL pipeline for observation (e.g. Prometheus) 

### 2. How would your solution change if the data inputs were to be received in the form of streamed messages?
- Consider use of a message bus (e.g. RabbitMQ)
- Awareness of out-of-order data
- 'Exactly-once' processing

### 3. How would your solution change if the data was 100x the scale?
- Standalone Pandas or Polars might not be sufficient.  Consider a move to distributed ETL solution (e.g. Apache Spark).

### 4. What kind of architecture and approach would you use to serve this data for dashboards and reporting, used by multiple teams with differing requirements?
- Consider a centralised data warehouse
- Serious tooling like Power BI, Tableau etc
- Overnight rollup, materialized views
- APIs to expose data
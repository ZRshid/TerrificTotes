# create a google calendar - 
# project planning , we use Trello 
# create a a detailed project plan 
# create tickets using the project plan (create deadlines for our selfes.)

## WEEK 1
1. CICD 
2. A job scheduler
3. Orchestration process to run the ingestion job and subsequent processes.
4. An S3 bucket that will act as a "landing zone" for ingested data.
5. A Python application to check for changes to the database tables and ingest any new or updated data. 
6. A Cloudwatch alert should be generated in the event of a major error 

## WEEK 2 
7. A second S3 bucket for "processed" data.
8. A Python application to transform data landing in the "ingestion" S3 bucket and place the results in the "processed" S3 bucket. 
    - The data should be transformed to conform to the warehouse schema (see above). 
    -  The job should be triggered by either an S3 event triggered when data lands in the ingestion bucket, or on a schedule. 
    - Again, status and errors should be logged to Cloudwatch, and an alert triggered if a serious error occurs.
9. A Python application that will periodically schedule an update of the data warehouse from the data in S3. 
    - Again, status and errors should be logged to Cloudwatch, 
    - An alert triggered if a serious error occurs.

## WEEK 3
10. Data visualisation 
   - In practice, this will mean creating SQL queries to answer common business questions. Depending on the complexity of your visualisation tool, other coding may be required too.


## TOOLS
- Github
- Github Actions
- Makefile 
- Requirements 
- Scheduler: Lambda + step fuctions / Eventbridge
- S3 bucket 
- Terraform 
- Pandas ? 
- Cloudwatch 
- boto3 
- moto
- postgres
- pg8000
- EC2? 
- AIM 
- IAM 
- pytest
- Look for tools for testing 
- Black or bandit 


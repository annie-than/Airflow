Data Pipelines with Airflow
============================

Purpose
-------
A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.

The purpose of this project is to create high grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills. Besides, the data quality plays a big part when analyses are executed on top the data warehouse and want to run tests against their datasets after the ETL steps have been executed to catch any discrepancies in the datasets.


Datasets
--------
The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to. Here are the s3 links for each:

	- Log data: s3://udacity-dend/log_data
	- Song data: s3://udacity-dend/song_data


Project Template
----------------
The project template package contains three major components for the project:

	- DAG with default parameter:
	 	The DAG does not have dependencies on past runs
	  	On failure, the task are retried 3 times
 	  	Retries happen every 5 minutes
 	  	Catchup is turned off
	  	Do not email on retry	

	- Helper class for the SQL transformations

	- Operators: perform tasks such as staging the data, filling the data warehouse, and running checks on the data as the final step:
	  + Stage Operator:
        	The stage operator is expected to be able to load any JSON formatted files from S3 to Amazon Redshift. 
	        The operator creates and runs a SQL COPY statement based on the parameters provided. 
	        The operator's parameters should specify where in S3 the file is loaded and what is the target table. The parameters should be used to distinguish between JSON file. 
	 	Another important requirement of the stage operator is containing a templated field that allows it to load timestamped files from S3 based on the execution time and run backfills.

	  + Fact and Dimension Operators:
	 	Utilize the provided SQL helper class to run data transformations. 
	 	The operator is expected to take as input a SQL statement and target database on which to run the query against. 
	 	
	  + Data Quality Operator:
 		Run checks on the data. 
	 	The operator's main functionality is to receive one or more SQL based test cases along with the expected results and execute the tests. For each the test, the test result and expected result needs to be checked and if there is no match, the operator should raise an exception and the task should retry and fail eventually.



Build Instructions
-----------------
After you have updated the DAG, you will need to run /opt/airflow/start.sh command to start the Airflow webserver. Wait for the Airflow web server to be ready and then access the Airflow UI by clicking on the blue "Access Airflow" button.






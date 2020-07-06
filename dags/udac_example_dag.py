from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries


default_args = {
    'owner': 'udacity',
    'start_date': datetime(2019, 1, 12),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup_by_default': False,
    'email_on_retry': False
}


dag = DAG('udac_example_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='0 * * * *',
          catchup = False
        )

# Starting of DAG
start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)


# Create staging_events, staging_songs, songplays, users, song, artists, time tables on Redshift
create_tables_task = PostgresOperator(
    task_id = "create_tables",
    dag = dag,
    sql = 'create_tables.sql',
    postgres_conn_id = "redshift"
)


# Copy log_data from S3 to staging_events table on Redshift
stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    provide_context = True,
    dag=dag,
    table = "staging_events",
    s3_path = "s3://udacity-dend/log_data",
    redshift_conn_id = "redshift",
    aws_conn_id = "aws_credentials",
    region = "us-west-2",
    data_format = "s3://udacity-dungthan/jsonpaths.json"          
)


# Copy song_data from S3 to staging_songs table on Redshift
stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',    
    dag=dag,
    provide_context = True,
    table = "staging_songs",
    s3_path = "s3://udacity-dend/song_data",
    redshift_conn_id = "redshift",
    aws_conn_id = "aws_credentials",
    region = "us-west-2",    
    data_format = "auto"        
)


# From staging_events and staging_songs, loading data to songplays table on Redshift
load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    redshift_conn_id = "redshift",
    table = "songplays",
    sql = SqlQueries.songplay_table_insert
)


# From staging_events, loading data to users table on Redshift
load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    redshift_conn_id = "redshift",
    table = "users",
    sql = SqlQueries.user_table_insert
)


# From staging_songs, loading data to songs table on Redshift
load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    redshift_conn_id = "redshift",
    table = "songs",
    sql = SqlQueries.song_table_insert
)


# From staging_songs, loading data to artists table on Redshift
load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    redshift_conn_id = "redshift",
    table = "artists",
    sql =  SqlQueries.artist_table_insert
)


# From staging_events, loading data to time table on Redshift
load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    redshift_conn_id = "redshift",
    table = "time",
    sql = SqlQueries.time_table_insert
)


# Checking if there is records on tables
run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id = "redshift",
    tables = ["songplays", "users", "songs", "artists", "time"]
)

# Ending of DAG
end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)


# Orders of operator
start_operator >> create_tables_task

create_tables_task >>  stage_events_to_redshift >> load_songplays_table
create_tables_task >>  stage_songs_to_redshift >> load_songplays_table

load_songplays_table >> load_song_dimension_table >> run_quality_checks
load_songplays_table >> load_user_dimension_table >> run_quality_checks
load_songplays_table >> load_artist_dimension_table >> run_quality_checks
load_songplays_table >> load_time_dimension_table >> run_quality_checks

run_quality_checks >> end_operator




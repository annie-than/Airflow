from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from helpers import SqlQueries

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,               
                 redshift_conn_id = "",
                 table = "",
                 sql = "",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)       
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql = sql

    def execute(self, context):
        #self.log.info('LoadFactOperator not implemented yet')
        redshift = PostgresHook(postgres_conn_id = self.redshift_conn_id)
        self.log.info(f"Start loading fact table {self.table}")
        insert_sql = f"INSERT INTO public.{self.table}(start_time, userid, level, song_id, artist_id, sessionid, location, useragent) {self.sql}"
        redshift.run(insert_sql)       
                      
                      

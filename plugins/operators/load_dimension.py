from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,                 
                 redshift_conn_id = "",
                 table = "",
                 sql = "",                 
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)    
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql = sql        

    def execute(self, context):        
        redshift = PostgresHook(postgres_conn_id = self.redshift_conn_id)
        self.log.info(f"Start loading dimension table {self.table}")
        insert_sql = f"INSERT INTO public.{self.table} {self.sql}"
        redshift.run(insert_sql)

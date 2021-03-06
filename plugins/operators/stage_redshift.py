from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    
    ui_color = '#358140'
    
    copy_sql = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        REGION '{}'
        FORMAT AS JSON  '{}'       
        
    """        
       

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 # Example:
                 # redshift_conn_id=your-connection-name
                 redshift_conn_id = "",
                 aws_conn_id = "",
                 table = "",
                 s3_path = "",   
                 region = "",
                 data_format = "",              
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id
        self.redshift_conn_id = redshift_conn_id
        self.aws_conn_id = aws_conn_id
        self.table = table
        self.s3_path = s3_path
        self.region = region
        self.data_format = data_format
        
        

    def execute(self, context):
        #self.log.info('StageToRedshiftOperator not implemented yet')
        aws_hook = AwsHook(self.aws_conn_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id = self.redshift_conn_id)
        
        self.log.info("Clearing data from destination Redshift table")
        redshift.run("DELETE FROM {}".format(self.table))
        
        self.log.info("Copying data from S3 to Redshift")       
        formatted_sql = StageToRedshiftOperator.copy_sql.format(
            self.table,
            self.s3_path,
            credentials.access_key,
            credentials.secret_key,
            self.region,
            self.data_format            
        )
        redshift.run(formatted_sql)
         
            






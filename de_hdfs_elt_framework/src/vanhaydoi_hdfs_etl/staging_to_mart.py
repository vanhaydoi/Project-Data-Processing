from pyspark.sql import SparkSession

class StagingToMart:

    def __init__(self,
                app_name: str = "staging_to_mart",
                staging_path: str = "hdfs://namenode:9000/datalake/staging/",
                mart_path: str = "hdfs://namenode:9000/datalake/mart/"):
        self.spark = SparkSession.builder.appName(app_name).getOrCreate()
        self.staging_path = staging_path
        self.mart_path = mart_path
        self.df_staging = None
        self.df_mart = None

    def read_data(self):
        self.df_staging = self.spark.read.parquet(self.staging_path)
    
    def process_data(self):
        self.df_mart = self.df_staging
    
    def write_data(self):
        self.df_mart.write.mode("append").parquet(self.mart_path)
    
    def run(self,
            staging_path: str = None,
            mart_path: str = None):
        if staging_path:
            self.staging_path = staging_path
        if mart_path:
            self.mart_path = mart_path

        self.read_data()
        self.process_data()
        self.write_data()

mart_etl = StagingToMart(
    staging_path="hdfs://namenode:9000/datalake/staging/",
    mart_path="hdfs://namenode:9000/datalake/mart/"
)
mart_etl.run()
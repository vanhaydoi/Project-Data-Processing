from pyspark.sql import SparkSession
from pyspark.sql.functions import col

class RawToStaging:

    def __init__(self,
                 app_name: str = "raw_to_staging",
                 kafka_path: str = "hdfs://namenode:9000/datalake/raw/kafka_data/",
                 batch_path: str = "hdfs://namenode:9000/datalake/raw/batch_data",
                 staging_path: str = "hdfs://namenode:9000/datalake/staging/"):
        self.spark = SparkSession.builder.appName(app_name).getOrCreate()
        self.kafka_path = kafka_path
        self.batch_path = batch_path
        self.staging_path = staging_path
        self.df_kafka = None
        self.df_batch = None
        self.df_all = None
        self.df_clean = None
    
    def read_data(self):
        self.df_batch = self.spark.read.parquet(self.batch_path)
        self.df_kafka = self.spark.read.parquet(self.kafka_path)

    def process_data(self):
        # Chèn logic xử lý dữ liệu tùy chỉnh (nếu cần).
        pass

    def union_data(self):
        # Gộp 2 DataFrame theo schema (unionByName).
        self.df_all = self.df_kafka.unionByName(self.df_batch)

    def clean_data(self):
        # Loại bỏ bản ghi trùng và id null.
        self.df_clean = (
            self.df_all
            .dropDuplicates(["id"])
            .filter(col("id").isNotNull())
        )

    def write_data(self):
        # Ghi kết quả đã clean về HDFS dưới dạng parquet.
        self.df_clean.write.mode("append").parquet(self.staging_path)

    def run(self,
            kafka_path: str = None,
            batch_path: str = None,
            staging_path: str = None):
        if kafka_path:
            self.kafka_path = kafka_path
        if batch_path:
            self.batch_path = batch_path
        if staging_path:
            self.staging_path = staging_path

        self.read_data()
        self.process_data()
        self.union_data()
        self.clean_data()
        self.write_data()

# raw_etl = RawToStaging()
# raw_etl.run()
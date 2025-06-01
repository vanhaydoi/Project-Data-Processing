from pyspark.sql import functions as F
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructField, StructType, StringType, IntegerType, TimestampType

class JsonStreamingProcessor:

    def __init__(self, app_name: str = "ClickStreaming", 
                 kafka_bootstrap_servers: str = "kafka1:9092",
                 kafka_topic: str = "de-captions", 
                 hdfs_output_path: str = "hdfs://namenode:9000/datalake/raw/kafka_data",
                 hdfs_checkpoint_path: str = "hdfs://namenode:9000/checkpoints/kafka_data"
                 ):

        self.app_name = app_name
        self.spark = None
        self.kafka_topic = kafka_topic
        self.hdfs_output_path = hdfs_output_path
        self.hdfs_checkpoint_path = hdfs_checkpoint_path
        self.kafka_bootstrap_servers = kafka_bootstrap_servers

    # Khởi tạo SparkSession
    def create_spark_session(self):
        if not self.spark:
            self.spark = (
                SparkSession \
                .builder \
                .appName(self.app_name)
                .getOrCreate()
            )
        return self.spark
    
    # Tạo các schema
    def create_schema(self) -> StructField:
        self.schema = StructType([
            StructField("id", IntegerType(), True),
            StructField("filename", StringType(), True),
            StructField("content", StringType(), True),
            StructField("size", IntegerType(), True),
            StructField("type", StringType(), True),
            StructField("status", StringType(), True),
            StructField("created_at", TimestampType(), True),
            StructField("updated_at", TimestampType(), True)
        ])
        return self.schema

    # Lấy data từ kafka topic
    def read_stream(self):
        df_clickstream = (
            self.spark \
            .readStream \
            .option("kafka.bootstrap.servers", self.kafka_bootstrap_servers)
            .option("subscriber", self.kafka_topic)
            .load()
            .select(from_json(col("value").cast("string"), self.schema).alias("parsed_value"))
        )

        return df_clickstream.select("parsed_value.*").withColumnRenamed("timestamp\n", "timestamp")
    
    # Viết data vào hdfs
    def write_stream(self, df_clickstream):

        df_stream_hdfs = (
            df_clickstream \
            .writeStream \
            .outputMode("append") \
            .format("parquet") \
            .option("trucate", "false") \
            .option("path", self.hdfs_output_path)
            .option("checkpointLocation", self.hdfs_checkpoint_path)
            .trigger(processingTime="1 minute")
            .start()
        )

        return df_stream_hdfs
    
    # Chạy
    def start(self):
        df_clickstream = self.read_stream()
        df_stream_hdfs = self.write_stream(df_clickstream)
        df_stream_hdfs.awaitTermination()
    

# Ví dụ sử dụng
# streamer = JsonStreamingProcessor()
# streamer.start()

streamer = JsonStreamingProcessor()
streamer.start()
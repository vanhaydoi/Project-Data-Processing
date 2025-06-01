from hdfs.ext.kerberos import KerberosClient
import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from io import BytesIO
import json

class JsonBatchProcessor:

    def __init__(self, hdfs_output_dir: str, hdfs_url: str = "http://localhost:9870", hdfs_user: str ="hadoop"):

        self.client = KerberosClient(hdfs_url)
        self.hdfs_output_dir = hdfs_output_dir

    def read_json_files(self, folder_path: str) -> list:
        # Đọc tất cả file .json trong folder_path, trả về list các dict.
        records = []
        for fname in os.listdir(folder_path):
            if fname.lower().endswith(".json"):
                with open(os.path.join(folder_path, fname), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Kiểm tra xem data có thuộc dạng list hay không
                    if isinstance(data, list): 
                        records.extend(data)
                    else:
                        records.append(data)
        return records
    
    def json_to_parquet(self, records: list) -> BytesIO:
        # Chuyển list dict thành Parquet lưu vào BytesIO (in-memory).
        table = pa.Table.from_pylist(records)
        sink = pa.BufferOutputStream()
        pq.write_table(table, sink)
        buf = sink.getvalue().to_pybytes()
        return BytesIO(buf)
    
    def save_parquet_to_hdfs(self, buffer:BytesIO, hdfs_file_name: str) -> None:

        hdfs_path = os.path.join(self.hdfs_output_dir, hdfs_file_name)
        buffer.seek(0)
        self.client.write(hdfs_path, buffer, overwrite=True)

    
    
    def process_folder(self, folder_path: str, hdfs_file_name: str = 'data.parquet') -> None:
        
        # Toàn bộ pipeline: đọc JSON, tạo Parquet in-memory, upload lên HDFS.
        
        records = self.read_json_files(folder_path)
        parquet_buffer = self.json_to_parquet(records)
        self.save_parquet_to_hdfs(parquet_buffer, hdfs_file_name)

# Ví dụ sử dụng:
# converter = JsonBatchProcessor(
#     hdfs_output_dir='/datalake/raw/batch_data'
# )
# converter.process_folder('C:/Users/Admin/Desktop/BigData/Project_DE/Data/input/json', 'data.parquet')

converter = JsonBatchProcessor(
    hdfs_output_dir='/datalake/raw/batch_data'
)
converter.process_folder('C:/Users/Admin/Desktop/BigData/Project_DE/Data/input/json', 'data.parquet')
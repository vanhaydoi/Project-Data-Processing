# Real-Time & Batch Data Ingestion Platform
Nền tảng xử lý dữ liệu thời gian thực được thiết kế để thu thập, xử lý và phân tích dữ liệu từ nhiều nguồn khác nhau, bao gồm luồng streaming và batch processing. Framework này được phát triển dưới dạng các package riêng biệt và được publish lên PyPI để tái sử dụng dễ dàng.
# 🏗️ Kiến trúc hệ thống
![Kiến trúc hệ thống](./Data%20Processing.png)
# ✨ Tính năng chính
## 🌊 Streaming Data Processing
- Thu thập dữ liệu real-time từ Apache Kafka
- Xử lý JSON data với Apache Spark Streaming
- Ghi dữ liệu trực tiếp vào HDFS RAW zone
## 📦 Batch Data Processing
- Xử lý file JSON theo lịch trình định kỳ
- Tích hợp với Python batch jobs
- Hỗ trợ multiple data sources
## 🏭 ETL Pipeline
- Pipeline 3 tầng: RAW → STAGING → MART
- Data transformation và cleansing
- Schema normalization và data enrichment
- Partitioning theo ngày (partitioned by dt)
## 🎛️ Orchestration & Monitoring
- Quản lý workflow với Apache Airflow
- Lên lịch chạy định kỳ (daily/hourly)
- Data quality monitoring
- Job dependency management
# ⚙️ Công nghệ sử dụng
## Công nghệ sử dụng

| Công nghệ | Phiên bản | Mục đích |
|:-----------|:-----------|:----------|
| Apache Kafka | 2.8+ | Message streaming platform |
| Apache Spark | 3.3+ | Distributed data processing |
| Hadoop HDFS | 3.3+ | Distributed file storage |
| Apache Hive | 3.1+ | Data warehouse và SQL analytics |
| Apache Airflow | 2.5+ | Workflow orchestration |
| Python | 3.8+ | Batch processing scripts |
| Docker | 20.10+ | Containerization |
| Power BI | Latest | Business intelligence và visualization |
# 🚀 Cài đặt
- Python 3.8+
- Docker & Docker Compose
- Java 8/11 (cho Spark và Hadoop)
- Minimum 8GB RAM
- 50GB storage space
# Cài đặt từ PyPI
## Cài đặt các framework từ PyPI
pip install de-streaming-ingestion-framework \
pip install de-batch-ingestion-framework  \
pip install de-hdfs-elt-framework 
# 📁 Cấu trúc dự án
realtime-data-processing/ \
├── 📦 de_streaming_ingestion_framework/    # Streaming framework \
│   ├── src/ \
│   │   ├── streaming_ingestion.py \
│   │   └── __init__.py \
│   ├── setup.py \
│   ├── requirements.txt \
│   └── README.md \
│ \
├── 📦 de_batch_ingestion_framework/        # Batch processing framework  \
│   ├── src/ \
│   │   ├── json_processor.py \
│   │   └── __init__.py \
│   ├── setup.py \
│   ├── requirements.txt \
│   └── README.md \
│ \
├── 📦 de_hdfs_elt_framework/              # ETL framework \
│   ├── src/ \
│   │   ├── raw_to_staging.py \
│   │   ├── staging_to_mart.py \
│   │   └── __init__.py \
│   ├── setup.py \
│   ├── requirements.txt \
│   └── README.md \
│
├── 🎛️ de_dags/                           # Airflow orchestration \
│   ├── dags/ \
│   │   ├── main_pipeline.py \
│   │   ├── streaming_dag.py \
│   │   └── batch_dag.py \
│   ├── plugins/ \
│   ├── requirements.txt \
│   └── README.md \
│ \
├── 🐳 docker/                            # Docker configurations \
│   ├── airflow/ \
│   ├── jenkin/ \
│   ├── hadoop/ \
│   └── kafka/ \
│
├── 🧪 tests/                            # Test cases \
│   ├── unit/ \
│   ├── integration/ \
│   └── fixtures/ \
│
├── 📄 requirements.txt                  # Python dependencies \
└── 📖 README.md                        # Project documentation \
# 📞 Liên hệ 
- Maintainer: Vanhaydoi
- Email: nguyenduyvanhaydoi1512@gmail.com

from hdfs.ext.kerberos import KerberosClient
# Replace with your HDFS URL, typically http://<namenode-host>:50070 or :9870
client = KerberosClient('http://localhost:9870', session=False)
 
# List root directory
print(client.list('/'))
 
# client.makedirs("/data/haha")

client.upload("/data/haha/test.csv", 'test.csv')
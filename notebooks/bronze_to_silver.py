# Databricks notebook source
# DBTITLE 1,Cell 1
dbutils.fs.ls('abfss://bronze@projectadlsgen2demosk.dfs.core.windows.net/SalesLT/')

# COMMAND ----------

dbutils.fs.ls('abfss://silver@projectadlsgen2demosk.dfs.core.windows.net/')

# COMMAND ----------

input_path = 'abfss://bronze@projectadlsgen2demosk.dfs.core.windows.net/SalesLT/'

# COMMAND ----------

table_name = []

for i in dbutils.fs.ls(input_path):
  print(i.name)
  table_name.append(i.name.split('/')[0])

# COMMAND ----------

table_name

# COMMAND ----------

from pyspark.sql.functions import from_utc_timestamp, date_format
from pyspark.sql.types import TimestampType

for i in table_name:
  path = input_path + i + '/' + i + '.parquet'
  df = spark.read.format('parquet').load(path)
  column = df.columns

  for col in column:
    if "Date" in col or "date" in col:
      df = df.withColumn(col, date_format(from_utc_timestamp(df[col].cast(TimestampType()), "UTC"), "yyyy-MM-dd"))

  output_path = 'abfss://silver@projectadlsgen2demosk.dfs.core.windows.net/SalesLT/' +i +'/'
  df.write.format('delta').mode("overwrite").save(output_path)


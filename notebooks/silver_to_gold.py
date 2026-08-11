# Databricks notebook source
# DBTITLE 1,Cell 1
dbutils.fs.ls('abfss://silver@projectadlsgen2demosk.dfs.core.windows.net/SalesLT/')

# COMMAND ----------

dbutils.fs.ls('abfss://gold@projectadlsgen2demosk.dfs.core.windows.net/')

# COMMAND ----------

input_path = 'abfss://silver@projectadlsgen2demosk.dfs.core.windows.net/SalesLT/'

# COMMAND ----------

table_name = []

for i in dbutils.fs.ls(input_path):
  print(i.name)
  table_name.append(i.name.split('/')[0])

# COMMAND ----------

table_name

# COMMAND ----------

for name in table_name:
  path = input_path + name
  print(path)
  df = spark.read.format('delta').load(path)

  # Get the list of column names
  column_names = df.columns

  for old_col_name in column_names:
      # Convert column name from ColumnName to Column_Name format
      new_col_name = "".join(["_" + char if char.isupper() and not old_col_name[i - 1].isupper() else char for i, char in enumerate(old_col_name)]).lstrip("_")
      
      # Change the column name using withColumnRenamed and regexp_replace
      df = df.withColumnRenamed(old_col_name, new_col_name)

  output_path = 'abfss://gold@projectadlsgen2demosk.dfs.core.windows.net/SalesLT/' +name +'/'
  df.write.format('delta').mode("overwrite").save(output_path)


# Databricks notebook source
# Databricks notebook source
configs = {
  "fs.azure.account.auth.type": "CustomAccessToken",
  "fs.azure.account.custom.token.provider.class": spark.conf.get("spark.databricks.passthrough.adls.gen2.tokenProviderClassName")
}

# COMMAND ----------

# DBTITLE 1,Cell 2
# DBFS mounts are disabled on this workspace. Apply storage configs directly to the Spark session
# and access ADLS Gen2 using the abfss:// URI directly instead of /mnt/bronze.
for key, value in configs.items():
    spark.conf.set(key, value)

# Access data directly via abfss:// path, e.g.:
# df = spark.read.parquet("abfss://bronze@projectadlsgen2demosk.dfs.core.windows.net/<directory-name>")

# COMMAND ----------

# DBTITLE 1,List ADLS Gen2 container
# Configs from Cell 2 are already applied to the Spark session.
# dbutils.fs.ls() picks them up automatically — just pass the abfss:// URI.
display(dbutils.fs.ls("abfss://bronze@projectadlsgen2demosk.dfs.core.windows.net/"))

# COMMAND ----------

# DBTITLE 1,List SalesLT folder contents
# dbutils.fs.ls("abfss://bronze@projectadlsgen2demosk.dfs.core.windows.net/SalesLT/")
display(dbutils.fs.ls("abfss://bronze@projectadlsgen2demosk.dfs.core.windows.net/SalesLT/"))

# COMMAND ----------

# DBTITLE 1,Mount Bronze
# Bronze container
bronze_path = "abfss://bronze@projectadlsgen2demosk.dfs.core.windows.net/"
print(f"Bronze path: {bronze_path}")
display(dbutils.fs.ls(bronze_path))

# COMMAND ----------

# DBTITLE 1,Mount Silver
# Silver container
silver_path = "abfss://silver@projectadlsgen2demosk.dfs.core.windows.net/"
print(f"Silver path: {silver_path}")
display(dbutils.fs.ls(silver_path))

# COMMAND ----------

# DBTITLE 1,Mount Gold
# Gold container
gold_path = "abfss://gold@projectadlsgen2demosk.dfs.core.windows.net/"
print(f"Gold path: {gold_path}")
display(dbutils.fs.ls(gold_path))
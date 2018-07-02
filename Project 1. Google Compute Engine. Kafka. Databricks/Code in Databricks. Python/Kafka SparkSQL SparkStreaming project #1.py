# Databricks notebook source
# MAGIC %md # Streaming data from Kafka and analyzing realtime / Language:python

# COMMAND ----------

# MAGIC %md ## Creating connection with Kafka server on Google Compute Engine

# COMMAND ----------

import string
from pyspark.sql.functions import *

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "35.193.247.113:9092") \
  .option("subscribe", "ripple-api-v4") \
  .option("startingOffsets", "latest") \
  .load() \
  .selectExpr("CAST(value AS STRING)")
  
interm = df.select(get_json_object(df["value"],"$.payload").alias('value'))
res = interm.select(get_json_object(interm["value"],"$.time").cast("float").cast("timestamp").alias("time"),
		   get_json_object(interm["value"],"$.amount").cast("float").alias("amount"),
		   get_json_object(interm["value"],"$.currency").alias("currency"),
		   get_json_object(interm["value"],"$.t_hash").alias("t_hash"))

display(res)

# COMMAND ----------

# MAGIC %md ###Let's Add Static Dataframe with Countries and currency

# COMMAND ----------

from pyspark.sql import Row
arr_cur_countries = [('CNY','CHN'),('USD','USA'),('JPY','JPN'),('INR','IND')]
rdd = sc.parallelize(arr_cur_countries)
cur_countries = rdd.map(lambda x: Row(currency=x[0], country=x[1]))
schemaCurCountries = sqlContext.createDataFrame(cur_countries)

display(schemaCurCountries)

# COMMAND ----------

# MAGIC %md ## Stream Processing, adding 1 second "Window" to our Data
# MAGIC ## and join Streaming DataFrame with Static DataFrame

# COMMAND ----------

from pyspark.sql.functions import *

# Same query as staticInputDF
streamingCountsDF = (
  res
    .groupBy(
      res.t_hash, 
      res.currency, 
      res.amount, 
     window(res.time, "1 second"))
   .count()
)

#JOINING STREAMINGDATAFRAME WITH STATIC DATAFRAME
streamingCountsDF = streamingCountsDF.join(schemaCurCountries, "currency", "left")
display(streamingCountsDF)

# COMMAND ----------

# MAGIC %md #Lets store our dataframe in memory and do some Magic!

# COMMAND ----------

spark.conf.set("spark.sql.shuffle.partitions", "2")  # keep the size of shuffles small

query = (
  streamingCountsDF
    .writeStream
    .format("memory")        # memory = store in-memory table (for testing only in Spark 2.0)
    .queryName("counts")     # counts = name of the in-memory table
    .outputMode("complete")  # complete = all the counts should be in the table
    .start()
)

# COMMAND ----------

# MAGIC %md ###Show me the Relative amount each second!

# COMMAND ----------

# MAGIC %sql select date_format(window.end, "hh:mm:ss") as time, count, amount, currency from counts order by time

# COMMAND ----------

# MAGIC %md As we can see money is flowing over a period, streaming...

# COMMAND ----------

# MAGIC %sql select amount, currency, date_format(window.end, "hh:mm:ss") as time, count from counts order by time

# COMMAND ----------

# MAGIC %md That chart shows us that INDIA sends a lot of money in ONE transaction, we are using country variable from static dataframe

# COMMAND ----------

# MAGIC %sql select amount, country, date_format(window.end, "MMM-dd HH:mm:ss") as time from counts where country is not null order by time

# COMMAND ----------

# MAGIC %md ###Amount on packets coming each second...

# COMMAND ----------

# MAGIC %sql select currency, date_format(window.end, "MMM-dd HH:mm:ss") as time, count from counts order by time, currency

# COMMAND ----------

# MAGIC %md #Thank you!

# COMMAND ----------



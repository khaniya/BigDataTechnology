# *******Project #1
# Add external IP address for your server, so you can be sure that it's not going to change every day
# On the Google compute engine you have to open
# the ports of the machine and the ports in zookeeper itself
# check the advertised.listeners parameter and the rerun zookeper
# 1) Run the generator
# I'm running this script to run simulation and add the test data into the file,
# which will then will be pushed into the topic by file producer, you can find php script in the folder "Project 1. Kafka. Databricks/Kafka part/"

while true; do php generator.php;sleep 1;done&

# 2) Run the Kafka standalone script, for simplicity we are running in standalone mode
# you can find the configuration for kafka in the folder "Project 1. Kafka. Databricks/Kafka part"

bin/connect-standalone.sh config/connect-standalone.properties config/connect-file-source.properties 

# 3) Additionaly if you want to check all the ports on Google Compute Engine and zookeeper install and run Kafka-tool for windows.

# 4) Import the python Jupyter notebook "Kafka SparkSQL SparkStreaming project #1.ipynb" to Databricks,
#    you can find it in the folder "Project 1. Kafka. Databricks/Code in Databricks. Python/"
#    change the IP address in the notebook and also the topic name
#    you can find screenshots in each folder and also check the "Kafka SparkSQL SparkStreaming project #1.html" 
#    file in the folder "Project 1. Kafka. Databricks/Code in Databricks. Python/"
#
# 5) That's it, run the code in Databricks, it provides you with Python, SparkSQL, SparkStreaming from the box, also you can use Scala.



# ******Project #2
# 1) Set up the environment in cloudera hadoop (CDH)
# Requirements to set up the environment:
# cloudera quickstart vmware 5.12.0
# scala 2.11
# spark 2.2.0
# jdk 1.8

# 2) Spark SQl and HIVE
# The files is stored in Hive Table in snappy compression, parquet file format.
# We created some Hive table, wrote the SQL to get the interested data and load it into Impala tables (5 tables).
# After we visualize the data in Tableau pdf files can be found in the "Project 2. CDH Hive Impala Tableau/Output charts from Tableau in pdf/".
# Since Hive executes MapReduce jobs for most of the queries in Hive and making operation slow, 
# We used Impala instead. We can access all tables created in Impala in Hive.
# SQL Scripts can be found in "Project 2. CDH Hive Impala Tableau/SQL Scripts.txt"

# 3.Tableau for visualisation
# We have installed tableau in windows10. We connected tableau with cloudera hadoop virtual machine 
# using ClouderaImpala ODBC driver and cloudera's IP address (NAT mode is localhost).
# This links all the hive/impala tables to the tableau where can I join the tables,
# and play with statistic analysis and plot the charts.  
# one example of tableau file is in the project folder.
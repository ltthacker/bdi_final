from graphframes import *
from pyspark.sql import SQLContext
from pyspark import SparkContext

# Create DataFrames from HIVE query
v=SQLContext.sql("select  id, name, total_seconds from my_schema.nodes")
e=SQLContext.sql("select src, dst, relationship from my_schema.edges")

# Create DataFrames manually for testing purposes
v = SQLContext.createDataFrame([
    ("A", "ARON"  ,350 ),
    ("B", "BILL"  ,360 ),
    ("C", "CLAIR" ,195 ),
    ("D", "DANIEL",90),
    ("E", "ERIC"  ,90),
    ("F", "FRANK" ,215 ),
    ("G", "GRAHAM",30 ),
    ("H", "HENRY" ,25 ),
    ("I", "INNA"  ,25 ),
    ("J", "JEN"   ,20 )
], ["id", "name", "total_seconds"])

e=SQLContext.createDataFrame([
    ("A", "B", 60),
    ("B", "A", 50),
    ("A", "C", 50),
    ("C", "A", 100),
    ("A", "D", 90),
    ("C", "I", 25),
    ("C", "J", 20),
    ("B", "F", 50),
    ("F", "B", 110),
    ("F", "G", 30),
    ("F", "H", 25),
    ("B", "E", 90)
],["src","dst","relationship"])

# Now lets construct the graph
g = GraphFrame(v,e)
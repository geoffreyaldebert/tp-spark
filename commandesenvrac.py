### Les imports nécessaires
import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql.types import IntegerType
from pyspark.sql.window import Window



#### Lire un fichier csv
### pour hdfs, syntaxe : hdfs:///PATH/TO/DATA
df = spark.read\
.option("delimiter", ",")\
.option("header","true")\
.csv('file:/root/cours-spark/dump/large-table/1913377.csv', inferSchema=True)


# Lire une table Hive déjà existante
df = sqlContext.sql('select * from xxxx')

# Sauvegarder un dataframe dans un fichier csv
df.coalesce(1).write.csv('/data-lake/red/enrs/A_Var1', compression='gzip')
df.write.csv('/data-lake/red/enrs/A_Var1')

# Création de vues temporaires pouvant être utilisée par la suite (se détruit à la fermeture de la session Spark)
peopledf.createGlobalTempView("people")
df.createTempView("customer")
df.createOrReplaceTempView("customer")

# Permet de visualiser le contenu d'un dataframe
df.show()
# +-----+----+----+
# |   id|val1|val2|
# +-----+----+----+
# |64727|   3| 195|
# |64727|  37| 196|
# |64727|  93| 411|
# |64727|  97| 185|
# |64727|  84| 233|
# +-----+----+----+
# only showing top 5 rows

# Permet de visualiser les 10 premiers rows d'un DF
df.show(10)

# Permet de visualiser complètement les rows d'un DF
df.show(10, False)

# Permet de compter le nombre de ligne d'un DF
df.count()
# 50

# Permet d'afficher les types des différentes colonnes d'un DF
df.dtypes
# [('id', 'int'), ('val1', 'int'), ('val2', 'int')]

# Permet d'afficher le schéma d'un DF
df.schema
# StructType(List(StructField(id,IntegerType,true),StructField(val1,IntegerType,true),StructField(val2,IntegerType,true)))
df.printSchema()
# root
#  |-- id: integer (nullable = true)
#  |-- val1: integer (nullable = true)
#  |-- val2: integer (nullable = true)

# Information sur le DF
df.explain()
# == Physical Plan ==
# *(1) FileScan csv [id#298,val1#299,val2#300] 
# Batched: false, 
# Format: CSV, 
# Location: 
# InMemoryFileIndex[file:/root/cours-spark/dump/large-table/1913377.csv], 
# PartitionFilters: [], 
# PushedFilters: [], 
# ReadSchema: struct<id:int,val1:int,val2:int>


# Permet de forcer le type d'une colonne d'un DF (ici en float)
df.withColumn('val1', df['val1'].cast(T.FloatType()))
# [('id', 'int'), ('val1', 'float'), ('val2', 'int')]

# StringType
# BooleanType
# FloatType
# IntegerType
# DateType
# TimestampType

# https://spark.apache.org/docs/2.3.0/api/python/pyspark.sql.html#module-pyspark.sql.types



# Permet de décrire les différentes colonnes d'un DF avec certaines métriques communes (moy, min max count, écart type)
df.describe().show()
# +-------+------------------+------------------+------------------+
# |summary|                id|              val1|              val2|
# +-------+------------------+------------------+------------------+
# |  count|                50|                50|                50|
# |   mean|           57628.6|              55.5|            244.92|
# | stddev|21975.424368217908|33.290465632682526|139.21658944073513|
# |    min|             23158|                 0|                37|
# |    max|             82087|               100|               491|
# +-------+------------------+------------------+------------------+



df.sort(F.col('val1').desc()).show(5)

# Permet d'ordonner l'affichage d'un DF
df.orderBy(['col1', 'col2'], ascending=[True, False]).show(10)
# +-----+----+----+
# |   id|val1|val2|
# +-----+----+----+
# |42880| 100| 127|
# |82087|  99| 289|
# |75291|  99| 451|
# |64727|  97| 185|
# |82087|  97| 218|
# +-----+----+----+


## Permet de visualiser seulement une colonne spéfifique d'un DF
df.select('id').show(5)
# +-----+
# |   id|
# +-----+
# |64727|
# |64727|
# |64727|
# |64727|
# |64727|
# +-----+

# Permet de visualiser plusieurs colonnes d'un DF
df.select(['id', 'val1']).show(5)
# +-----+----+
# |   id|val1|
# +-----+----+
# |64727|   3|
# |64727|  37|
# |64727|  93|
# |64727|  97|
# |64727|  84|
# +-----+----+
# only showing top 5 rows


# Permet de visualiser les valeurs distinctes d'un DF
df.select('id').distinct().show()
# +-----+
# |   id|
# +-----+
# |64727|
# |75291|
# |42880|
# |23158|
# |82087|
# +-----+


# Permet d'afficher une partie du DF en fonction d'une condition
df.where(df.id == 75291).show()
# +-----+----+----+
# |   id|val1|val2|
# +-----+----+----+
# |75291|  72| 460|
# |75291|  82| 206|
# |75291|  33| 334|
# |75291|  57| 146|
# |75291|   4| 166|
# |75291|  51| 337|
# |75291|  74| 253|
# |75291|  99| 451|
# |75291|  13|  97|
# |75291|  96| 391|
# +-----+----+----+


# Plusieurs conditions
df.where((df.id == 75291) | (df.id == 82087)).show()
df.where(df.id.isin(75291, 82087)).show()
# +-----+----+----+
# |   id|val1|val2|
# +-----+----+----+
# |82087|   8| 155|
# |82087|  75| 138|
# ...
# |75291|  13|  97|
# |75291|  96| 391|
# +-----+----+----+


cond = (df.id == 75291) & (df.val1 > 70)
df.where(cond).show()
# +-----+----+----+
# |   id|val1|val2|
# +-----+----+----+
# |75291|  72| 460|
# |75291|  82| 206|
# |75291|  74| 253|
# |75291|  99| 451|
# |75291|  96| 391|
# +-----+----+----+

# Condition entre deux valeurs
cond = df.val1.between(50,70)
df.where(cond).show()
# +-----+----+----+
# |   id|val1|val2|
# +-----+----+----+
# |64727|  65| 491|
# |23158|  63| 112|
# |23158|  68| 344|
# |23158|  63| 385|
# |82087|  68| 157|
# |42880|  70|  38|
# |75291|  57| 146|
# |75291|  51| 337|
# +-----+----+----+


# Permet de changer le nom d'une colonne avec un alias
import pyspark.sql.functions as F
df.select(df.id.alias("new_id")).show()

# Permet de supprimer une colonne d'un DF
df.drop('val2').show(5)
# +-----+----+
# |   id|val1|
# +-----+----+
# |64727|   3|
# |64727|  37|
# |64727|  93|
# |64727|  97|
# |64727|  84|
# +-----+----+


# Permet de regrouper des rows d'un DF en fonction des valeurs d'une colonne particulière
df.groupby('id')\
.agg(
	F.sum(df.val1).alias('somme'),
	F.min(df.val1).alias('min')
).show()
# +-----+-----+---+
# |   id|somme|min|
# +-----+-----+---+
# |64727|  550|  3|
# |75291|  581|  4|
# |42880|  573| 10|
# |23158|  459|  0|
# |82087|  612|  8|
# +-----+-----+---+

# Les fonctions utiles
# F.sum, F.mean
# F.min, F.max
# F.count
# ...
# https://spark.apache.org/docs/2.3.1/api/python/_modules/pyspark/sql/functions.html


# Permet d'ajouter une colonne à un DF (ici la somme de deux autres)
df.withColumn('sum_val', df.val1 + df.val2).show()
df.withColumn('sum_val', sum([df[col] for col in ['val1', 'val2']])).show()
# +-----+----+----+-------+
# |   id|val1|val2|sum_val|
# +-----+----+----+-------+
# |64727|   3| 195|    198|
# |64727|  37| 196|    233|
# |64727|  93| 411|    504|
# ...



df.select([F.count(F.when(F.isnan(c), c)).alias(c) for c in df.columns]).show()
# +---+----+----+
# | id|val1|val2|
# +---+----+----+
# |  0|   0|   0|
# +---+----+----+

df.na.fill(50).show()
df.na.drop().show()


# Permet de filtrer les données d'un DF sur une condition
df.filter(df.val1.isNotNull())

# Créer une table Hive à partir d'un DF
df.createOrReplaceTempView("tmpTable") 
sqlContext.sql("create table if not exists mytable as select * from tmpTable");



# Permet de faire du windowing (lag) / Utile pour faire le liant entre différentes lignes d'un DF
from pyspark.sql.window import Window
w = Window()\
.partitionBy('id')\
.orderBy(F.col('id'))

# Ici je créé un lag d'un row et l'affiche dans une nouvelle colonne (val1_lag) puis je rajoute une nouvelle colonne "delta_val1"
# qui permet de détecter l'écart entre deux lignes
df\
.select(['id', 'val1'])\
.withColumn('val1_lag', F.lag('val1', 1).over(w))\
.withColumn('delta_val1', F.col('val1') - F.col('val1_lag'))\
.show(5)
# +-----+----+--------+----------+
# |   id|val1|val1_lag|delta_val1|
# +-----+----+--------+----------+
# |64727|   3|    null|      null|
# |64727|  37|       3|        34|
# |64727|  93|      37|        56|
# |64727|  97|      93|         4|
# |64727|  84|      97|       -13|
# +-----+----+--------+----------+

w = Window()\
.partitionBy('A_EquipId')\
.orderBy(col('A_DateAlarm'))


df = df\
.orderBy(['A_SiteId', 'A_EquipId', 'A_DateAlarm'])\
.withColumn('A_DateAlarm_lag1', F.lag('A_DateAlarm', 1).over(w))\
.withColumn('delta_sec', F.unix_timestamp('A_DateAlarm') - F.unix_timestamp('A_DateAlarm_lag1'))\
.withColumn('delta_day', F.datediff('A_DateAlarm', 'A_DateAlarm_lag1'))


# Permet de joindre deux DF à partir d'une donnée pivot
df1.join(
    df2
, "personid"
, "inner") # plus lent

df1.join(
    df2
, df1.personid == df2.personid
, "inner")\
.drop(df1.personid)


# jointure avec condition
cond = [df1.id == df2.id2,
df1.date >= df2.date_start,
((df1.date < df2.date_end) | (df2.date_end.isNull())),
]

# jointure
alarm_oth = df1\
.join(df2.select(['id2', 'date_start', 'date_end', 'type_id']), 
	on=cond, how='left')\
.drop('id2', 'date_start', 'date_end')



from pyspark import SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql.window import Window


if __name__ == '__main__':

    spark = SparkSession.builder.master("yarn").appName("tpspark").enableHiveSupport().getOrCreate()
    sc = spark.sparkContext
    sqlContext = SQLContext(sc)
    sparkCores = sc.defaultParallelism
    sc.setLogLevel("ERROR")

    df = spark.read\
         .option("delimiter", ";")\
         .option("header","true")\
         .csv('hdfs:///user/root/freq_musees.csv', inferSchema=True)



    ### 7 ###
    print("7) Afficher un extrait du dataframe")
    df.show()

    ### 8 ###
    print("8) Afficher les 5 premières lignes du dataframe")
    df.show(5)

    ### 9 ###
    print("9) Afficher seulement les colonnes ' etablissements' et ' localite' à l’écran (texte complet)")
    df.select("etablissements", "localite").show(5, False)

    ### 10 ###
    print("10) Compter le nombre de musées disponibles dans ce dataframe")
    df.count()
    print(df.count())

    ### 11 ###
    print("11) Nous ne nous intéresserons pas à certaines des colonnes du dataframe, autant les enlever. Enlever les colonnes ' grat_06', ' grat_07', ' grat_08', ' commentaires', ' wgs84' en créant un nouveau dataframe ' df_clean'")
    df_clean=df.drop("grat_06").drop("grat_07").drop("grat_08").drop("grat_09").drop("grat_10").drop("commentaires").drop("wgs84")
    df_clean.show()

    ### 12 ###
    print("12) Créer un nouveau dataframe ' df_test' d’après ' df_clean' contenant uniquement les colonnes ' num_ref', ' etablissements' et ' total_06'.")
    df_test = df_clean.select("num_ref", "etablissements", "total_06")
    df_test.show()

    ### 13 ###
    print("13) Vérifier le type de la colonne ' total_06' de ' df_test'. Si ce n’est pas le bon, créez un nouveau dataframe ' df_test2' à partir du ' df_test'. Que constatez-vous ? Faites-en part à vos encadrants.")
    df_test2 = df_test.withColumn("total_06", df_test["total_06"].cast( T.IntegerType()))
    df_test2.show()

    ### 14 ###
    print("14) Le format du fichier csv de départ n’est pas très propre (par exemple, le nombre 288179 est écrit avec un espace dans le fichier : 288 179). Au moment du cast, Spark considère ce nombre comme un string et le passe à null, ce que nous voulons éviter. Nous devons donc créer une fonction pour enlever ces espaces. La fonction suivante enlève tout caractère qui n’est pas un chiffre ")
    def remove_all_except_numbers(col):
            return F.regexp_replace(col, "[^0-9]+", "")
    print("function remove_all_except_numbers added")

    ### 15 ###
    print("15) Recrééez un nouveau dataframe ' df_test3' à partir de ' df_test'. Après cela, appliquez la fonction ' remove_all_except_numbers' pour enlever tous les espaces sur la colonne ' total_06'. Enfin, passez le type de ' total_06' à Integer, le problème devrait être réglé.")
    df_test3 = df_test
    df_test3 = df_test3.withColumn("total_06", remove_all_except_numbers(df_test3["total_06"]))
    df_test3 = df_test3.withColumn("total_06", df_test3["total_06"].cast( T.IntegerType()))
    df_test3.show()

    ### 16 ###
    print("16) Maintenant que vous avez compris comment faire le cast proprement sur une colonne, créez un nouveau dataframe ' df_clean_and_cast' en appliquant le cast sur toutes les colonnes le nécessitant à partir de ' df_clean' (qui est complet).\n Liste des colonnes à caster : ' total_06', ' total_07', ' total_08', ' total_09', ' total_10', ' evolution_07_06_en', ' evolution_08_07_en', ' evolution_09_08_en', ' evolution_10_09_en'")
    df_clean_and_cast = df_clean

    df_clean_and_cast = df_clean_and_cast.withColumn("total_06", remove_all_except_numbers(df_clean_and_cast["total_06"]))
    df_clean_and_cast = df_clean_and_cast.withColumn("total_07", remove_all_except_numbers(df_clean_and_cast["total_07"]))
    df_clean_and_cast = df_clean_and_cast.withColumn("total_08", remove_all_except_numbers(df_clean_and_cast["total_08"]))
    df_clean_and_cast = df_clean_and_cast.withColumn("total_09", remove_all_except_numbers(df_clean_and_cast["total_09"]))
    df_clean_and_cast = df_clean_and_cast.withColumn("total_10", remove_all_except_numbers(df_clean_and_cast["total_10"]))
    df_clean_and_cast = df_clean_and_cast.withColumn("evolution_07_06_en", remove_all_except_numbers(df_clean_and_cast["evolution_07_06_en"]))
    df_clean_and_cast = df_clean_and_cast.withColumn("evolution_08_07_en", remove_all_except_numbers(df_clean_and_cast["evolution_08_07_en"]))
    df_clean_and_cast = df_clean_and_cast.withColumn("evolution_09_08_en", remove_all_except_numbers(df_clean_and_cast["evolution_09_08_en"]))
    df_clean_and_cast = df_clean_and_cast.withColumn("evolution_10_09_en", remove_all_except_numbers(df_clean_and_cast["evolution_10_09_en"]))


    df_clean_and_cast = df_clean_and_cast.withColumn("total_06", df_clean_and_cast["total_06"].cast( T.IntegerType()))
    df_clean_and_cast = df_clean_and_cast.withColumn("total_07", df_clean_and_cast["total_07"].cast( T.IntegerType()))
    df_clean_and_cast = df_clean_and_cast.withColumn("total_08", df_clean_and_cast["total_08"].cast( T.IntegerType()))
    df_clean_and_cast = df_clean_and_cast.withColumn("total_09", df_clean_and_cast["total_09"].cast( T.IntegerType()))
    df_clean_and_cast = df_clean_and_cast.withColumn("total_10", df_clean_and_cast["total_10"].cast( T.IntegerType()))
    df_clean_and_cast = df_clean_and_cast.withColumn("evolution_07_06_en", df_clean_and_cast["evolution_07_06_en"].cast( T.IntegerType()))
    df_clean_and_cast = df_clean_and_cast.withColumn("evolution_08_07_en", df_clean_and_cast["evolution_08_07_en"].cast( T.IntegerType()))
    df_clean_and_cast = df_clean_and_cast.withColumn("evolution_09_08_en", df_clean_and_cast["evolution_09_08_en"].cast( T.IntegerType()))
    df_clean_and_cast = df_clean_and_cast.withColumn("evolution_10_09_en", df_clean_and_cast["evolution_10_09_en"].cast( T.IntegerType()))

    df_clean_and_cast.show()

    ### 17 ###
    print("17) Trouver combien il y a de musées parisiens")
    print(df_clean_and_cast.where(df.localite == "PARIS").count())

    ### 18 ###
    print("18) Afficher par ordre décroissant la liste des musées les plus fréquentés pendant l’année 2010")
    df_clean_and_cast.select("etablissements", "total_10").orderBy(['total_10'], ascending=[False, False]).show(150, False)

    ### 19 ###
    print("19) Afficher par ordre décroissant la liste des musées parisiens les plus fréquentés pendant l’année 2010")
    df_clean_and_cast.where(df.localite == "PARIS").select("etablissements", "localite", "total_10").orderBy(['total_10'], ascending=[False, False]).show(150, False)

    ### 20 ###
    print("20) Afficher la liste des musées ayant une fréquentation supérieure à 1000000 millions de personnes en 2010")
    df_clean_and_cast.where(df_clean_and_cast.total_10 > 1000000).select("etablissements", "localite", "total_10").show(150, False)


    ### 21 ###
    print("21) Afficher la liste des musées ayant une fréquentation entre 500000 et 1000000 millions de visiteurs en 2010")
    df_clean_and_cast.where(df_clean_and_cast.total_10.between(500000,800000)).select("etablissements", "localite", "total_10").show(150, False)


    ### 22 ###
    print("22) Créez un nouveau dataframe ' df_enrich' à partir de ' df_clean_and_cast' contenant une colonne supplémentaire : la somme de toutes les fréquentations de l’année 2006 à 2010 (somme_freq)")
    df_enrich = df_clean_and_cast.withColumn('somme_freq', df_clean_and_cast.total_06 +df_clean_and_cast.total_07 +df_clean_and_cast.total_08 + df_clean_and_cast.total_09 + df_clean_and_cast.total_10)
    df_enrich.select("etablissements", "localite", "total_06", "total_07", "total_08", "total_09", "total_10", "somme_freq").show()

    ### 23 ###
    print("23) Créez un nouveau dataframe ' df_enrich2' à partir de ' df_enrich' écartant tous les musées dont la fréquentation n’a pas été remontée au moins une année (de sorte à écarter tous les ' null'). Notez ensuite le nombre de musées suite au filtre appliqué.")
    df_enrich2 = df_enrich.filter(df_enrich.total_06.isNotNull() & df_enrich.total_07.isNotNull() & df_enrich.total_08.isNotNull() & df_enrich.total_09.isNotNull() & df_enrich.total_10.isNotNull())
    print(df_enrich2.count()) ## 87

    ### 24 ###
    print("24) Calculez la moyenne de fréquentation sur les 5 années pour chacun des musées et ajouter une nouvelle colonne ' moy_freq' au dataframe ' df_enrich2'")
    df_enrich2 = df_enrich2.withColumn('moy_freq', (df_enrich2.total_06 +df_enrich2.total_07 +df_enrich2.total_08 + df_enrich2.total_09 + df_enrich2.total_10)/5)
    df_enrich2.select("etablissements", "localite", "total_06", "total_07", "total_08", "total_09", "total_10", "somme_freq", "moy_freq").show()

    ### 25 ###
    print("25) Créez un nouveau dataframe ' df_enrich3' à partir de ' df_enrich2' ne gardant que les musées qui ont une fréquentation qui a augmenté d’année en année de 2006 à 2010. Affichez les ainsi que leur nombre.")
    df_enrich3 = df_enrich2.where((df_enrich2.total_10 > df_enrich2.total_09) & (df_enrich2.total_09 > df_enrich2.total_08) & (df_enrich2.total_08 > df_enrich2.total_07) & (df_enrich2.total_07 > df_enrich2.total_06))
    df_enrich3.select("etablissements", "localite", "total_06", "total_07", "total_08", "total_09", "total_10", "somme_freq", "moy_freq").show()


    ### 26 ###
    print("26) A partir du ' df_enrich3', afficher à l’écran l’ensemble des valeurs moyenne, min, max pour chaque colonne ' total_XX' du dataframe")
    df_enrich3.select("total_06", "total_07", "total_08", "total_09", "total_10", "somme_freq").describe().show()

    ### 27 ###
    print("27) Afficher à l’écran la colonne ' localite' du ' df_enrich3' en ' ville'")
    df_enrich3.select(df_enrich3.localite.alias("ville")).show()

    ### 28 ###
    print("28) A pàrtir du ' df_enrich2', créer un nouveau dataframe ' df_enrich4' et calculez l’évolution de fréquentation des musées entre les années 2006 et 2010 dans une nouvelle colonne ' evolution_10_06_en'")
    df_enrich4 = df_enrich2.withColumn('evolution_10_06_en', (df_enrich2.total_10 - df_enrich2.total_06)/df_enrich2.total_06*100)
    df_enrich4.select("etablissements", "total_06", "total_07", "evolution_07_06_en", "total_10", "evolution_10_06_en").show()


    ### 29 ###
    print("29) Créez un nouveau dataframe ' df_enrich5' à partir de ' df_enrich4' contenant une nouvelle colonne ' écart' et affichant l’écart de fréquentation entre les musées (à partir du musée le plus fréquenté jusqu’au moins fréquenté).")
    df_enrich5 = df_enrich4
    w = Window.partitionBy().orderBy(df_enrich5.somme_freq.desc())
    df_enrich5 = df_enrich5.withColumn("somme_freq_lag", F.lag(df_enrich5.somme_freq, 1).over(w)).withColumn('ecart', F.col('somme_freq_lag') - F.col('somme_freq'))
    df_enrich5.select("num_ref", "etablissements", "somme_freq", "ecart").show(150,False)


    ### 30 ###
    print("30) Créez un nouveau dataframe ' df_enrich6' à partir de ' df_enrich5'. Créez trois nouvelles colonnes à partir de la colonne ' num_ref'. Une colonne ' departement_id' contenant les deux premiers chiffres, une colonne ' code_insee' contenant les 5 premiers et une colonne ' num_musee_insee' contenant les deux derniers chiffres.")
    df_enrich6 = df_enrich5
    df_enrich6 = df_enrich6.withColumn('departement_id', F.concat(df_enrich6.num_ref.substr(1, 2)))
    df_enrich6 = df_enrich6.withColumn('code_insee', F.concat(df_enrich6.num_ref.substr(1, 5)))
    df_enrich6 = df_enrich6.withColumn('num_musee_insee', F.concat(df_enrich6.num_ref.substr(6, 7)))
    df_enrich6.select("num_ref", "departement_id", "code_insee", "num_musee_insee").show()


    ### 31 ###
    # Download communes.csv and put it to hdfs
    print("31) Télécharger le fichier suivant sur data.gouv.fr : https://www.data.gouv.fr/fr/datasets/correspondance-code-insee-code-postal/ Il s’agit de la liste des communes de France. Transférer le fichier sur la sandbox puis sur hdfs dans /data/ (en le renommant ' communes.csv')")
    print("Already done!")

    ### 32 ###`
    print("32) Créez un dataframe ' df_communes' à partir du fichier communes.csv et ne gardez que les champs ' code_insee', ' commune', ' département', ' region', ' population'")
    df_communes = spark.read\
         .option("delimiter", ";")\
         .option("header","true")\
         .csv('hdfs:///user/root/communes.csv', inferSchema=True)

    df_communes = df_communes.select("code INSEE", "Commune", "Département", "Région", "Population")
    df_communes.show()


    ### 33 ###
    print("33) Faire un join entre le dataframe ' df_communes' et le ' df_enrich6' sur la colonne ' code_insee' dans un nouveau dataframe ' df_join'.")
    df_join = df_enrich6
    df_join = df_join.join(
        df_communes
    , df_join.code_insee == df_communes['code INSEE']
    , "inner")\
    .drop(df_join.code_insee)
    df_join.show()

    ### 34 ###
    print("34) Faire un dataframe ' df_group_by_code_insee' contenant la somme des fréquentations des musées par code_insee, le minimum de fréquentation, le maximum de fréquentation et le nombre de musée dans le code_insee")
    df_group_by_code_insee = df_join.groupby('code INSEE', 'Commune')\
    .agg(
    	F.sum(df_join.somme_freq).alias('somme_freq_code_insee'),
    	F.min(df_join.somme_freq).alias('min_freq_code_insee'),
    	F.max(df_join.somme_freq).alias('max_freq_code_insee'),
    	F.count(df_join.somme_freq).alias('count_freq_code_insee')
    )

    ### 35 ###
    print("35) Enregistrer le dataframe ' df_join' dans une table hive (nommé ' frequentations_musees')")
    df_join.createOrReplaceTempView("tmpTable") 
    sqlContext.sql("create table if not exists frequentations_musees as select * from tmpTable");


    ### 36 ###
    print("36) Requêter la table hive une fois enregistré")
    df_hive = sqlContext.sql("select * from default.frequentations_musees")
    df_hive.show()


    ### 37 ###
    print("37) Enregistrer le dataframe ' df_group_by_code_insee' dans un fichier csv")
    # Gestion de la possibilité de dossier déjà existant
    import subprocess
    some_path = "/data/code_insee"
    subprocess.call(["hadoop", "fs", "-rmr", "-f", some_path])
    #spark
    df_group_by_code_insee.repartition(1).write.format("com.databricks.spark.csv").option("header", "true").save("code_insee")

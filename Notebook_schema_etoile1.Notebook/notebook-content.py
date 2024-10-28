# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse_name": "",
# META       "default_lakehouse_workspace_id": ""
# META     }
# META   }
# META }

# MARKDOWN ********************

# ### **Chargement de la données**

# CELL ********************

from pyspark.sql.functions import monotonically_increasing_id, when

csv_file_path = "abfss://Espace@onelake.dfs.fabric.microsoft.com/lakehouse1.Lakehouse/Files/2020_detail_IDF_dep_75.csv"

df = spark.read.csv(csv_file_path, header=True, inferSchema=True, sep=';')

# Afficher les 20 premières lignes, sans tronquer les colonnes
df_pandas = df.limit(20).toPandas()
df_pandas

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### **Dimension Construction**

# CELL ********************

table_construction = df.select("TYPECONST").distinct()

table_construction = table_construction.withColumnRenamed("TYPECONST", "TypeConstruction")

table_construction = table_construction.withColumn(
    "TypeConstruction", 
    when(table_construction["TypeConstruction"] == "C", "Collectivité")
    .when(table_construction["TypeConstruction"] == "I", "Individuel")
    .when(table_construction["TypeConstruction"] == "E", "Étudiant")
    .otherwise(table_construction["TypeConstruction"])  
)

table_construction = table_construction.withColumn("ConstructionID", monotonically_increasing_id())

table_construction = table_construction.select("ConstructionID", "TypeConstruction")

table_construction.show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### **Dimension Typologie**

# CELL ********************

table_typologie = df.select("NBPIECE").distinct()

table_typologie = table_typologie.withColumnRenamed("NBPIECE", "TypologieID")




# Ajouter une nouvelle colonne TypologieLabel avec les valeurs 'T1', 'T2', etc.
table_typologie = table_typologie.withColumn(
    "Typologie",
    when(table_typologie["TypologieID"] == 1, "T1")
    .when(table_typologie["TypologieID"] == 2, "T2")
    .when(table_typologie["TypologieID"] == 3, "T3")
    .when(table_typologie["TypologieID"] == 4, "T4")
    .when(table_typologie["TypologieID"] == 5, "T5")
    .when(table_typologie["TypologieID"] == 6, "T6")
    .when(table_typologie["TypologieID"] == 7, "T7")
    .when(table_typologie["TypologieID"] == 8, "T8")
    .when(table_typologie["TypologieID"] == 9, "T9")
    .when(table_typologie["TypologieID"] == 4, "T4")
    .otherwise("T5 et plus")  
)

# Afficher le DataFrame



table_typologie.show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### **Dimension Financement**

# CELL ********************

table_financement = df.select("FINAN").distinct()

table_financement = table_financement.withColumnRenamed("FINAN", "FinancementID")


# Ajouter une colonne correspondante avec les étiquettes spécifiques
table_financement = table_financement.withColumn(
    "TypeFinancement",
    when(table_financement["FinancementID"] == 10, "PLA d'intégration (LLTS dans les DOM)")
    .when(table_financement["FinancementID"] == 11, "PLA Loyer Minoré / PLA Très Social / PLA Insertion")
    .when(table_financement["FinancementID"] == 12, "PLA ordinaire")
    .when(table_financement["FinancementID"] == 13, "PLUS (LLS dans les DOM)")
    .when(table_financement["FinancementID"] == 14, "PLS/PPLS/PCLS/PLA CFF")
    .when(table_financement["FinancementID"] == 15, "PAP locatif")
    .when(table_financement["FinancementID"] == 16, "PLI")
    .when(table_financement["FinancementID"] == 17, "PCL (conventionné ou non)")
    .when(table_financement["FinancementID"] == 49, "Autre financement")
    .when(table_financement["FinancementID"] == 50, "HBM")
    .when(table_financement["FinancementID"] == 51, "PLR/PSR")
    .when(table_financement["FinancementID"] == 52, "HLM/O")
    .when(table_financement["FinancementID"] == 53, "ILM")
    .when(table_financement["FinancementID"] == 54, "ILN")
    .when(table_financement["FinancementID"] == 55, "Prêts spéciaux du CFF")
    .when(table_financement["FinancementID"] == 99, "Autre financement")
    .otherwise("Inconnu")  # Pour les autres valeurs non spécifiées
)

# Afficher le résultat
table_financement.show(truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### **Table de Fait**

# CELL ********************

df = df.withColumn(
    "CONSTID",
    when(df["TYPECONST"] == "C", 0)
    .when(df["TYPECONST"] == "I", 1)
    .when(df["TYPECONST"] == "E", 2)
    
)
df = df.withColumn("ID", monotonically_increasing_id())
table_fact = df.select("ID","FINAN","NBPIECE","CONSTID","COMRIL")
table_fact

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### **Chargement les données Lakehouse 3**

# CELL ********************

tables = {
    "tableConst": table_construction,  
    "tableFinan": table_financement,       
    "tableTypo": table_typologie,         
    "tableFact1": table_fact
}

base_workspace_nom = 'abfss://Espace@onelake.dfs.fabric.microsoft.com/Lakehouse3.Lakehouse/Tables/'

for table_name, dataframe in tables.items():
    
    workspace_nom = base_workspace_nom + table_name

    
    dataframe.write.format("delta").mode("overwrite").save(workspace_nom)

    



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

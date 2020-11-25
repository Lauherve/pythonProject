import pandas as pd
import sqlalchemy
import numpy as np
# DEF pour réaliser la dataframe relation (avec les contraintes et les clés)
def lireConstraintes():
    engine = sqlalchemy.create_engine("oracle+cx_oracle://stag08:Phoenix#Icar67@51.91.76.248:15440/coursdb")
    print("connecting with engine " + str(engine))
    connection = engine.connect()
    query = """
                select uc.r_constraint_name,
                        uc.table_name, 
                       uc.constraint_name
                from user_constraints uc 
    """
    return pd.read_sql_query(query, connection)
df_r = lireConstraintes()
df_r.r_constraint_name.fillna(value=np.nan,inplace=True)
df_r.drop(df_r.loc[df_r['table_name']=='INDICATEURS'].index, inplace=True)
df_r.drop(df_r.loc[df_r['table_name']=='DIM_PRODUITS'].index, inplace=True)
df_r.drop(df_r.loc[df_r['table_name']=='DIM_GEOGRAPHIE'].index, inplace=True)
df_r.drop(df_r.loc[df_r['table_name']=='DIM_CLIENTS'].index, inplace=True)
df_r.drop(df_r.loc[df_r['table_name']=='DIM_EMPLOYES'].index, inplace=True)
df_r.drop(df_r.loc[df_r['table_name']=='DIM_TEMPS'].index, inplace=True)
df_r.rename(columns={'r_constraint_name':'conn_nodeA', 'table_name':'node','constraint_name':'conn_nodeB'}, inplace=True)
# DEF pour réaliser la dataframe sur les colonnes
def lireColonnes():
    engine = sqlalchemy.create_engine("oracle+cx_oracle://stag08:Phoenix#Icar67@51.91.76.248:15440/coursdb")
    print("connecting with engine " + str(engine))
    connection = engine.connect()
    query = """
                select utc.table_name,
                        utc.column_name, 
                       utc.data_type
                from user_tab_columns utc 
    """
    return pd.read_sql_query(query, connection)
df_c = lireColonnes()
df_c.drop(df_c.loc[df_c['table_name']=='INDICATEURS'].index, inplace=True)
df_c.drop(df_c.loc[df_c['table_name']=='DIM_PRODUITS'].index, inplace=True)
df_c.drop(df_c.loc[df_c['table_name']=='DIM_GEOGRAPHIE'].index, inplace=True)
df_c.drop(df_c.loc[df_c['table_name']=='DIM_CLIENTS'].index, inplace=True)
df_c.drop(df_c.loc[df_c['table_name']=='DIM_EMPLOYES'].index, inplace=True)
df_c.drop(df_c.loc[df_c['table_name']=='DIM_TEMPS'].index, inplace=True)
df_c.drop(df_c.loc[df_c['table_name']=='VENTES_MOIS'].index, inplace=True)
df_c.drop(df_c.loc[df_c['table_name']=='VENTES_CLIENTS_2011'].index, inplace=True)
df_c.drop(df_c.loc[df_c['table_name']=='VENTES_CLIENTS_2010'].index, inplace=True)
df_c.drop(df_c.loc[df_c['table_name']=='VENTES_CLIENTS_2009'].index, inplace=True)
df_c.drop(df_c.loc[df_c['table_name']=='VENTES_CLIENTS'].index, inplace=True)
df_c.drop(df_c.loc[df_c['table_name']=='VENTES_ANNEES'].index, inplace=True)
df_c.drop(df_c.loc[df_c['table_name']=='QUANTITES_CLIENTS'].index, inplace=True)
df_c.rename(columns={'table_name':'node', 'column_name':'column'}, inplace=True)
# DEF pour réaliser la dataframe sur les tables
def lireTables():
    engine = sqlalchemy.create_engine("oracle+cx_oracle://stag08:Phoenix#Icar67@51.91.76.248:15440/coursdb")
    print("connecting with engine " + str(engine))
    connection = engine.connect()
    query = """
                select ut.table_name
                from user_tables ut
    """
    return pd.read_sql_query(query, connection)
df_t = lireTables()

df_t.drop(df_t.loc[df_t['table_name']=='INDICATEURS'].index, inplace=True)
"""df_t.drop(df_t.loc[df_t['table_name']=='INDICATEURS'].index, inplace=True)
df_t.drop(df_t.loc[df_t['table_name']=='DIM_PRODUITS'].index, inplace=True)
df_t.drop(df_t.loc[df_t['table_name']=='DIM_GEOGRAPHIE'].index, inplace=True)
df_t.drop(df_t.loc[df_t['table_name']=='DIM_CLIENTS'].index, inplace=True)
df_t.drop(df_t.loc[df_t['table_name']=='DIM_EMPLOYES'].index, inplace=True)
df_t.drop(df_t.loc[df_t['table_name']=='DIM_TEMPS'].index, inplace=True)
df_t.drop(df_t.loc[df_t['table_name']=='VENTES_MOIS'].index, inplace=True)
df_t.drop(df_t.loc[df_t['table_name']=='VENTES_CLIENTS_2011'].index, inplace=True)
df_t.drop(df_t.loc[df_t['table_name']=='VENTES_CLIENTS_2010'].index, inplace=True)
df_t.drop(df_t.loc[df_t['table_name']=='VENTES_CLIENTS_2009'].index, inplace=True)
df_t.drop(df_t.loc[df_t['table_name']=='VENTES_CLIENTS'].index, inplace=True)
df_t.drop(df_t.loc[df_t['table_name']=='VENTES_ANNEES'].index, inplace=True)
df_t.drop(df_t.loc[df_t['table_name']=='QUANTITES_CLIENTS'].index, inplace=True)
df_t.drop(df_t.loc[df_t['table_name']=='QUANTITES_CLIENTS'].index, inplace=True)"""

df_t.rename(columns={'table_name':'node'}, inplace=True)

# DEF pour réaliser la dataframe contenant les trois connecteurs des trois dataframes précédentes
def lireConsuser():
    engine = sqlalchemy.create_engine("oracle+cx_oracle://stag08:Phoenix#Icar67@51.91.76.248:15440/coursdb")
    print("connecting with engine " + str(engine))
    connection = engine.connect()
    query = """
                select ucc.table_name,
                ucc.column_name,
                ucc.constraint_name
                from user_cons_columns ucc
    """
    return pd.read_sql_query(query, connection)
df_to = lireConsuser()
df_to.drop(df_to.loc[df_to['table_name']=='INDICATEURS'].index, inplace=True)
df_to.drop(df_to.loc[df_to['table_name']=='DIM_PRODUITS'].index, inplace=True)
df_to.drop(df_to.loc[df_to['table_name']=='DIM_GEOGRAPHIE'].index, inplace=True)
df_to.drop(df_to.loc[df_to['table_name']=='DIM_CLIENTS'].index, inplace=True)
df_to.drop(df_to.loc[df_to['table_name']=='DIM_EMPLOYES'].index, inplace=True)
df_to.drop(df_to.loc[df_to['table_name']=='DIM_TEMPS'].index, inplace=True)
df_to.drop(df_to.loc[df_to['table_name']=='VENTES_MOIS'].index, inplace=True)
df_to.drop(df_to.loc[df_to['table_name']=='VENTES_CLIENTS_2011'].index, inplace=True)
df_to.drop(df_to.loc[df_to['table_name']=='VENTES_CLIENTS_2010'].index, inplace=True)
df_to.drop(df_to.loc[df_to['table_name']=='VENTES_CLIENTS_2009'].index, inplace=True)
df_to.drop(df_to.loc[df_to['table_name']=='VENTES_CLIENTS'].index, inplace=True)
df_to.drop(df_to.loc[df_to['table_name']=='VENTES_ANNEES'].index, inplace=True)
df_to.drop(df_to.loc[df_to['table_name']=='QUANTITES_CLIENTS'].index, inplace=True)
df_to.rename(columns={'table_name':'node','column_name':'column','constraint_name':'conn_node'}, inplace=True)
df_cyto = df_r.merge(df_t, on = 'node', how='left')
df_cyto=df_cyto.merge(df_c, on = 'node', how = 'left')
df_cyto.dropna(axis = 0, how = 'any', inplace =True)

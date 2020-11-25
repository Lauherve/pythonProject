import pandas as pd
import sqlalchemy

def lireConstraintes():
    engine = sqlalchemy.create_engine("oracle+cx_oracle://stag08:Phoenix#Icar67@51.91.76.248:15440/coursdb")
    print("connecting with engine " + str(engine))
    connection = engine.connect()
    query = """
                select p.table_name,
                       f.table_name,
                       p.constraint_name,
                       f.constraint_name
                from user_constraints p join user_constraints f
                on f.r_constraint_name = p.constraint_name
    """
    return pd.read_sql_query(query, connection)

df = lireConstraintes()

#df = df_test.astype('object')
df.columns = ['nodeA','nodeB','conn_nodeA','conn_nodeB']
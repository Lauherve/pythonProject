import pandas as pd
import sqlalchemy
import numpy as np

# Categories
def TableCategories():
    engine = sqlalchemy.create_engine("oracle+cx_oracle://stag08:Phoenix#Icar67@51.91.76.248:15440/coursdb")
    print("connecting with engine " + str(engine))
    connection = engine.connect()
    query = """
                select *
                from categories
    """
    return pd.read_sql_query(query, connection)


df_cat = TableCategories()
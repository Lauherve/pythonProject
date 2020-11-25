from data_dictionary import df_t
from sql_structure import df
import dash
import dash_cytoscape as cyto
import dash_html_components as html

import pandas as pd
import sqlalchemy
app = dash.Dash(__name__)
server = app.server

def lireConstraintes():
    engine = sqlalchemy.create_engine("oracle+cx_oracle://stag08:Phoenix#Icar67@51.91.76.248:15440/coursdb")
    print("connecting with engine " + str(engine))
    connection = engine.connect()
    query = """
                select p.table_name,
                       p.constraint_type,
                       p.constraint_name,
                       p.r_constraint_name
                from user_constraints p
    """
    return pd.read_sql_query(query, connection)
listeElements = []
for i in df_t.node:
    listeElements.append({'data': {'id': i, 'label': i}})

for index, i in df.iterrows():
    listeElements.append({'data': {'source': i['nodeB'], 'target': i['nodeA']}})

print(lireConstraintes().head())
df = lireConstraintes()
print(df.head())
app.layout = html.Div([
    cyto.Cytoscape(
        id='node',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '400px'},
        elements=listeElements
    )
])


if __name__ == '__main__':
    app.run_server(debug=True) 
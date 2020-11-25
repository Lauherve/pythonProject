# fichier acces a la bdd + extraction elements
# df_to et df sont les df completes
# df > nodeA, nodeB, conn_node, conn_nodeB
# df_to =  node, column, conn_node
import pandas as pd
import sqlalchemy
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto


def lireBaseDeDonnees(connexion):
    if len(connexion) < 1:
        connexion = "oracle+cx_oracle://stag08:Phoenix#Icar67@51.91.76.248:15440/coursdb"
    engine = sqlalchemy.create_engine(connexion)
    connection = engine.connect()
    query = """
                select ut.table_name as node
                from user_tables ut
    """
    tables = pd.read_sql_query(query, connection)

    query = """
                select tbe.CONSTRAINT_NAME        as "nom_contrainte",  
                           tbm.TABLE_NAME         as "table_parent",
                           clm.COLUMN_NAME        as "col_tab_parent",
                           tbe.TABLE_NAME         as "table_enfant",
                           cle.COLUMN_NAME        as "col_tab_enfant" 
                from user_constraints tbe 
                     join user_cons_columns cle
                       on  tbe.TABLE_NAME      = cle.TABLE_NAME
                       and tbe.CONSTRAINT_NAME = cle.CONSTRAINT_NAME 
                     join user_constraints tbm 
                       on tbm.CONSTRAINT_NAME = tbe.R_CONSTRAINT_NAME 
                     join user_cons_columns clm
                       on  tbm.TABLE_NAME      = clm.TABLE_NAME
                       and tbm.CONSTRAINT_NAME = clm.CONSTRAINT_NAME 
                where tbe.CONSTRAINT_TYPE = 'R'
        """
    tableReferences = pd.read_sql_query(query, connection)

    query = """
            select  
                   tc.TABLE_NAME                                                 as "nom_table",
                   tc.COLUMN_ID                                                  as "id_colonne",
                   tc.COLUMN_NAME                                                as "nom_colonne",
                   lower(tc.DATA_TYPE)                                           as "type_colonne",
                   nvl(to_char(coalesce(tc.DATA_PRECISION, tc.DATA_LENGTH)),' ') as "taille_colonne",
                   nvl(to_char(tc.DATA_SCALE),' ')                               as "precision_colonne",
                   decode(tc.NULLABLE,'Y','null','N','not null')                 as "is_nullable",
                   nvl(ky.CONSTRAINT_TYPE,' ')                                   as "type_contrainte", 
                   nvl(ky.CONSTRAINT_NAME,' ')                                   as "nom_contrainte"
            from user_tab_columns tc
                 left join (select                             
                               co.OWNER                   ,
                               co.TABLE_NAME              ,
                               cc.COLUMN_NAME             ,
                               co.CONSTRAINT_TYPE||'K'  as CONSTRAINT_TYPE,
                               co.CONSTRAINT_NAME         
                        from user_constraints co 
                             join user_cons_columns cc
                               on  co.TABLE_NAME      = cc.TABLE_NAME
                               and co.CONSTRAINT_NAME = cc.CONSTRAINT_NAME 
                        where co.CONSTRAINT_TYPE in ('P','U')) ky
                  on (     tc.TABLE_NAME     = ky.TABLE_NAME  
                       and tc.COLUMN_NAME    = ky.COLUMN_NAME  )

    """
    tableColonnes = pd.read_sql_query(query, connection)
    return tables, tableReferences, tableColonnes


# init Dash
app = dash.Dash(__name__)

listeElements = []
# LAYOUT

# ATTRIBUT HTML STYLE (classes non assignées dans css, propres à dash)
# pour pouvoir scroller etc

styles = {
    'json-output': {
        'overflow-y': 'scroll',
        'height': 'calc(50% - 25px)',
        'border': 'thin lightgrey solid'
    },
    'tab': {'height': 'calc(98vh - 115px)'},
    'sql-out': {'overflow-y': 'scroll',
                'height': 'calc(50% - 25px)',
                'border': 'thin lightgrey solid'}
}

# ATTRIBUTION DU TEXT AREA HTML
# DIV CYTOSCAPE

app.layout = html.Div([
    html.Div(className='eight columns', children=[
        cyto.Cytoscape(
            id='cytoscape',
            elements=listeElements,
            boxSelectionEnabled=True,
            layout={
                'name': 'breadthfirst'
            },
            style={
                'height': '500px',
                'width': '500px'
            }
        )
    ]),
    html.Div(className='four columns', children=[
        dcc.Tabs(id='tabs', children=[
            dcc.Tab(label='Selected Data', children=[
                html.Div(style=styles['tab'], children=[
                    html.Form([
                        html.I("Connectez vous à une base"),
                        html.Br(),
                        dcc.Input(id="lib", type="text", placeholder="Entrer la librairie de connexion",
                                  value="oracle+cx_oracle"),
                        dcc.Input(id="user", type="text", placeholder="Entrez l'id user", value="stag08"),
                        dcc.Input(id="Password", type="password", placeholder="Entrez le mot de passe",
                                  value="Phoenix#Icar67"),
                        dcc.Input(id="ip", type="text", placeholder="Entrer l'adresse ip de la bdd",
                                  value="51.91.76.248"),
                        dcc.Input(id="Port", type="text", placeholder="Entrez le port", value="15440"),
                        dcc.Input(id="dossier", type="text", placeholder="Entrer votre nom de dossier",
                                  value="coursdb"),
                        html.Button(id='submit-button', type='submit', children='Valider'),
                    ]),

                    html.P('SQL-output'),
                    html.Pre(
                        id='selected-nodes-edges',
                        style=styles['sql-out']
                    )
                ])
            ])
        ]),
    ]),
    html.Div(id='placeholder')
])


@app.callback(Output('selected-nodes-edges', 'children'),
              [Input('cytoscape', 'selectedEdgeData'),
               Input('cytoscape', 'selectedNodeData')])
def testing(selected_edge, selected_node):
    e = selected_edge
    n = selected_node
    if len(selected_node) == 0 and len(selected_edge) == 0:
        return None
    elif len(selected_node) == 0 and len(selected_edge) == 1:
        return 'Sélectionner un noeud en premier'
    elif len(selected_node) == 1 and len(selected_edge) == 0:
        return 'SELECT * FROM ' + selected_node[0]['id']
    elif len(selected_node) == 1 and len(selected_edge) == 1:
        return 'Merci de sélectionner le second noeud de la jointure'


@app.callback(Output('cytoscape', 'elements'),
              Input('cytoscape', 'tapNode'),
              State('cytoscape', 'elements'))  # recupere les elements caracteristiques
def selection(selected_node, els):
    print(selected_node)
    linkednodes = []  # pour mettre les composants de l'élément dans une liste
    for e in selected_node['edgesData']:
        if e['source'] != selected_node['data']['id']:
            linkednodes.append(e['source'])  # créer une liste qui retourne les composants de la source du node
        elif e['target'] != selected_node['data']['id']:
            linkednodes.append(e['target'])  # créer une liste qui retourne les composants de la target du node
    for i, e in enumerate(els):  # on recupère la position des éléments dans la liste
        if e['type'] == 'node':  # type c'est target ou source
            if e['data']['id'] in linkednodes:
                els[i]['selected'] = True  # affiche les éléments associés
    return els


@app.callback(
    [Output("cytoscape", "elements")],
    Input('submit-button', 'n_clicks'),
    [State('lib', 'value'),
     State('user', 'value'),
     State('Password', 'value'),
     State('ip', 'value'),
     State('Port', 'value'),
     State('dossier', 'value')])
def update_output(n_clicks, lib, user, password, ip, port, dossier):
    global listeElements

    if n_clicks is None:
        return [listeElements]

    connex = "{}://{}:{}@{}:{}/{}".format(lib, user, password, ip, port, dossier)
    tables, tableReferences, tableColonnes = lireBaseDeDonnees(connex)
    listeElements = []
    for i in tables.node:
        listeElements.append({'type': 'node', 'data': {'id': i, 'label': i}})

    for index, i in tableReferences.iterrows():
        listeElements.append({'type': 'edge', 'data': {'source': i['table_parent'], 'target': i['table_enfant'], 'colsource' :i['col_tab_parent'], 'coltarget': i['col_tab_enfant'], 'edge': i['nom_contrainte']}})

    return [listeElements]

@app.callback(Output('cytoscape', 'elements'),
             Input ('cytoscape','tapNode'),
             State('cytoscape', 'elements')) # recupere les elements caracteristiques
def selection(selected_node, els):
    print(selected_node)
    linkednodes = [] #pour mettre les composants de l'élément dans une liste
    for e in selected_node['edgesData']:
        if e['source'] != selected_node['data']['id']: linkednodes.append(e['source']) #créer une liste qui retourne les composants de la source du node
        elif e['target'] != selected_node['data']['id']: linkednodes.append(e['target']) #créer une liste qui retourne les composants de la target du node
    for i, e in enumerate(els): #on recupère la position des éléments dans la liste
        if e['type']=='node': #type c'est target ou source
            if e['data']['id'] in linkednodes:
                els[i]['selected'] = True #affiche les éléments associés
    return els

if __name__ == '__main__':
    app.run_server(debug=True)

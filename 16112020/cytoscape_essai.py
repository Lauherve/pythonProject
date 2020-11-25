import dash
import dash_cytoscape as cyto
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-two-nodes',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '400px'},
        elements=[
            {'data': {'id': 'Categories', 'label': 'Categories'}, 'position': {'x': 75, 'y': 75}},
            {'data': {'id': 'Clients', 'label': 'Clients'}, 'position': {'x': 200, 'y': 200}},
            {'data': {'id': 'Commandes', 'label': 'Commandes'}, 'position': {'x': 90, 'y': 90}},
            {'data': {'id': 'Employes', 'label': 'Employes'}, 'position': {'x': 90, 'y': 90}},
            {'data': {'id': 'Employes', 'label': 'Employes'}, 'position': {'x': 75, 'y': 75}},
            {'data': {'id': 'Fournisseurs', 'label': 'Fournisseurs'}, 'position': {'x': 90, 'y': 90}},
            {'data': {'id': 'Produits', 'label': 'Produits'}, 'position': {'x': 75, 'y': 75}},
            {'data': {'id': 'Details_commandes', 'label': 'Details_commandes'}, 'position': {'x': 90, 'y': 90}},

            {'data': {'source': 'Categories', 'target': 'Produits'}},
            {'data': {'source': 'Clients', 'target': 'Commandes'}},
            {'data': {'source': 'Commandes', 'target': 'Details_commandes'}},
            {'data': {'source': 'Employes', 'target': 'Commandes'}},
            {'data': {'source': 'Employes', 'target': 'Employes'}},
            {'data': {'source': 'Fournisseurs', 'target': 'Produits'}}
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
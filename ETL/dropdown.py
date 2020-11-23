# exemple de sélecteur pour des tables éventuelles
import dash
import dash_html_components as html
import dash_core_components as dcc
from data_dictionary import df_cyto

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
dcc.Dropdown(
    id='demo-dropdown',
    options=[
        {'label': 'Commandes', 'value': 'Com'},
        {'label': 'Produits', 'value': 'Pro'},
        {'label': 'Clients', 'value': 'Cli'}
    ],
    value=['Pro', 'Com'],
    multi=True
),
    html.Div(id='dd-output-container')
])


@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)
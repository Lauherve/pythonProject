import json
from data_dictionary import df_t
from sql_structure import df
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import dash_cytoscape as cyto

app = dash.Dash(__name__)
server = app.server


listeElements = []
for i in df_t.node:
    listeElements.append({'data': {'id': i, 'label': i}})

for index, i in df.iterrows():
    listeElements.append({'data': {'source': i['nodeB'], 'target': i['nodeA']}})

styles = {
    'json-output': {
        'overflow-y': 'scroll',
        'height': 'calc(50% - 25px)',
        'border': 'thin lightgrey solid'
    },
    'tab': {'height': 'calc(98vh - 115px)'}
}

app.layout = html.Div([
    html.Div(className='eight columns', children=[
        cyto.Cytoscape(
            id='cytoscape',
            elements=listeElements,
            boxSelectionEnabled=True,
            layout={
                'name': 'circle'
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
                    html.P('Node Data JSON:'),
                    html.Pre(
                        id='selected-node-data-json-output',
                        style=styles['json-output']
                    ),
                    html.P('Edge Data JSON:'),
                    html.Pre(
                        id='selected-edge-data-json-output',
                        style=styles['json-output']
                    )
                ])
            ])
        ]),
    ]),

    html.Div(id='placeholder')
])




@app.callback(Output('selected-node-data-json-output', 'children'),
              [Input('cytoscape', 'selectedNodeData')])
def displaySelectedNodeData(data):
    return json.dumps(data, indent=2)


@app.callback(Output('selected-edge-data-json-output', 'children'),
              [Input('cytoscape', 'selectedEdgeData')])
def displaySelectedEdgeData(data):
    return json.dumps(data, indent=2)


if __name__ == '__main__':
    app.run_server(debug=True)



    "SELECT * FROM {]".format('source')
import dash
import numpy as np
import pandas as pd
import re
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.CYBORG])
server = app.server
port = int(os.environ.get("PORT", 5000))

app.layout = html.Div(
                       [
               dbc.Row(
                       [
                         dbc.Col([
                                html.Ul(
                                  [
                                    html.Li('Green risk analysis - GRA'),
                                    html.Li('Produce simulated outcome based on selected ranges \
                                             of critical variables'),
                                    html.Li('Simulation based on Monte-Carlo algorithm')
                                  ]
                                ),
                                html.Br(),
                                html.Div(
                                    [    
                                     html.Label('Select critical variables - '),
                                     dcc.Dropdown(
                                                   id = 'dropdown_params',
                                                   multi = True,
                                                   style = {
                                                             'width' : '60%',
                                                             'height' : '40px',
                                                             'color' : 'black'
                                                            },
                                                   options = [{'label' : 'parameter - %s' %i,
                                                              'value' :  i} for i in \
                                                              ['A', 'B', 'C', 'AB', 'AC', 'BC']], 
                                                   value = ''
                                                  )
                                    ],
                                      style = {'marginLeft' : '30px'}
                                  ),
                         html.Br(),
                         html.Br(),
                         html.Br(),
                         html.Br(),
                         html.Br(),
                         html.Br(),
                         html.Br(),
                           
                         html.Div(
                                   id = 'text',
                                   style = {
                                             'width' : '60%',
                                             'height' : '40px',
                                             'marginLeft' : '30px',
                                             'fontSize' : 20
                                           }
                                 ),
                         html.Br(),
                         html.Div(
                                  [
                                    html.Label('Input coefficients - '),
                                    html.Br(),
                                    dcc.Textarea(
                                                  id = 'coefficient',
                                                  placeholder = 'coefficients from DoE model',
                                                  style = {
                                                            'width' : '60%',
                                                            'height' : '40px'
                                                          }
                                                )
                                  ],
                                    style = {'marginLeft' : '30px'}
                                ),
                         html.Br(),
                           
                         html.Div(
                                   [
                                     html.Label('Range selector for variable A -'),
                                     html.Br(),
                                     dcc.RangeSlider(
                                                      id = 'slider_A',
                                                      min = -1,
                                                      max = 1,
                                                      value = [-1, 1],
                                                      step = 0.01,
                                                      tooltip = {'always_visible' : True}
                                                    ),
                                     html.Br(),
                                     html.Label('Range selector for variable B -'),
                                     html.Br(),
                                     dcc.RangeSlider(
                                                      id = 'slider_B',
                                                      min = -1,
                                                      max = 1,
                                                      value = [-1, 1],
                                                      step = 0.01,
                                                      tooltip = {'always_visible' : True}
                                                    ),
                                     html.Br(),
                                     html.Label('Range selector for variable C -'),
                                     html.Br(),
                                     dcc.RangeSlider(
                                                      id = 'slider_C',
                                                      min = -1,
                                                      max = 1,
                                                      value = [-1, 1],
                                                      step = 0.01,
                                                      tooltip = {'always_visible' : True}
                                                    )
                                   ],
                                     style = {
                                               'marginLeft' : '30px',
                                               'width' : '55%'
                                             }
                                )
                                    ],
                                    lg = 6, md = 6), # end of first dbc.Col()
                                   
                  dbc.Col([
                            html.Br(),
                            html.Br(),
                            html.Div(
                                      [ 
                                        html.Label('Simulated range for the response - '),
                                        html.Div(
                                                  id = 'result',
                                                  style = {'fontSize' : 16}
                                                 ),
                                        html.Br()
                                       ],
                                        style = {
                                                  'width' : '60%',
                                                  'height' : '40px'
                                                }
                                       ),
                            html.Br(),
                            html.Br(),
                            
                            html.Div(
                                     [
                                       html.Label('Graphic simulation for the response - '),
                                       dcc.Graph(
                                                  id = 'figure',
                                                  style = {
                                                            'width' : '90%',
                                                            'height' : '450px'
                                                          }
                                                )
                            
                                     ],
                                       style = {
                                                 'width' : '100%',
                                                 'height' : '500px'
                                                }
                                    )
                       
                         ], lg = 6, md = 6)
                     
                                  ] # end of dbc.Row()
                                   ) # end of dbc.Row()
                       ]
                     )

@app.callback(
               Output('text', 'children'),
               Input('dropdown_params', 'value')
             )
def update_text(params):
    return 'Selected variables - int + ' + ' + '.join(params)


@app.callback(
               Output('result', 'children'),
               Input('dropdown_params', 'value'),
               Input('coefficient', 'value'),
               Input('slider_A', 'value'),
               Input('slider_B', 'value'),
               Input('slider_C', 'value')
             )
def update_result(params, coeff, range_A, range_B, range_C):
    if not coeff:
        raise PreventUpdate
        
    coeff_regex = re.compile(r'-?\d+\.?\d*')
    B = np.array([float(i) for i in coeff_regex.findall(coeff)]).T
    
    if len(params) + 1 != len(B):
        raise PreventUpdate
    
    dct = {}
    
    intecept = np.ones(shape = 100000, dtype = int)  
    dct.setdefault('int', intecept)
    
    if 'A' in params or 'AB' in params or 'AC' in params:
        array_A = np.random.uniform(range_A[0], range_A[1], 100000)
        dct.setdefault('A', array_A)
        
    if 'B' in params or 'AB' in params or 'BC' in params:
        array_B = np.random.uniform(range_B[0], range_B[1], 100000)
        dct.setdefault('B', array_B)
    
    if 'C' in params or 'AC' in params or 'BC' in params:
        array_C = np.random.uniform(range_C[0], range_C[1], 100000)
        dct.setdefault('C', array_C)
        
    if 'AB' in params:
        array_AB = array_A * array_B
        dct.setdefault('AB', array_AB)
    
    if 'AC' in params:
        array_AC = array_A * array_C
        dct.setdefault('AC', array_AC)
    
    if 'BC' in params:
        array_BC = array_B * array_C
        dct.setdefault('BC', array_BC)
        
 
    df = pd.DataFrame(dct)
    result = np.array(df) @ B
    
    predicted_min = result.min()
    predicted_max = result.max()
    
    result_txt = '(%s, %s)' %(np.round(predicted_min, 4), np.round(predicted_max, 4))
    
    return result_txt

#     return ' '.join(df.columns.tolist())


@app.callback(
               Output('figure', 'figure'),
               Input('dropdown_params', 'value'),
               Input('coefficient', 'value'),
               Input('slider_A', 'value'),
               Input('slider_B', 'value'),
               Input('slider_C', 'value')
             )
def update_graph(params, coeff, range_A, range_B, range_C):
    if not coeff:
        raise PreventUpdate
        
    coeff_regex = re.compile(r'-?\d+\.?\d*')
    B = np.array([float(i) for i in coeff_regex.findall(coeff)]).T
    
    if len(params) + 1 != len(B):
        raise PreventUpdate
    
    dct = {}
    
    intecept = np.ones(shape = 100000, dtype = int)  
    dct.setdefault('int', intecept)
    
    if 'A' in params or 'AB' in params or 'AC' in params:
        array_A = np.random.uniform(range_A[0], range_A[1], 100000)
        dct.setdefault('A', array_A)
        
    if 'B' in params or 'AB' in params or 'BC' in params:
        array_B = np.random.uniform(range_B[0], range_B[1], 100000)
        dct.setdefault('B', array_B)
    
    if 'C' in params or 'AC' in params or 'BC' in params:
        array_C = np.random.uniform(range_C[0], range_C[1], 100000)
        dct.setdefault('C', array_C)
        
    if 'AB' in params:
        array_AB = array_A * array_B
        dct.setdefault('AB', array_AB)
    
    if 'AC' in params:
        array_AC = array_A * array_C
        dct.setdefault('AC', array_AC)
    
    if 'BC' in params:
        array_BC = array_B * array_C
        dct.setdefault('BC', array_BC)
        
 
    df = pd.DataFrame(dct)
    result = (np.array(df) @ B).tolist()
    
    fig = go.Figure()
    fig.add_histogram(x = result, nbinsx = 20)
    fig.update_traces(marker_line_width = 0.5, marker_line_color = 'orange')
    
    fig.layout.title = 'Monte Carlo simulation'
    fig.layout.xaxis.title = 'Distribution'
    fig.layout.yaxis.title = 'Frequency'
    fig.layout.template = 'plotly_dark'
    
    return fig


if __name__ == '__main__':
    monte_carlo.run_server(debug = False, 
                   host="0.0.0.0",
                   port=port)

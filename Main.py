import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import matplotlib
import numpy as np
matplotlib.use("Agg") # Was having issues with matplotlib's interactive backend

from Calculation_Utils import BlackScholes
from Object_Utils import FormulaVariable, Card, COLORS
from SQL_functions import save_inputs_to_db, save_outputs_to_db # Set up in the SQL_functions file first

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Black-Scholes Pricing Model", style={'color': COLORS['blue'], "marginTop":"20px", "marginBottom": "10px", "textAlign" : "center"}),
    html.H4("*Press Calculate for Output*", style={'color': COLORS['blue'], "marginTop":"10px", "marginBottom": "15px", "textAlign" : "center"}),
    dbc.Row([
        dbc.Col([
            html.H3("Formula Parameters", style={'color': COLORS['blue'], "marginTop":"20px", "alignment" : "center"}),

            # For the base variables that go into calculating the put and call price
            FormulaVariable("Spot Price (S)", "spot_price", 0, 1000000, 0.01, 100).create_component(),
            FormulaVariable("Strike Price (K)", "strike_price", 0, 1000000, 0.01, 100).create_component(),
            FormulaVariable("Time to Maturity (T, in years)", "time_to_maturity", 0.01, 100, 0.001, 1).create_component(),
            FormulaVariable("Volatility (\u03c3, % per year)", "volatility", 0, 100, 0.01, 0.2).create_component(),
            FormulaVariable("Risk-Free Rate (r, % per year)", "risk_free_rate", 0, 100, 0.01, 0.05).create_component() 
        ], style={"marginBottom": "5px", "marginLeft":"50px"}),
            # Corresponding put and call values based on the variables above
        dbc.Col([
            html.H3("Put and Call Values", style = {'color': COLORS['blue'], "marginTop":"20px", "alignment" : "center"}),

            Card(title = "CALL", value_id = "call-value", value_class = "call-class", color = "success", inverse = True, start_value = "0.00").create_card(),
            Card(title = "PUT", value_id = "put-value", value_class = "put-class", color = "danger", inverse = True, start_value = "0.00").create_card()
        ])
    ], style = {"marginBottom": "50px", "marginRight":"30px"}),

    dbc.Row([
        # For the parameters that go into making the heatmap, in combination with the ones above
        dbc.Col([
            html.H3("Heatmap Parameters (strike price is constant)",style = {'color': COLORS['blue'], "marginTop":"20px", "alignment" : "center"}),

            FormulaVariable("Minimum Spot Price", "min_spot_price", 0, 1000000, 0.01, 80).create_component(),
            FormulaVariable("Maximum Spot Price", "max_spot_price", 0, 1000000, 0.01, 120).create_component(),
            FormulaVariable("Minimum Volatility", "min_volatility", 0, 100, 0.01, 0.10).create_component(),
            FormulaVariable("Maximum Volatility", "max_volatility", 0, 100, 0.01, 0.30).create_component(),
            FormulaVariable("Call Purchase Price", "purchase_price_call", 0, 1000000, 0.01, 10).create_component(),
            FormulaVariable("Put Purchase Price", "purchase_price_put", 0, 1000000, 0.01, 5).create_component(),

            dbc.Button("CALCULATE", id = "calculate-button", color = "primary", size = "lg", style = {"marginTop": "20px", "marginBottom":"10px"}),
            html.P("A mySQL relational database can be used to save snapshots of inputs and outputs every time Calculate is pressed. See SQL_functions file.")
        ], style = {"marginLeft": "30px"}),

        # For the heatmaps taht correspond to the variables
        dbc.Col([
            html.H3("Options Price Heatmaps (hover to zoom)",style = {'color': COLORS['blue'], "marginTop":"20px", "alignment" : "center"}),

            dcc.Graph(id='call_heatmap', style = {"marginBottom":"50px"}, config = {'modeBarButtonsToRemove': [
            'zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d',
            'zoomOut2d', 'autoScale2d', 'resetScale2d', 'hoverClosestCartesian',
            'hoverCompareCartesian'
            ]}, figure=go.Figure()),

            dcc.Graph(id='put_heatmap', config = {'modeBarButtonsToRemove': [
            'zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d',
            'zoomOut2d', 'autoScale2d', 'resetScale2d', 'hoverClosestCartesian',
            'hoverCompareCartesian'
            ]}, figure=go.Figure())
        ])
    ], style = {"marginRight":"30px"})
])

@app.callback(
    Output("call-value", "children"), 
    Output("put-value", "children"),
    Output("call_heatmap", "figure"),
    Output("put_heatmap", "figure"),
    # The callback layout makes it so that the state only becomes input once the calculate button is clicked
    Input("calculate-button", "n_clicks"),

    State("spot_price", "value"),
    State("strike_price", "value"),
    State("time_to_maturity", "value"),
    State("volatility", "value"),
    State("risk_free_rate", "value"),
    State("purchase_price_call", "value"),  
    State("purchase_price_put", "value"),   
    State("min_spot_price", "value"),
    State("max_spot_price", "value"),
    State("min_volatility", "value"),
    State("max_volatility", "value")
)
def update_option_prices(n_clicks, spot_price, strike_price, time_to_maturity, volatility, risk_free_rate,
                         purchase_price_call, purchase_price_put,  
                         min_spot_price, max_spot_price, min_volatility, max_volatility
                         ):
    if n_clicks is None:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # Handles temporary empty boxes
    if None in [spot_price, strike_price, time_to_maturity, volatility, risk_free_rate, purchase_price_call, purchase_price_put, min_spot_price, max_spot_price, min_volatility, max_volatility] or 0 in [spot_price, strike_price, time_to_maturity, volatility, risk_free_rate, purchase_price_call, purchase_price_put, min_spot_price, max_spot_price, min_volatility, max_volatility]:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update
    # This is the eventual return value for the call and put price boxes at the top of the app
    
    # Uncomment the variable below once you set up your SQL database
    #calculation_id = save_inputs_to_db(spot_price, strike_price, time_to_maturity, volatility, risk_free_rate)

    black_scholes1 = BlackScholes(time_to_maturity, strike_price, spot_price, volatility, risk_free_rate)
    black_scholes1.calculate_prices()
    call_price = round(black_scholes1.call_price,2)
    put_price = round(black_scholes1.put_price,2)
    # Below is to construct the heatmap, took a lot of inspiration and reference from https://github.com/prudhvi-reddy-m/BlackScholes/blob/main/streamlit_app.py#L166
    # But I edited the function to account for PnL instead of simply the heatmap representing the value
    # In other words it will be value - purchase price for each individual square
    spot_range = np.linspace(min_spot_price, max_spot_price, 10)
    vol_range = np.linspace(min_volatility, max_volatility, 10)
    call_pnl = np.zeros((len(vol_range), len(spot_range))) 
    put_pnl = np.zeros((len(vol_range), len(spot_range)))  

    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            bs_temp = BlackScholes(
                time_to_maturity=time_to_maturity,
                strike=strike_price,
                current_price=spot,
                volatility=vol,
                interest_rate=risk_free_rate
            )
            bs_temp.calculate_prices()
            call_pnl[i, j] = bs_temp.call_price - purchase_price_call  
            put_pnl[i, j] = bs_temp.put_price - purchase_price_put     

    call_pnl = np.flipud(call_pnl)
    put_pnl = np.flipud(put_pnl)
    
    # Uncomment the variable below once you set up your SQL database
    #save_outputs_to_db(calculation_id, spot_range, vol_range, call_pnl, put_pnl)

    # Setting up the heatmaps based on the calculated values--it goes from red, yellow, to green according to the value in the box
    call_fig = go.Figure(
        data=[go.Heatmap(z = call_pnl, x = spot_range, y = vol_range, colorscale = [[0, 'red'], [0.5, 'yellow'], [1, 'green']], 
                         colorbar = dict(title = "Call PnL"), text = call_pnl, texttemplate = "%{text:.2f}",
        textfont = {"size": 10}, showscale = True, hoverinfo = 'none')],
        layout = go.Layout(title = "Call PnL Heatmap (Value - Call Purchase Price)", xaxis_title = "Spot Price", yaxis_title = "Volatility", dragmode = False)
    )

    put_fig = go.Figure(
        data=[go.Heatmap(z = put_pnl, x = spot_range, y = vol_range, colorscale = [[0, 'red'], [0.5, 'yellow'], [1, 'green']],
                         colorbar = dict(title = "Put PnL"), text = put_pnl, texttemplate = "%{text:.2f}",
        textfont = {"size": 10}, showscale = True, hoverinfo = 'none')],
        layout = go.Layout(title = "Put PnL Heatmap (Value - Put Purchase Price)", xaxis_title = "Spot Price", yaxis_title = "Volatility", dragmode = False)
    )
    
    return call_price, put_price, call_fig, put_fig

if __name__ == "__main__":
    app.run_server(debug=True)

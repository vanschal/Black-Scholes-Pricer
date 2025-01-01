from dash import dcc, html
import dash_bootstrap_components as dbc

# These are objects created to make the Main file clearer and more readable, nothing special
COLORS = {
    'green': '#28a745',   
    'red': '#c61a09',     
    'white': '#ffffff',
    'blue': '#007bff'    
}

class FormulaVariable:
    def __init__(self, label, variable_id, min_value, max_value, step, value):
        self.label = label
        self.input_id = f"{variable_id}"
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = value

    def create_component(self):
        return html.Div([
            html.Label(self.label),
            dcc.Input(
                id = self.input_id,
                type = 'number',
                min = self.min_value,
                max = self.max_value,
                step = self.step,
                value = self.value,
                style = {'marginLeft': '10px', 'width': '100px', 'textAlign':'center'}
            )
        ], style = {'width':'80%', 'marginBottom':'20px'})

    
class Card:
    def __init__(self, title, value_id, value_class, start_value, font_size="32px", font_weight="bold", color="light", inverse=False):
        self.title = title
        self.value_id = value_id
        self.value_class = value_class
        self.font_size = font_size
        self.font_weight = font_weight
        self.color = color
        self.inverse = inverse
        self.start_value = start_value

    def create_card(self):
        return dbc.Card(
            dbc.CardBody([
                html.H4(self.title, className="card-title"),
                html.P(
                    f"${self.start_value}",
                    id=self.value_id,
                    className=self.value_class,
                    style={"fontSize": self.font_size, "fontWeight": self.font_weight, "textAlign":"center"}
                )
            ]),
            color=self.color,
            inverse=self.inverse,
            style={"marginBottom": "20px"} 
        )
    
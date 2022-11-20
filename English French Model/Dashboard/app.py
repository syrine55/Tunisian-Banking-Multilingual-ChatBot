import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


data = pd.read_excel("Dashboard/client.xlsx")
data["Date_ope"] = pd.to_datetime(data["Date_ope"], format="%d-%m-%Y")
data.sort_values("Date_ope", inplace=True)

fig = px.bar(data, x="Type", y="Debit", color="Type", barmode="group",width=1024,height=450)
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
fig3=make_subplots(rows=1,cols=2,specs=[[{'type':'domain'},{'type':'domain'}]])

fig3.add_trace(go.Pie(labels=data["Type"].unique(),values=data["Debit"]))

fig3.update_traces(hole=.4, hoverinfo="label+percent+name")
fig3.update_layout(
    title_text="Debit distribution regarding the types of banking operations"
)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Account Analytics: Understand Your actions"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="", className="header-emoji"),
                html.H1(
                    children="Account Analytics", className="header-title"
                ),
                html.P(
                    children="",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                # html.Div(
                #     children=[
                #         html.Div(children="Region", className="menu-title"),
                #         dcc.Dropdown(
                #             id="region-filter",
                #             options=[
                #                 {"label": region, "value": region}
                #                 for region in np.sort(data.region.unique())
                #             ],
                #             value="Albany",
                #             clearable=False,
                #             className="dropdown",
                #         ),
                #     ]
                # ),
                # html.Div(
                #     children=[
                #         html.Div(children="Type", className="menu-title"),
                #         dcc.Dropdown(
                #             id="type-filter",
                #             options=[
                #                 {"label": avocado_type, "value": avocado_type}
                #                 for avocado_type in data.Type.unique()
                #             ],
                #             value="organic",
                #             clearable=False,
                #             searchable=False,
                #             className="dropdown",
                #         ),
                #     ],
                # ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.Date_ope.min().date(),
                            max_date_allowed=data.Date_ope.max().date(),
                            start_date=data.Date_ope.min().date(),
                            end_date=data.Date_ope.max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        
                        id="price-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(id='example-graph',
            figure=fig), className="card",
                    ),
                html.Div(
                    children=dcc.Graph(figure=fig3), className="card",
                    )
                ],
            className="wrapper",
        
        ),
   
    

        
    ]
)








@app.callback(
    [Output("price-chart", "figure"), Output("volume-chart", "figure")],
    [
        # Input("region-filter", "value"),
        # Input("type-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(start_date, end_date):
    mask = (
       # (data.region == region)
      #  & 
      #(data.type == ope_type) 
       (data.Date_ope >= start_date)
        & (data.Date_ope <= end_date)
      
      
    )
    filtered_data = data.loc[mask, :]
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date_ope"],
                "y": filtered_data["Solde"],
                "type": "lines",
                "hovertemplate": "DT%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Your balance",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "DT", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    volume_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date_ope"],
                "y": filtered_data["Debit"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Flow rate", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True,"tickprefix": "DT"},
            "colorway": ["#E12D39"],
        },
    }
    return price_chart_figure, volume_chart_figure


if __name__ == "__main__":
    app.run_server(host="25.75.41.18", port=8050, debug=False)
from dash import dcc, html
from dash.dependencies import Input, Output
from utils.models import VRLI, SessionLocal
import pandas as pd


def create_layout():

    # считаем  значения для инициализации дропдауна
    session = SessionLocal()
    try:
        file_names = session.query(VRLI.filename).distinct().all()
    finally:
        session.close()

    file_names = [name[0] for name in file_names]

    # начало самого layout

    return html.Div([
        dcc.Store(id="selected-points-store", data=[]),
        dcc.Store(id="selected-df", data=pd.DataFrame({}).to_dict('records')),

        html.H1("Аннотация данных", style={'textAlign': 'center'}),

        html.Div([
            html.Div([
                html.Label("Выберите файл:"),
                dcc.Dropdown(
                    options=[{'label': name, 'value': name}
                             for name in file_names],
                    value=file_names[0],
                    id='dropdown',
                    clearable=False,
                    style={'width': '100%'}
                ),
                html.Label("Диапазон скорости:"),
                dcc.RangeSlider(id='velocity-slider', min=1, max=100),
                html.Label("Диапазон времени:"),
                dcc.RangeSlider(id='range-slider', min=1, max=100),
                html.Div([
                    html.Button("Сохранить", id="submit-button"),
                    html.Button("Сбросить нынешнее выделение",
                                id="reset-button"),
                    html.Button("Полный сброс", id="full-reset-button")
                ], style={'display': 'flex', 'gap': '10px', 'marginTop': '10px'})
            ], style={
                'flex': '1',
                'padding': '20px',
                'borderRadius': '10px',
                'backgroundColor': '#f9f9f9',
                'boxShadow': '0 4px 12px rgba(0,0,0,0.1)'
            }),

            html.Div([
                html.H3("Статистика"),
                html.Div(id='stats-output',
                     style={'fontSize': '16px', 'lineHeight': '1.5'})
            ], style={
                'flex': '1',
                'padding': '20px',
                'borderRadius': '10px',
                'backgroundColor': '#f9f9f9',
                'boxShadow': '0 4px 12px rgba(0,0,0,0.1)'
            })
        ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px'}),
        html.Div([
            dcc.Graph(id='graph_x_y', style={'flex': '1', 'height': '500px'}),
            dcc.Graph(id='graph_x_z', style={'flex': '1', 'height': '500px'})
        ], style={'display': 'flex', 'gap': '10px'})
    ], style={'width': '95%', 'margin': '0 auto'})

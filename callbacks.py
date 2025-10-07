from dash import Input, Output, State, callback, no_update, dcc
from dash.exceptions import PreventUpdate
from utils.FigureUpdate import get_figure
from utils.getdf import get_df
from utils.models import VRLI, SessionLocal
import pandas as pd


def register_callbacks(app):

    @app.callback(
        Output('range-slider', 'min'),
        Output('range-slider', 'max'),
        Output('range-slider', 'value'),
        Output('range-slider', 'step'),
        Output('range-slider', 'marks'),
        Output('velocity-slider', 'min'),
        Output('velocity-slider', 'max'),
        Output('velocity-slider', 'value'),
        Output('velocity-slider', 'step'),
        Output('velocity-slider', 'marks'),
        Output('selected-points-store', 'data'),
        Output('selected-df', 'data'),
        Input('dropdown', 'value')
    )
    def update_sliders_params(selected_name):
        session = SessionLocal()
        try:
            filtered_df = get_df(session, selected_name)
        finally:
            session.close()

        if filtered_df.empty:
            raise PreventUpdate

        # параметры временного слайдера

        tmin = filtered_df['Time'].min()
        tmax = filtered_df['Time'].max()
        tstep = (tmax - tmin) / \
            20 if len(filtered_df) >= 20 else (tmax - tmin) / len(filtered_df)
        marks = {}
        num_marks = int((tmax - tmin) / tstep)

        for i in range(num_marks):
            value = tmin + (tmax - tmin) * i / (num_marks - 1)
            rounded_value = round(value, 2)
            label = str(int(rounded_value)) if rounded_value.is_integer(
            ) else f"{rounded_value:.2f}".rstrip('0').rstrip('.')
            marks[rounded_value] = {'label': label, 'style': {
                'fontSize': '11px', 'whiteSpace': 'nowrap'}}

        labeled_points = filtered_df.index[filtered_df['label'] == 1].tolist()

        # параметры слайдера со скоростями

        vmin = filtered_df['Velocity'].min()
        vmax = filtered_df['Velocity'].max()
        vstep = (vmax - vmin) / \
            20 if len(filtered_df) >= 20 else (vmax - vmin) / len(filtered_df)
        marks_vel = {}
        num_marks_vel = int((vmax - vmin) / vstep)
        for i in range(num_marks_vel):
            value = vmin + (vmax - vmin) * i / (num_marks - 1)
            rounded_value = round(value, 2)
            label = str(int(rounded_value)) if rounded_value.is_integer(
            ) else f"{rounded_value:.2f}".rstrip('0').rstrip('.')
            marks_vel[rounded_value] = {'label': label, 'style': {
                'fontSize': '11px', 'whiteSpace': 'nowrap'}}

        return tmin, tmax, [tmin, tmax], tstep, marks, \
            vmin, vmax, [vmin, vmax], vstep, marks_vel, \
            labeled_points, filtered_df.to_dict("records")

    @app.callback(
        Output('graph_x_y', 'figure'),
        Output('graph_x_z', 'figure'),
        Input('range-slider', 'value'),
        Input('velocity-slider', 'value'),
        State('selected-points-store', 'data'),
        State('selected-df', 'data')
    )
    def update_graphs(time_range, velocity_range, selectedpoints, filtered_dict):
        filtered_df = pd.DataFrame(filtered_dict)
        if time_range is not None:
            filtered_df = filtered_df[(filtered_df['Time'] >= time_range[0]) &
                                      (filtered_df['Time'] <= time_range[1])]
        if velocity_range is not None:
            filtered_df = filtered_df[(filtered_df['Velocity'] >= velocity_range[0]) &
                                      (filtered_df['Velocity'] <= velocity_range[1])]

        fig_xy = get_figure(filtered_df, x_axis="Range", y_axis="Azimuth", color='Velocity',
                            selectedpoints=filtered_df.index.get_indexer(selectedpoints))
        fig_xz = get_figure(filtered_df, x_axis="Range", y_axis="Elevation", color='Velocity',
                            selectedpoints=filtered_df.index.get_indexer(selectedpoints))

        return fig_xy, fig_xz

    @app.callback(
        Output('selected-points-store', 'data', allow_duplicate=True),
        Input('graph_x_y', 'selectedData'),
        Input('graph_x_z', 'selectedData'),
        State('selected-points-store', 'data'),
        State('selected-df', 'data'),
        State('range-slider', 'value'),
        State('velocity-slider', 'value'),
        prevent_initial_call=True
    )
    def add_mapped_points(selection_xy, selection_xz, selectedpoints_state, filtered_dict, time_range, velocity_range):
        filtered_df = pd.DataFrame(filtered_dict)
        if time_range is not None:
            filtered_df = filtered_df[(filtered_df['Time'] >= time_range[0]) &
                                      (filtered_df['Time'] <= time_range[1])]
            
        if velocity_range is not None:
            filtered_df = filtered_df[(filtered_df['Velocity'] >= velocity_range[0]) &
                                      (filtered_df['Velocity'] <= velocity_range[1])]
            
        selectedpoints_xy = [p["customdata"] for p in selection_xy.get(
            "points", [])] if selection_xy else []
        selectedpoints_xz = [p["customdata"] for p in selection_xz.get(
            "points", [])] if selection_xz else []

        return selectedpoints_state + selectedpoints_xy + selectedpoints_xz

    @app.callback(
        Output('graph_x_y', 'figure', allow_duplicate=True),
        Output('graph_x_z', 'figure', allow_duplicate=True),
        Input('selected-points-store', 'data'),
        State('selected-df', 'data'),
        State('range-slider', 'value'),
        State('velocity-slider', 'value'),

        prevent_initial_call=True
    )
    def plot_mapped_points(selectedpoints, filtered_dict, time_range, velocity_range):
        filtered_df = pd.DataFrame(filtered_dict)
        if time_range is not None:
            filtered_df = filtered_df[(filtered_df['Time'] >= time_range[0]) &
                                      (filtered_df['Time'] <= time_range[1])]
            
        if velocity_range is not None:
            filtered_df = filtered_df[(filtered_df['Velocity'] >= velocity_range[0]) &
                                      (filtered_df['Velocity'] <= velocity_range[1])]

        fig_xy = get_figure(filtered_df, x_axis="Range", y_axis="Azimuth", color='Velocity',
                            selectedpoints=filtered_df.index.get_indexer(selectedpoints))
        fig_xz = get_figure(filtered_df, x_axis="Range", y_axis="Elevation", color='Velocity',
                            selectedpoints=filtered_df.index.get_indexer(selectedpoints))

        return fig_xy, fig_xz

    @app.callback(
        Input('submit-button', 'n_clicks'),
        State('selected-points-store', 'data'),
        State('selected-df', 'data')
    )
    def save_annotation(n_clicks, selected_indexes, df_dict):
        if n_clicks is None:
            raise PreventUpdate

        df = pd.DataFrame(df_dict)
        session = SessionLocal()
        try:
            all_ids = df['Id'].tolist()
            selected_ids = df.loc[selected_indexes,
                                  'Id'].tolist() if selected_indexes else []
            if selected_ids:
                session.query(VRLI).filter(VRLI.data_id.in_(selected_ids)).update(
                    {VRLI.label: 1}, synchronize_session=False
                )

            remaining_ids = set(all_ids) - set(selected_ids)
            if remaining_ids:
                session.query(VRLI).filter(VRLI.data_id.in_(remaining_ids)).update(
                    {VRLI.label: 0}, synchronize_session=False
                )

            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

        return None

    @app.callback(
        Output('selected-points-store', 'data', allow_duplicate=True),
        Input('reset-button', 'n_clicks'),
        State('selected-df', 'data'),
        prevent_initial_call=True
    )
    def reset_annotation(n_clicks, filtered_dict):
        filtered_df = pd.DataFrame(filtered_dict)
        labeled_points = filtered_df.index[filtered_df['label'] == 1].tolist()
        return labeled_points

    @app.callback(
        Output('selected-points-store', 'data', allow_duplicate=True),
        Input('full-reset-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def full_reset_annotation(n_clicks):
        return []

    @app.callback(
        Output('stats-output', 'children'),
        Input('selected-points-store', 'data'),
        Input('range-slider', 'value'),
        Input('velocity-slider', 'value'),
        State('selected-df', 'data')
    )
    def update_stats(selectedpoints, time_range, slider_range, filtered_dict,):
        filtered_df = pd.DataFrame(filtered_dict)
        total_points = len(filtered_df)
        if time_range is not None:
            filtered_df = filtered_df[(filtered_df['Time'] >= time_range[0]) &
                                      (filtered_df['Time'] <= time_range[1])]

        if slider_range is not None:
            filtered_df = filtered_df[(filtered_df['Velocity'] >= slider_range[0]) &
                                      (filtered_df['Velocity'] <= slider_range[1])]

        mapped_points = len(set(selectedpoints))
        sliced_points = len(filtered_df)

        markdown_text = (
            f"* Выделено точек: {mapped_points}/{total_points}  \n"
            f"* Точек на временном срезе: {sliced_points}"
        )

        return dcc.Markdown(markdown_text)

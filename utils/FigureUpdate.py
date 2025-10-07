from utils.constants import DURATION
import plotly.graph_objects as go


def get_polar_ra(df, range_max, selectedpoints=[]):
    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=df["Range"],
            theta=df["Azimuth"],
            mode="markers",
            marker=dict(size=6, color="blue"),
            name="Range-Azimuth",
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(range=[0, range_max * 1.05]),
        ),
        uirevision="fixed",
    )

    fig.update_traces(showlegend=False)

    fig.update_traces(
        selectedpoints=selectedpoints,
        customdata=df.index,
        selected={"marker": {"opacity": 0.5, "size": 8, "color": "#379E4D"}},
        unselected={"marker": {"opacity": 0.5, "size": 8, "color": "#A32B2B"}},
    )

    fig.update_layout(
        margin={"l": 20, "r": 0, "b": 15, "t": 5},
        dragmode="lasso",
        hovermode=False,
        newselection_mode="immediate",
        transition_duration=DURATION,
    )

    return fig


def get_polar_re(df, range_max, selectedpoints=[]):
    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=df["Range"],
            theta=df["Elevation"],
            mode="markers",
            marker=dict(size=10, color="blue"),
            name="Range-Elevation",
        )
    )

    fig.update_traces(
        selectedpoints=selectedpoints,
        customdata=df.index,
        selected={"marker": {"opacity": 0.5, "size": 8, "color": "#379E4D"}},
        unselected={"marker": {"opacity": 0.5, "size": 8, "color": "#A32B2B"}},
    )

    fig.update_layout(
        margin={"l": 20, "r": 0, "b": 15, "t": 5},
        dragmode="lasso",
        hovermode=False,
        newselection_mode="immediate",
        transition_duration=DURATION,
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(range=[0, range_max]),
        ),
        uirevision="fixed",
    )
    fig.update_traces(showlegend=False)
    return fig


# def expand_range_max(max_val, pad_ratio=0.05):

#     if max_val is None:
#         return [0, 1]

#     if max_val == 0:
#         return [0, 1]  # защита от деления на ноль

#     pad = max_val * pad_ratio
#     return [0, max_val + pad]

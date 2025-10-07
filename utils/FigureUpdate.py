import plotly.express as px
import numpy as np
from utils.constants import DURATION


def get_figure(df, x_axis, y_axis, color, selectedpoints=[]):
    fig = px.scatter(df, x=x_axis, y=y_axis, template="seaborn",
                     color_continuous_scale=px.colors.sequential.Cividis)

    fig.update_traces(
        selectedpoints=selectedpoints,
        customdata=df.index,

        selected={"marker": {"opacity": 0.9, 
                            "size": 15,
                            "color": "#379E4D"}},
        unselected={"marker": {"opacity": 0.3, 
                               "size": 15,
                               "color": "#A32B2B"
                               }},
    )

    fig.update_layout(
        margin={"l": 20, "r": 0, "b": 15, "t": 5},
        dragmode="lasso",
        hovermode=False,
        newselection_mode="immediate",
        transition_duration=DURATION
    )

    return fig


from utils.models import VRLI
import pandas as pd


def get_df(session, selected_name):
    data = session.query(VRLI).filter(VRLI.filename == selected_name).all()

    times = [row.time for row in data]
    azimuths = [row.azimuth for row in data]
    ranges = [row.range_ for row in data]
    ids = [row.data_id for row in data]
    elevations = [row.elevation for row in data]
    labels = [row.label for row in data]
    velocity = [row.velocity for row in data]
    dct = {
        "Time": times,
        "Range": ranges,
        "Azimuth": azimuths,
        "Elevation": elevations,
        "label": labels,
        "Id": ids,
        "Velocity": velocity,
    }

    df = pd.DataFrame(dct)
    df = df.set_index("Id")
    return df

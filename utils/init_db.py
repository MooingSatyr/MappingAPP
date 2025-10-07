import pandas as pd
from models import Base, engine, SessionLocal, VRLI

# Создать таблицы заново
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Читаем Excel
df = pd.read_excel("D:/Projects/mapping_app/marks.xlsx")


df = df.rename(
    columns={
        "Time": "time",
        "Range": "range_",
        "Azimuth": "azimuth",
        "Elevation": "elevation",
        "FileName": "filename",
        "File Size, Мб": "file_size_mb",
        "label": "label",
        "velocity": "velocity",
        "Id": "data_id",
    }
)


# Заливаем данные
session = SessionLocal()
records = [VRLI(**row) for row in df.to_dict(orient="records")]
session.bulk_save_objects(records)
session.commit()
session.close()

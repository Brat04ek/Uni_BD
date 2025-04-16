"""insert data from csv weather_record table

Revision ID: 7bf661a1d662
Revises: c9c5a4d5a64a
Create Date: 2025-04-16 11:55:08.041528

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7bf661a1d662'
down_revision: Union[str, None] = 'c9c5a4d5a64a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from models import WeatherRecord, WindDirectionEnum  
from sqlalchemy.orm import Session
from datetime import datetime
import csv

def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    path = r'C:\Users\Danylo\Documents\University\bd\lab3\GlobalWeatherRepository.csv'
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        records = []

        for row in reader:
            record = WeatherRecord(
                country=row["country"],
                wind_degree=int(row["wind_degree"]),
                wind_kph=float(row["wind_kph"]),
                wind_direction=WindDirectionEnum[row["wind_direction"]],
                last_updated=datetime.strptime(row["last_updated"], "%Y-%m-%d %H:%M").date(),

                air_quality_Carbon_Monoxide=float(row["air_quality_Carbon_Monoxide"]),
                air_quality_Ozone=float(row["air_quality_Ozone"]),
                air_quality_Nitrogen_dioxide=float(row["air_quality_Nitrogen_dioxide"]),
                air_quality_Sulphur_dioxide=float(row["air_quality_Sulphur_dioxide"]),
                air_quality_PM2=float(row["air_quality_PM2.5"]),
                air_quality_PM10=float(row["air_quality_PM10"]),
                air_quality_us_epa_index=int(row["air_quality_us-epa-index"]),
                air_quality_gb_defra_index=int(row["air_quality_gb-defra-index"]),
            )
            records.append(record)

        session.add_all(records)
        session.commit()


def downgrade() -> None:
    op.execute(f"DELETE FROM weather_record;")
    
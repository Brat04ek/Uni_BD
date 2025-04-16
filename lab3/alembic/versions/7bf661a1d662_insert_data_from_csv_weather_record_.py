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
    conn = op.get_bind()
    csv_path = r'C:\Users\Danylo\Documents\University\bd\lab3\GlobalWeatherRepository.csv'
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            wind_dir = row['wind_direction']
            conn.execute(
                sa.text("""
                    INSERT INTO weather_record (
                        country, wind_degree, wind_kph, wind_direction,
                        last_updated, "air_quality_Carbon_Monoxide",
                        "air_quality_Ozone", "air_quality_Nitrogen_dioxide",
                        "air_quality_Sulphur_dioxide", "air_quality_PM2",
                        "air_quality_PM10", air_quality_us_epa_index,
                        air_quality_gb_defra_index
                    ) VALUES (
                        :country, :wind_degree, :wind_kph, :wind_direction,
                        :last_updated, :co, :ozone, :no2,
                        :so2, :pm2, :pm10, :epa, :gb
                    )
                """),
                {
                    'country': row['country'],
                    'wind_degree': int(row['wind_degree']),
                    'wind_kph': float(row['wind_kph']),
                    'wind_direction': wind_dir,
                    'last_updated': datetime.strptime(row['last_updated'], '%Y-%m-%d %H:%M').date(),
                    'co': float(row['air_quality_Carbon_Monoxide']),
                    'ozone': float(row['air_quality_Ozone']),
                    'no2': float(row['air_quality_Nitrogen_dioxide']),
                    'so2': float(row['air_quality_Sulphur_dioxide']),
                    'pm2': float(row['air_quality_PM2.5']),
                    'pm10': float(row['air_quality_PM10']),
                    'epa': int(row['air_quality_us-epa-index']),
                    'gb': int(row['air_quality_gb-defra-index'])
                }
            )


def downgrade() -> None:
    op.execute(f"DELETE FROM weather_record;")
    
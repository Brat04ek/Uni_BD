from models import WeatherRecord
from sqlalchemy.orm import joinedload, Session
from sqlalchemy import create_engine,  select


def get_full_weather_info(session, country_name, target_date):
    sql_statement = (
        select(WeatherRecord)
        .options(joinedload(WeatherRecord.air_quality))
        .where(
            WeatherRecord.country == country_name,
            WeatherRecord.last_updated == target_date
        )
    )
    try:
        results = session.scalars(sql_statement).all()
    except:
        return None
    return results



if __name__ == "__main__":
        
    db_url = "postgresql://postgres:postgres@localhost/lab-3"
    engine = create_engine(db_url)

    country = input('Enter country name:       ')
    date = input('Enter date (YYYY-MM-DD):  ')

    with Session(engine) as session:
        results = get_full_weather_info(session, country, date)

    if not results:
        print("\nNo data found")
    else:
        for record in results:
            print("\n=== Weather Record ===")
            print(
                f"ID: {record.id}, Country: {record.country}, Wind: {record.wind_kph} kph,\n"
                f"Direction: {record.wind_direction}, Degree: {record.wind_degree}, "
                f"Date: {record.last_updated}"
            )
            if record.air_quality:
                aq = record.air_quality
                print(f"Carbon_Monoxide: {aq.air_quality_Carbon_Monoxide}, Ozone: {aq.air_quality_Ozone},")
                print(f"Nitrogen_dioxide: {aq.air_quality_Nitrogen_dioxide}, Sulphur_dioxide: {aq.air_quality_Sulphur_dioxide},")
                print(f"PM2.5: {aq.air_quality_PM2}, PM10: {aq.air_quality_PM10},")
                print(f"us_epa_index: {aq.air_quality_us_epa_index}, gb_defra_index: {aq.air_quality_gb_defra_index},")
            else:
                print("No Air Quality data found.")

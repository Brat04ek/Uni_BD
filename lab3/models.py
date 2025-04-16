import enum
from datetime import date

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, Enum, Date, ForeignKey, Boolean

# Базовий клас
class Base(DeclarativeBase):
    pass

# Enum для напрямків вітру
class WindDirectionEnum(enum.Enum):
    N = "N"
    NNE = "NNE"
    NE = "NE"
    ENE = "ENE"
    E = "E"
    ESE = "ESE"
    SE = "SE"
    SSE = "SSE"
    S = "S"
    SSW = "SSW"
    SW = "SW"
    WSW = "WSW"
    W = "W"
    WNW = "WNW"
    NW = "NW"
    NNW = "NNW"


class WeatherRecord(Base):
    __tablename__ = "weather_record"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    country: Mapped[str] = mapped_column(String)
    wind_degree: Mapped[int] = mapped_column(Integer)
    wind_kph: Mapped[float] = mapped_column(Float)
    wind_direction: Mapped[WindDirectionEnum] = mapped_column(Enum(WindDirectionEnum))
    last_updated: Mapped[date] = mapped_column(Date)

    air_quality: Mapped["AirQuality"] = relationship(
        back_populates="weather", cascade="all, delete-orphan"
    )

class AirQuality(Base):
    __tablename__ = "air_quality"
    
    id: Mapped[int] = mapped_column(ForeignKey("weather_record.id"), primary_key=True)

    air_quality_Carbon_Monoxide : Mapped[float] = mapped_column(Float)
    air_quality_Ozone : Mapped[float] = mapped_column(Float)
    air_quality_Nitrogen_dioxide : Mapped[float] = mapped_column(Float)
    air_quality_Sulphur_dioxide : Mapped[float] = mapped_column(Float)
    air_quality_PM2 : Mapped[float] = mapped_column(Float)
    air_quality_PM10 : Mapped[float] = mapped_column(Float)
    air_quality_us_epa_index : Mapped[int] = mapped_column(Integer)
    air_quality_gb_defra_index : Mapped[int] = mapped_column(Integer)

    worth_go_outside: Mapped[bool] = mapped_column(Boolean,  nullable=False, server_default="False")

    weather : Mapped["WeatherRecord"] = relationship(back_populates="air_quality")
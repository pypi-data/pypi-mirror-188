"""Type definitions for NAM."""
from dataclasses import dataclass
from typing import Optional

import aiohttp


@dataclass
class ConnectionOptions:
    """Options for NAM."""

    host: str
    username: Optional[str] = None
    password: Optional[str] = None
    auth: Optional[aiohttp.BasicAuth] = None

    def __post_init__(self) -> None:
        """Call after initialization."""
        if self.username is not None:
            if self.password is None:
                raise ValueError("Supply both username and password")

            object.__setattr__(
                self, "auth", aiohttp.BasicAuth(self.username, self.password)
            )


@dataclass(frozen=True)
class NAMSensors:
    """Data class for NAM sensors."""

    bme280_humidity: Optional[float]
    bme280_pressure: Optional[float]
    bme280_temperature: Optional[float]
    bmp180_pressure: Optional[float]
    bmp180_temperature: Optional[float]
    bmp280_pressure: Optional[float]
    bmp280_temperature: Optional[float]
    dht22_humidity: Optional[float]
    dht22_temperature: Optional[float]
    heca_humidity: Optional[float]
    heca_temperature: Optional[float]
    mhz14a_carbon_dioxide: Optional[float]
    pms_caqi: Optional[int]
    pms_caqi_level: Optional[str]
    pms_p0: Optional[float]
    pms_p1: Optional[float]
    pms_p2: Optional[float]
    sds011_caqi: Optional[int]
    sds011_caqi_level: Optional[str]
    sds011_p1: Optional[float]
    sds011_p2: Optional[float]
    sht3x_humidity: Optional[float]
    sht3x_temperature: Optional[float]
    signal: Optional[float]
    sps30_caqi: Optional[int]
    sps30_caqi_level: Optional[str]
    sps30_p0: Optional[float]
    sps30_p1: Optional[float]
    sps30_p2: Optional[float]
    sps30_p4: Optional[float]
    uptime: Optional[int]

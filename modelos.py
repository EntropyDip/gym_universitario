"""Entidades del gimnasio y utilidades de fecha."""
from dataclasses import dataclass
from datetime import datetime, timedelta

from excepciones import (
    DatoVacioError,
    DuracionInvalidaError,
    FechaInvalidaError,
)      

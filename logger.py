import json
from enum import StrEnum
from dataclasses import dataclass
from datetime import tzinfo, datetime
import base64
from pathlib import Path

from export_builder import JsonExportBuilder, TxtExportBuilder, ExportDirector


class Level(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ExportFormat(StrEnum):
    TXT = "txt"
    JSON = "json"


@dataclass
class Config:
    timezone: tzinfo | None
    level: Level = "INFO"
    encode: bool = False


class Logger:
    def __init__(self, config: Config):
        self.config = config
        self.base_path = Path(__file__).parent

    def log(self, message: str):
        today = datetime.now()
        if today.weekday() < 5:
            path = self.base_path / f"log{today.strftime('%Y-%m-%d')}.txt"
        else:
            path = self.base_path / "weekend.txt"

        if self.config.encode:
            message = base64.b64encode(message.encode())
        if self.config.timezone:
            today = today.astimezone(self.config.timezone)

        with open(path, "a") as f:
            f.write(f'{message} / {today.strftime("%Y-%m-%d %H:%M:%S")}')

    def export(self, name: str, date: str, export_format: ExportFormat):
        builder = None
        path = self.base_path / f"log{date}.txt"
        with open(path, "r") as f:
            data = json.loads(f.read())

        match export_format:
            case ExportFormat.TXT:
                builder = TxtExportBuilder(data)
            case ExportFormat.JSON:
                builder = JsonExportBuilder(data)

        if builder:
            director = ExportDirector(builder)
            log = director.build_log()
            with open(self.base_path / f"{name}.{export_format}", "w") as f:
                f.write(log)

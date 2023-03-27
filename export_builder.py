import json
from abc import ABC, abstractmethod


class ExportBuilder(ABC):
    @abstractmethod
    def build_level(self):
        pass

    @abstractmethod
    def build_event(self):
        pass

    @abstractmethod
    def build_message(self):
        pass

    @abstractmethod
    def build_date(self):
        pass

    @abstractmethod
    def get_log(self):
        pass


class TxtExportBuilder(ExportBuilder):
    def __init__(self, data: dict):
        self.data = data
        self.log = ""

    def build_level(self):
        self.log += f"Level: {self.data['level']}"

    def build_event(self):
        self.log += f"Event: {self.data['event']}\n"

    def build_message(self):
        self.log += f"Message: {self.data['message']}\n"

    def build_date(self):
        self.log += f"Date: {self.data['date']}\n"

    def get_log(self):
        return self.log


class JsonExportBuilder(ExportBuilder):
    def __init__(self, data: dict):
        self.data = data
        self.log = {}

    def build_level(self):
        self.log["level"] = self.data["level"]

    def build_event(self):
        self.log["event"] = self.data["event"]

    def build_message(self):
        self.log["message"] = self.data["message"]

    def build_date(self):
        self.log["date"] = self.data["date"]

    def get_log(self):
        return json.dumps(self.log)


class ExportDirector:
    def __init__(self, builder: ExportBuilder):
        self.builder = builder

    def build_log(self):
        self.builder.build_level()
        self.builder.build_event()
        self.builder.build_message()
        self.builder.build_date()
        return self.builder.get_log()

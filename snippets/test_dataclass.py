from dataclasses import  dataclass
from logging import LogRecord


@dataclass
class LogData:
    name: str
    value: str = None

    def __init__(self, record: LogRecord):
        self.name = record.__dict__.get('name')


record = {
    "name": "acme",
    "level": "WARNING",
    "pathname": "/",
    "lineno": 12,
    "msg": "hello world!",
    "args": (),
    "exc_info": None
}

record = LogRecord(**record)
log_data = LogData(record)
print(log_data.__dict__)
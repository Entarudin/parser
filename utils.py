import json
from datetime import datetime


class DateTimeEncoder(json.JSONEncoder):
    def default(self, date):
        if isinstance(date, datetime):
            return date.isoformat()
        if isinstance(date, bytes):
            return list(date)
        return json.JSONEncoder.default(self, date)

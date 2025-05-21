from datetime import datetime


class Time:
    @staticmethod
    def get_date():
        now = datetime.now().astimezone()
        formatted_time = now.strftime("%a %b %d %H:%M:%S %Y %z")
        return formatted_time

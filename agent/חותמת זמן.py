from datetime import datetime


def timestamp():
    return f"\n***** {datetime.now().strftime('date: %Y-%m-%d  time: %H:%M:%S')} *****"

print(timestamp())

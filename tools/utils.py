import datetime

def info(s: str) -> None:
    ts = datetime.datetime.now().replace(microsecond=0).isoformat()
    print(ts + ': ' + s)


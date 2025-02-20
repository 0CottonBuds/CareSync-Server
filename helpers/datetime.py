
def convert_str_time_to_minutes(time: str):
    hours, minutes = time.split(":")
    return int(hours) * 60 + int(minutes)

def convert_minutes_to_str_time(minutes: int):
    hours = minutes // 60
    minutes = minutes % 60

    return f"{hours:2}:{minutes:2}"
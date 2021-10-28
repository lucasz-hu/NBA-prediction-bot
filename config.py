from datetime import datetime, time

season = 2022
test_time = int(round(datetime.now().timestamp()))
test_time_datetime = datetime.fromtimestamp(test_time)
test_time_datetime = datetime.combine(test_time_datetime, time.min) 
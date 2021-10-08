from datetime import datetime, time

season = 2021
test_time = 1617269986
test_time_datetime = datetime.fromtimestamp(test_time)
test_time_datetime = datetime.combine(test_time_datetime, time.min) 
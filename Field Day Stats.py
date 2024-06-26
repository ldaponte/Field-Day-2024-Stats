import csv
from datetime import datetime, timedelta
import time
from dateutil import tz
import numpy as np

contest_period = np.zeros(1440, dtype=np.int64)
contest_period_times = []

from_zone = tz.tzutc()
to_zone = tz.tzlocal()

start_time = datetime.strptime('06/22/24 11:00:00', '%m/%d/%y %H:%M:%S')
start_time = start_time.replace(tzinfo=to_zone)

# print(time.mktime(start_time.timetuple()))

with open('data/W7AVM Field Day 2024 ARRL-FD.csv') as csvfile:

    reader = csv.DictReader(csvfile)
    for row in reader:
        # print(row['qso_date'], row['time_on'], row['band'], row['mode'], row['operator'])
        ds = row['qso_date']
        ts = row['time_on']

        date_time_string = '{}/{}/{} {}:{}:{}'.format(ds[4:6], ds[6:8], ds[2:4], ts[0:2], ts[2:4], ts[4:6])

        datetime_object = datetime.strptime(date_time_string, '%m/%d/%y %H:%M:%S')

        datetime_object = datetime_object.replace(tzinfo=from_zone)
        local_time = datetime_object.astimezone(to_zone)

        # print(local_time, time.mktime(local_time.timetuple()))  # printed in default format

        # print(time.mktime(local_time.timetuple()) - time.mktime(start_time.timetuple()))

        # print(int((local_time - start_time).total_seconds() / 60))

        minute = int((local_time - start_time).total_seconds() / 60)
        contest_period[minute] = contest_period[minute] + 1

start = 0
end = 0

minute_time = start_time

for i in range(1440):
    contest_period_times.append(minute_time)
    minute_time = minute_time + timedelta(minutes=1) 

with open('rates.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
    for i in range(1440):
        writer.writerow([contest_period_times[i], np.sum(contest_period[start:end])])
        print(contest_period_times[i], start, end, np.sum(contest_period[start:end]))
        
        if end > 59:
            start = start + 1

        end = end + 1

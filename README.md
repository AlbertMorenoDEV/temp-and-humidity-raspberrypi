# temp-and-humidity-raspberrypi

## /etc/supervisor/conf.d/temp_and_humidity.conf
```
[program:temp_and_humidity_sensor_reader]
command = /usr/bin/python sensor_reader.py
directory = /home/pi/Projects/temp-and-humidity
user = root
autostart = true
autorestart = true
startretries = 10
priority = 998
stdout_logfile = /var/log/supervisor/temp_and_humidity_sensor_reader.log
stderr_logfile = /var/log/supervisor/temp_and_humidity_sensor_reader_err.log
environment = SENSOR_NAME="pis-barcelona"

[program:temp_and_humidity_csv_updater]
command = /usr/bin/python csv_updater.py
directory = /home/pi/Projects/temp-and-humidity
user = pi
autostart = true
autorestart = true
startretries = 10
stdout_logfile = /var/log/supervisor/temp_and_humidity_csv_updater.log
stderr_logfile = /var/log/supervisor/temp_and_humidity_csv_updater_err.log
environment = SENSOR_NAME="pis-barcelona"

[program:temp_and_humidity_sns_publisher]
command = /usr/bin/python sns_publisher.py
directory = /home/pi/Projects/temp-and-humidity
user = pi
autostart = true
autorestart = true
startretries = 10
stdout_logfile = /var/log/supervisor/temp_and_humidity_sns_publisher.log
stderr_logfile = /var/log/supervisor/temp_and_humidity_sns_publisher_err.log

[program:temp_and_humidity_telegram_anomaly_alerter]
command = /usr/bin/python telegram_anomaly_alerter.py
directory = /home/pi/Projects/temp-and-humidity
user = pi
autostart = true
autorestart = true
startretries = 10
stdout_logfile = /var/log/supervisor/temp_and_humidity_telegram_anomaly_alerter.log
stderr_logfile = /var/log/supervisor/temp_and_humidity_telegram_anomaly_alerter_err.log

[program:temp_and_humidity_webserver]
command = /usr/bin/node webserver.js
directory = /home/pi/Projects/temp-and-humidity
user = pi
autostart = true
autorestart = true
startretries = 10
stdout_logfile = /var/log/supervisor/temp_and_humidity_webserver.log
stderr_logfile = /var/log/supervisor/temp_and_humidity_webserver_err.log
```

`sudo service supervisor restart`

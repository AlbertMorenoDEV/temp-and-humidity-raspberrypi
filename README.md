# temp-and-humidity-raspberrypi

## /etc/supervisor/conf.d/temp_and_humidity.conf
```
[program:temp_and_humidity_sensor_reader]
command = /usr/bin/python sensor_reader.py
directory = /home/pi/Projects/temp-and-humidity
user = root
autostart = true
autorestart = true
stdout_logfile = /var/log/supervisor/temp_and_humidity_sensor_reader.log
stderr_logfile = /var/log/supervisor/temp_and_humidity_sensor_reader_err.log
environment = SENSOR_NAME="pis-barcelona"

[program:temp_and_humidity_csv_updater]
command = /usr/bin/python csv_updater.py
directory = /home/pi/Projects/temp-and-humidity
user = pi
autostart = true
autorestart = true
stdout_logfile = /var/log/supervisor/temp_and_humidity_csv_updater.log
stderr_logfile = /var/log/supervisor/temp_and_humidity_csv_updater_err.log
environment = SENSOR_NAME="pis-barcelona"

[program:temp_and_humidity_webserver]
command = /usr/bin/node webserver.js
directory = /home/pi/Projects/temp-and-humidity
user = pi
autostart = true
autorestart = true
stdout_logfile = /var/log/supervisor/temp_and_humidity_webserver.log
stderr_logfile = /var/log/supervisor/temp_and_humidity_webserver_err.log
```

`sudo service supervisor restart`

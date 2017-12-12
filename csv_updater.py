#!/usr/bin/env python
import os, sys, Adafruit_DHT, time, pika, json
from datetime import datetime, date

sensor                       = Adafruit_DHT.AM2302 #DHT11/DHT22/AM2302
pin                          = 4
sensor_name                  = os.getenv('SENSOR_NAME', 'pi')
csv_folder                   = "csv"
hist_temperature_file_path   = csv_folder + "/temperature_" + sensor_name + "_log_" + str(date.today().year) + ".csv"
latest_temperature_file_path = csv_folder + "/temperature_" + sensor_name + "_latest_value.csv"
hist_humidity_file_path      = csv_folder + "/humidity_" + sensor_name + "_log_" + str(date.today().year) + ".csv"
latest_humidity_file_path    = csv_folder + "/humidity_" + sensor_name + "_latest_value.csv"
csv_header_temperature       = "timestamp,temperature_in_celsius\n"
csv_header_humidity          = "timestamp,relative_humidity\n"
csv_entry_format             = "{0},{1}\n"
sec_between_log_entries      = 60

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='temp_and_humidity',
                         exchange_type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='temp_and_humidity',
                   queue=queue_name)

def write_header(file_handle, csv_header):
  file_handle.write(csv_header)

def write_value(file_handle, datetime, value):
  line = csv_entry_format.format(datetime, value)
  file_handle.write(line)
  file_handle.flush()

def open_file_ensure_header(file_path, mode, csv_header):
  f = open(file_path, mode, os.O_NONBLOCK)
  if os.path.getsize(file_path) <= 0:
    write_header(f, csv_header)
  return f

def write_latest_value(datetime, temperature, humidity):
  with open_file_ensure_header(latest_temperature_file_path, 'w', csv_header_temperature) as f_latest_value:  #open and truncate
    write_value(f_latest_value, datetime, temperature)
  with open_file_ensure_header(latest_humidity_file_path, 'w', csv_header_humidity) as f_latest_value:  #open and truncate
    write_value(f_latest_value, datetime, humidity)

f_hist_temp = open_file_ensure_header(hist_temperature_file_path, 'a', csv_header_temperature)
f_hist_hum  = open_file_ensure_header(hist_humidity_file_path, 'a', csv_header_humidity)

def callback(ch, method, properties, body):
  data = json.loads(body)
  print body
  write_latest_value(data["datetime"], data["temperature"], data["humidity"])
  write_value(f_hist_temp, data["datetime"], data["temperature"])
  write_value(f_hist_hum, data["datetime"], data["humidity"])
  
channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

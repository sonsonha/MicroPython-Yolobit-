# -*- coding: utf-8 -*-
"""
Yolobit MicroPython - Template RTOS (VSCode).
Dùng event_manager (OhStem): mỗi task nằm trong file riêng (task1.py, task2.py, ...),
có task_init() và task_run(); task_run() được add vào event_manager.add_timer_event().

Cách thêm task mới:
  1. Tạo file taskN.py với status toàn cục, task_init(), task_run().
  2. Trong config.py: thêm INTERVAL_TASKN_MS.
  3. Trong main.py: gọi taskN.task_init(); event_manager.add_timer_event(..., taskN.task_run).
"""

import time
from event_manager import *
import config
import task1
import task2
import task_mqtt
import task_ntp
import task_aiot
import task_event

# Khởi tạo event manager
event_manager.reset()

# Gọi task_init()
task1.task_init()
task2.task_init()
task_mqtt.task_init()
task_ntp.task_init()
task_aiot.task_init()
task_event.task_init()

# Đăng ký task_run() của từng task vào event_manager (timer event)
event_manager.add_timer_event(config.INTERVAL_TASK1_MS, task1.task_run)
event_manager.add_timer_event(config.INTERVAL_TASK2_MS, task2.task_run)
event_manager.add_timer_event(config.INTERVAL_TASK_MQTT_MS, task_mqtt.task_run)
event_manager.add_timer_event(config.INTERVAL_TASK_NTP_MS, task_ntp.task_run)
event_manager.add_timer_event(config.INTERVAL_TASK_AIOT_MS, task_aiot.task_run)
event_manager.add_timer_event(config.INTERVAL_TASK_EVENT_MS, task_event.task_run)

# In ra serial (Serial Monitor 115200)
print("Yolobit event_manager - bat dau.")

while True:
    event_manager.run()
    time.sleep_ms(10)

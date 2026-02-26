# -*- coding: utf-8 -*-
"""
Chương trình chính - Yolobit MicroPython (VSCode).
Dùng thư viện event_manager của OhStem: đăng ký timer event, vòng lặp gọi event_manager.run().
Code tương đương với code do app OhStem sinh ra khi lập trình kéo thả.

Cách thêm task mới:
  1. Trong tasks.py: viết callback on_event_timer_callback_<tên>().
  2. Trong config.py: thêm INTERVAL_xxx_MS nếu cần.
  3. Ở dưới: gọi event_manager.add_timer_event(interval_ms, tasks.on_event_timer_callback_<tên>).
"""

import time
from event_manager import *
import config
import tasks

# Gán config cho module tasks (LED, ...)
tasks.set_config(config)

# Khởi tạo event manager (chuẩn OhStem)
event_manager.reset()

# --- Đăng ký timer event (giống code kéo thả OhStem sinh ra) ---
# Task 1: in "Xin chào!" mỗi INTERVAL_PRINT_HELLO_MS
event_manager.add_timer_event(
    config.INTERVAL_PRINT_HELLO_MS,
    tasks.on_event_timer_callback_print_hello
)
# Task 2: chớp LED mỗi INTERVAL_LED_BLINK_MS
event_manager.add_timer_event(
    config.INTERVAL_LED_BLINK_MS,
    tasks.on_event_timer_callback_blink_led
)
# Thêm task: event_manager.add_timer_event(interval_ms, tasks.on_event_timer_callback_xxx)

# In ra serial khi chạy (Serial Monitor 115200)
print("Yolobit event_manager - bat dau.")

# Vòng lặp chính: chạy event manager (giống code kéo thả OhStem)
while True:
    event_manager.run()
    time.sleep_ms(10)

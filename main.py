# -*- coding: utf-8 -*-
"""
Chương trình chính - Yolobit MicroPython (VSCode).
Tổ chức theo hướng RTOS: nhiều task chạy theo chu kỳ, tương thích với thư viện OhStem.

Cách thêm task mới:
  1. Trong tasks.py: viết hàm mới (ví dụ task_my_sensor).
  2. Trong config.py: thêm INTERVAL_xxx_MS nếu cần.
  3. Ở dưới đây: thêm (interval_ms, task_my_sensor) vào danh sách TASKS.
"""

import time
import config
import tasks

# Gán config cho module tasks (để task_blink_led biết dùng LED nào)
tasks.set_config(config)

# --- Danh sách task: (chu kỳ ms, hàm task) ---
# Scheduler sẽ gọi mỗi task khi đủ chu kỳ.
TASKS = [
    (config.INTERVAL_PRINT_HELLO_MS, tasks.task_print_hello),
    (config.INTERVAL_LED_BLINK_MS, tasks.task_blink_led),
    # Thêm task của bạn ở đây, ví dụ:
    # (2000, tasks.task_do_something),
]


def run_scheduler():
    """Vòng lặp chính: chạy từng task theo chu kỳ (mô phỏng RTOS)."""
    n = len(TASKS)
    last_run = [0] * n  # Thời điểm chạy gần nhất (ms) của từng task

    while True:
        now = time.ticks_ms()
        for i in range(n):
            interval_ms, task_fn = TASKS[i]
            if interval_ms <= 0:
                continue
            if time.ticks_diff(now, last_run[i]) >= interval_ms:
                try:
                    task_fn()
                except Exception as e:
                    print("Task error:", e)
                last_run[i] = now
        time.sleep_ms(10)  # Tránh chiếm 100% CPU


def setup():
    """
    Khởi tạo một lần trước khi chạy scheduler.
    Gọi các lệnh setup phần cứng (LED, serial, ...) tại đây.
    """
    # In ra serial để biết chương trình đã chạy (mở Serial Monitor 115200 để xem)
    print("Yolobit RTOS template - bat dau.")
    # Có thể gọi thêm: khởi tạo cảm biến, display, ...
    # tasks._get_led_pin() sẽ được gọi lần đầu khi task_blink_led chạy.


def main():
    setup()
    run_scheduler()


if __name__ == "__main__":
    main()

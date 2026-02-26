# -*- coding: utf-8 -*-
"""
Cấu hình cho project Yolobit - MicroPython (VSCode).
Chỉnh các tham số tại đây thay vì sửa trong main.py.
Tương thích với thiết bị và thư viện OhStem (code kéo thả).
"""

# --- LED ---
# Dùng LED trên board (nếu có): đặt USE_BUILTIN_LED = True và LED_GPIO = số chân GPIO (ví dụ 2 với nhiều board ESP32).
# Dùng LED ngoài qua chân mở rộng: đặt USE_BUILTIN_LED = False và dùng PIN_LED (P0, P1, P2, ... như trong app OhStem).
USE_BUILTIN_LED = False
LED_GPIO = 2  # Chỉ dùng khi USE_BUILTIN_LED = True (LED tích hợp trên board).
PIN_LED = "pin0"  # Chỉ dùng khi USE_BUILTIN_LED = False; tên pin giống trong yolobit: pin0, pin1, pin2, ...

# --- Chu kỳ task (milli giây) ---
INTERVAL_PRINT_HELLO_MS = 1000   # In "Xin chào!" mỗi 1 giây.
INTERVAL_LED_BLINK_MS = 500      # Chớp LED mỗi 0.5 giây.

# --- Serial / Terminal ---
# print() sẽ xuất ra UART. Mở Serial Monitor trong app OhStem hoặc VSCode (baud thường 115200) để xem.
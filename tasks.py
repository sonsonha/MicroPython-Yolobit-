# -*- coding: utf-8 -*-
"""
Các task chạy theo lịch (kiểu RTOS).
Mỗi task là một hàm không tham số; scheduler sẽ gọi theo chu kỳ đã cấu hình.
Chỉ dùng thư viện mà Yolobit/OhStem hỗ trợ (yolobit, time, machine, ...).
"""

import time

# Sẽ được gán trong main sau khi import yolobit và config
_config = None
_led_pin = None
_led_state = 0  # Trạng thái LED để chớp (0/1)


def _get_led_pin():
    """Khởi tạo đối tượng LED (built-in hoặc qua yolobit pin) một lần."""
    global _led_pin, _config
    if _led_pin is not None:
        return _led_pin
    if _config.USE_BUILTIN_LED:
        from machine import Pin
        _led_pin = Pin(_config.LED_GPIO, Pin.OUT)
    else:
        import yolobit
        _led_pin = getattr(yolobit, _config.PIN_LED)
    return _led_pin


def task_print_hello():
    """
    Task 1: In ra terminal/serial dòng chữ "Xin chào!" mỗi chu kỳ.
    Xem trên Serial Monitor (app OhStem hoặc VSCode, baud 115200).
    """
    print("Xin chào!")


def task_blink_led():
    """
    Task 2: Chớp tắt LED (đảo trạng thái mỗi lần gọi).
    LED có thể là LED trên board hoặc LED nối vào chân P0 (xem config.py).
    Tương thích yolobit: write_digital(0/1) hoặc write_analog(0/1023).
    """
    global _led_state
    led = _get_led_pin()
    try:
        if hasattr(led, "write_digital"):
            _led_state = 1 - _led_state
            led.write_digital(_led_state)
        elif hasattr(led, "write_analog"):
            _led_state = 1 - _led_state
            led.write_analog(1023 if _led_state else 0)
        else:
            led.value(1 - led.value())
    except Exception as e:
        print("LED error:", e)


def set_config(cfg):
    """Gán config từ main (để tasks dùng USE_BUILTIN_LED, PIN_LED, ...)."""
    global _config
    _config = cfg

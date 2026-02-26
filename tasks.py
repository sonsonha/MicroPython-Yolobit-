# -*- coding: utf-8 -*-
"""
Các callback cho event_manager (OhStem).
Dùng thư viện event_manager của OhStem: mỗi "task" là timer event callback,
đăng ký bằng event_manager.add_timer_event(interval_ms, callback).
Đặt tên hàm callback theo chuẩn: on_event_timer_callback_<mô tả>.
Chỉ dùng thư viện Yolobit/OhStem hỗ trợ (yolobit, time, machine, ...).
"""

import time

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


def on_event_timer_callback_print_hello():
    """
    Timer event callback: in ra serial "Xin chào!" mỗi chu kỳ.
    Xem trên Serial Monitor (app OhStem hoặc VSCode, baud 115200).
    """
    print("Xin chào!")


def on_event_timer_callback_blink_led():
    """
    Timer event callback: chớp tắt LED (đảo trạng thái mỗi lần gọi).
    LED: onboard hoặc chân P0 (xem config.py).
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
    """Gán config từ main (để callbacks dùng USE_BUILTIN_LED, PIN_LED, ...)."""
    global _config
    _config = cfg

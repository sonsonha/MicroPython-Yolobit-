# Yolobit MicroPython – Template RTOS (VSCode)

Template lập trình **MicroPython** cho **Yolo:Bit** (OhStem) trên **VSCode**, tổ chức theo hướng **nhiều task** chạy theo chu kỳ (giống RTOS). Tương thích với thư viện và cách đặt tên chân của **code kéo thả OhStem** (app.ohstem.vn).

## Yêu cầu

- **Phần cứng:** Yolo:Bit (OhStem), có thể kèm mạch mở rộng.
- **Firmware:** MicroPython cho Yolo:Bit (cài qua app OhStem hoặc hướng dẫn chính thức).
- **Môi trường:** VSCode + extension MicroPython (ví dụ **MicroPico** / **MicroPython**), hoặc app OhStem để nạp code và mở Serial Monitor.

## Cấu trúc thư mục

```
yolobit-micropython/
├── boot.py      # (Tùy chọn) Chạy trước main.py
├── main.py      # Điểm vào, scheduler và danh sách task
├── config.py    # Cấu hình: LED, chu kỳ task, ...
├── tasks.py     # Các task: in "Xin chào!", chớp LED, ...
└── README.md    # Hướng dẫn này
```

## Setup nhanh

1. **Kết nối Yolo:Bit** với máy tính qua USB.
2. **Mở thư mục project** trong VSCode.
3. **Chọn interpreter/port** MicroPython đúng với cổng COM của Yolo:Bit.
4. **Nạp code** (Run / Upload tùy extension):
   - Nạp ít nhất: `main.py`, `config.py`, `tasks.py`.
5. **Mở Serial Monitor** (baud thường **115200**) để xem dòng `Xin chào!` và gỡ lỗi.

## Hai task mẫu

| Task | Mô tả | Chu kỳ (mặc định) |
|------|--------|--------------------|
| **task_print_hello** | In ra serial dòng `Xin chào!` | Mỗi 1 giây |
| **task_blink_led**   | Chớp tắt LED (P0 hoặc LED onboard) | Mỗi 0,5 giây |

- **In ra terminal:** dùng `print("Xin chào!")` trong task; xem trên Serial Monitor (app OhStem hoặc VSCode).
- **LED:** cấu hình trong `config.py` — dùng LED trên board hoặc LED nối vào chân **P0** (giống kéo thả: chân P0).

## Cấu hình (config.py)

- **LED**
  - Dùng **LED trên board:** `USE_BUILTIN_LED = True`, `LED_GPIO = 2` (hoặc theo tài liệu board).
  - Dùng **LED ngoài ở P0:** `USE_BUILTIN_LED = False`, `PIN_LED = "pin0"`.
- **Chu kỳ task**
  - `INTERVAL_PRINT_HELLO_MS = 1000`  → in "Xin chào!" mỗi 1 giây.
  - `INTERVAL_LED_BLINK_MS = 500`    → chớp LED mỗi 0,5 giây.

Chỉnh các giá trị này cho phù hợp board và bài tập.

## Thêm task mới

1. **Trong `tasks.py`:** viết hàm không tham số, ví dụ:
   ```python
   def task_do_something():
       print("Task cua toi")
       # ... gọi API yolobit / machine / thư viện OhStem
   ```
2. **Trong `config.py`:** thêm hằng chu kỳ (ms), ví dụ `INTERVAL_MY_TASK_MS = 2000`.
3. **Trong `main.py`:** thêm vào danh sách `TASKS`:
   ```python
   (config.INTERVAL_MY_TASK_MS, tasks.task_do_something),
   ```

Chỉ dùng **các thư viện mà Yolo:Bit/OhStem hỗ trợ** (ví dụ `yolobit`, `machine`, `time`, thư viện mở rộng từ app OhStem) để giống với môi trường code kéo thả.

## Đồng bộ với code kéo thả OhStem

- **Chân:** Dùng tên `pin0`, `pin1`, `pin2`, ... tương ứng P0, P1, P2 trong app OhStem; cấu hình trong `config.py` bằng `PIN_LED = "pin0"`, v.v.
- **API:** Dùng `write_digital(0/1)`, `read_digital()`, `write_analog()`, `read_analog()` trên đối tượng pin từ `yolobit` như trong code sinh ra từ khối kéo thả.
- **Thư viện mở rộng:** Nếu dùng Kit (Home:Bit, Plant:Bit, City:Bit, …), copy các file `.py` thư viện đó vào project và `import` trong `tasks.py` hoặc `main.py` giống trong app OhStem.

## Gỡ lỗi

- Không thấy "Xin chào!" → kiểm tra Serial Monitor đúng cổng và baud **115200**.
- LED không chớp → kiểm tra `config.py` (LED onboard vs P0), nối dây đúng chân và GND.
- Lỗi `no module named 'yolobit'` → dùng firmware MicroPython đúng cho Yolo:Bit (OhStem).

## Tài liệu tham khảo

- [OhStem Education](https://docs.ohstem.vn/)
- [Cài đặt thư viện Yolo:Bit](https://docs.ohstem.vn/en/latest/module/thu-vien-yolobit.html)
- App lập trình: [app.ohstem.vn](https://app.ohstem.vn/) (kéo thả / MicroPython)

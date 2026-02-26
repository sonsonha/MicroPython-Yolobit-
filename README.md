# Yolobit MicroPython – Template RTOS (VSCode)

Template lập trình **MicroPython** cho **Yolo:Bit** (OhStem) trên **VSCode**, dùng thư viện **event_manager** của OhStem (giống code do app kéo thả sinh ra). Các "task" là **timer event callback**, đăng ký bằng `event_manager.add_timer_event(interval_ms, callback)`, vòng lặp chính: `event_manager.run()` + `time.sleep_ms(10)`.

## Yêu cầu

- **Phần cứng:** Yolo:Bit (OhStem), có thể kèm mạch mở rộng.
- **Firmware:** MicroPython cho Yolo:Bit (cài qua app OhStem hoặc hướng dẫn chính thức). Cần có thư viện **event_manager** (có sẵn trong firmware/app OhStem).
- **Môi trường:** VSCode + extension MicroPython (ví dụ **PyMakr**, **MicroPico** / **MicroPython**), hoặc app OhStem để nạp code và mở Serial Monitor.

## Cấu trúc thư mục

```
yolobit-micropython/
├── boot.py        # (Tùy chọn) Chạy trước main.py
├── main.py        # Điểm vào, scheduler và danh sách task
├── config.py      # Cấu hình: LED, chu kỳ task, ...
├── tasks.py       # Các task: in "Xin chào!", chớp LED, ...
├── pymakr.conf    # Cấu hình PyMakr (sửa address = cổng COM)
└── README.md      # Hướng dẫn này
```

## Setup nhanh

1. **Kết nối Yolo:Bit** với máy tính qua USB.
2. **Mở thư mục project** trong VSCode.
3. **Chọn interpreter/port** MicroPython đúng với cổng COM của Yolo:Bit.
4. **Nạp code** (Run / Upload tùy extension):
   - Nạp ít nhất: `main.py`, `config.py`, `tasks.py`.
5. **Mở Serial Monitor** (baud thường **115200**) để xem dòng `Xin chào!` và gỡ lỗi.

### Dùng extension PyMakr (VSCode)

PyMakr dùng được với Yolo:Bit. Cần làm đúng hai việc: **mở đúng project (thư mục code)** và **chọn đúng cổng COM** khi Yolo:Bit cắm USB.

#### 1. Mở project hiện tại (không tạo project mới)

- **Workspace = thư mục đang mở trong VSCode.** Để làm việc đúng với source hiện tại, hãy dùng **File → Open Folder** của **VSCode** (không phải nút Open trong PyMakr), chọn thư mục **yolobit-micropython**. Khi đó workspace chính là source của bạn.
- **Nút "Open" trong PyMakr** thường dùng để *chọn thư mục cho project PyMakr*; nó có thể mở cửa sổ mới hoặc đổi workspace, nên bạn cảm giác "không thể ở workspace ở source hiện tại". Cách làm đúng: **trước tiên** mở thư mục bằng **File → Open Folder** (VSCode) → chọn `yolobit-micropython` → Open. Sau đó **không cần** bấm "Open" trong PyMakr; chỉ dùng PyMakr để Connect, Upload, mở Console. Project trong PyMakr sẽ trỏ đúng thư mục đang mở.
- **Không** dùng “Create project” / “New project” trong PyMakr — nếu tạo project mới, PyMakr sẽ tạo thư mục khác và bạn không thấy code của mình.
- Nếu vẫn thấy “Empty Project”: đóng VSCode, mở lại và **File → Open Folder** vào `yolobit-micropython`.

#### 2. PyMakr không có mục “chọn board Yolobit”

- Trong PyMakr **không có** danh sách board (Yolo:Bit, ESP32, …). Extension chỉ hiển thị danh sách **cổng COM / serial** do máy tính báo.
- Các mục kiểu **tty.Bluetooth-Incoming-Port**, **tty.EDIFIERX2s**, **tty.RedmiBuds...** (hoặc “unknown?”) là cổng Bluetooth / thiết bị khác, **không phải** Yolo:Bit.
- Để dùng Yolo:Bit với PyMakr:
  1. **Cắm Yolo:Bit vào máy bằng cáp USB** (không dùng kết nối Bluetooth cho nạp code).
  2. Chờ vài giây; nếu đã cài driver USB (CH340, CP210x, …) thì sẽ xuất hiện **một cổng serial mới** (ví dụ macOS: `/dev/cu.usbserial-xxxx`, `/dev/cu.SLAB_USBtoUART`; Windows: `COM3`, `COM4`; Linux: `/dev/ttyUSB0`).
  3. Trong PyMakr, **chọn cổng đó** (có thể qua “Add device” hoặc cấu hình `address` trong `pymakr.conf`).
- Nếu **không thấy** cổng USB sau khi cắm Yolo:Bit: cài driver theo [hướng dẫn OhStem](https://docs.ohstem.vn/) (Thiết lập và cài đặt Driver).

#### 3. Cấu hình và Upload

- Mở file **`pymakr.conf`** trong project; sửa **`address`** thành cổng COM của Yolo:Bit (ví dụ `"COM3"` trên Windows, `"/dev/cu.usbserial-0001"` trên macOS). Để trống nếu bạn chọn cổng trực tiếp trong PyMakr.
- **Upload:** trong Pymakr chọn **Upload project to device** (icon mây + mũi tên lên) để đồng bộ file lên board.
- **Chạy:** trên board sẽ tự chạy `main.py` khi reset; hoặc mở **Console/REPL** (icon `>_`) rồi gõ `import main` để chạy. Dùng Console để xem `print("Xin chào!")` (baud thường 115200).

#### 4. Sau khi upload: có cần chạy main.py? Code có chạy khi rút USB?

- **Không cần “chạy main.py” từ VSCode sau khi upload.** File đã nằm trong bộ nhớ của Yolo:Bit. Mỗi lần **bật nguồn hoặc nhấn nút Reset**, board sẽ tự chạy `boot.py` rồi `main.py`. Chỉ cần upload xong rồi reset (hoặc rút USB rồi cắm lại / bật nguồn) là chương trình chạy (LED chớp, in "Xin chào!" nếu có nối serial).
- **Rút USB (rút COM) ra thì sao?**
  - Nếu Yolo:Bit **chỉ dùng nguồn USB**: rút ra = mất điện = board tắt, code không chạy. **Code vẫn còn** trong board; lần sau cắm USB (hoặc cấp nguồn khác) và bật lại thì `main.py` lại tự chạy.
  - Nếu Yolo:Bit **có nguồn pin/ắc-quy** (cổng pin hoặc pin gắn trên board): rút USB thì board vẫn chạy bằng nguồn đó, LED vẫn chớp, code vẫn chạy bình thường.
- Tóm lại: Upload một lần, code được lưu trên board; mỗi lần bật nguồn/reset là chạy. Rút COM chỉ ngắt nguồn (nếu không có pin), không xóa code.

## Hai task mẫu (timer event callbacks)

| Callback | Mô tả | Chu kỳ (mặc định) |
|----------|--------|--------------------|
| **on_event_timer_callback_print_hello** | In ra serial "Xin chào!" | Mỗi 1 giây |
| **on_event_timer_callback_blink_led**   | Chớp tắt LED (P0 hoặc onboard) | Mỗi 0,5 giây |

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

## Thêm task mới (timer event)

1. **Trong `tasks.py`:** viết callback đặt tên `on_event_timer_callback_<mô_tả>`, ví dụ:
   ```python
   def on_event_timer_callback_do_something():
       print("Task cua toi")
       # ... gọi API yolobit / machine / thư viện OhStem
   ```
2. **Trong `config.py`:** thêm chu kỳ (ms), ví dụ `INTERVAL_MY_TASK_MS = 2000`.
3. **Trong `main.py`:** sau khi `event_manager.reset()`, thêm dòng:
   ```python
   event_manager.add_timer_event(config.INTERVAL_MY_TASK_MS, tasks.on_event_timer_callback_do_something)
   ```

Chỉ dùng **thư viện Yolo:Bit/OhStem** (yolobit, event_manager, machine, time, ...) để đồng bộ với code kéo thả.

## Đồng bộ với code kéo thả OhStem

- **event_manager:** Chương trình dùng thư viện **event_manager** của OhStem: `event_manager.reset()`, `event_manager.add_timer_event(interval_ms, callback)`, vòng lặp `event_manager.run()` + `time.sleep_ms(10)`. Cấu trúc giống code Python do app OhStem sinh ra khi lập trình kéo thả.
- **Chân:** Dùng tên `pin0`, `pin1`, `pin2`, ... tương ứng P0, P1, P2 trong app OhStem; cấu hình trong `config.py` bằng `PIN_LED = "pin0"`, v.v.
- **API:** Dùng `write_digital(0/1)`, `read_digital()`, `write_analog()`, `read_analog()` trên đối tượng pin từ `yolobit` như trong code sinh ra từ khối kéo thả.
- **Thư viện mở rộng:** Nếu dùng Kit (Home:Bit, Plant:Bit, City:Bit, …), copy các file `.py` thư viện đó vào project và `import` trong `tasks.py` hoặc `main.py` giống trong app OhStem.

## Gỡ lỗi

- Không thấy "Xin chào!" → kiểm tra Serial Monitor đúng cổng và baud **115200**.
- LED không chớp → kiểm tra `config.py` (LED onboard vs P0), nối dây đúng chân và GND.
- Lỗi `no module named 'yolobit'` → dùng firmware MicroPython đúng cho Yolo:Bit (OhStem).
- **PyMakr:** Chỉ thấy Bluetooth (tty.RedmiBuds, tty.EDIFIER...) → cắm Yolo:Bit bằng **cáp USB** và cài driver; chọn cổng serial USB (ví dụ `/dev/cu.usbserial-*`, `COMx`), không chọn cổng Bluetooth. Không mở được project → dùng **File → Open Folder** vào thư mục chứa `main.py`/`pymakr.conf`, không tạo "Create project" mới.

## Tài liệu tham khảo

- [OhStem Education](https://docs.ohstem.vn/)
- [Cài đặt thư viện Yolo:Bit](https://docs.ohstem.vn/en/latest/module/thu-vien-yolobit.html)
- App lập trình: [app.ohstem.vn](https://app.ohstem.vn/) (kéo thả / MicroPython)

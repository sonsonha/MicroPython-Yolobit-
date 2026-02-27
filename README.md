# Yolobit MicroPython – Template RTOS (VSCode)

Mỗi **task** nằm trong **một file riêng** (task1.py, task2.py, ...), có **hai hàm**: `task_init()` (chạy một lần) và `task_run()` (được đăng ký vào `event_manager.add_timer_event()`). Biến **status** (nếu cần) khai báo **toàn cục** trong từng file task.

## Yêu cầu

- **Phần cứng:** Yolo:Bit (OhStem), có thể kèm mạch mở rộng.
- **Firmware:** MicroPython cho Yolo:Bit (cài qua app OhStem hoặc hướng dẫn chính thức). Cần có thư viện **event_manager** (có sẵn trong firmware/app OhStem).
- **Môi trường:** VSCode + extension MicroPython (ví dụ **PyMakr**, **MicroPico** / **MicroPython**), hoặc app OhStem để nạp code và mở Serial Monitor.

## Cấu trúc thư mục

```
yolobit-micropython/
├── boot.py        # (Tùy chọn) Chạy trước main.py
├── main.py        # Điểm vào: event_manager.reset(), task_init(), add_timer_event(..., task_run)
├── config.py      # Cấu hình chu kỳ task (INTERVAL_TASK1_MS, INTERVAL_TASK2_MS, ...)
├── task1.py       # Task 1: task_init(), task_run(), status toàn cục
├── task2.py       # Task 2: task_init(), task_run(), status toàn cục (chớp HEART/HEART_SMALL)
├── pymakr.conf    # Cấu hình PyMakr (sửa address = cổng COM)
└── README.md      # Hướng dẫn này
```

## Setup nhanh

1. **Kết nối Yolo:Bit** với máy tính qua USB.
2. **Mở thư mục project** trong VSCode.
3. **Chọn interpreter/port** MicroPython đúng với cổng COM của Yolo:Bit.
4. **Nạp code** (Run / Upload tùy extension):
   - Nạp ít nhất: `main.py`, `config.py`, `task1.py`, `task2.py`.
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

## Hai task mẫu (mỗi task một file, task_init + task_run)

| File     | Mô tả                                      | Chu kỳ (mặc định) |
|----------|--------------------------------------------|--------------------|
| **task1.py** | In "Xin chào!" ra serial; có `status` toàn cục, `task_init()`, `task_run()` | 1 giây  |
| **task2.py** | Chớp hình trái tim trên display (HEART / HEART_SMALL); `status` toàn cục, `task_init()`, `task_run()` — code giống block kéo thả OhStem | 0,5 giây |

- **task1:** `task_run()` gọi `print("Xin chào!")`; xem trên Serial Monitor (115200).
- **task2:** `task_run()` đảo `status = 1 - status`, rồi `display.show(Image.HEART)` hoặc `display.show(Image.HEART_SMALL)` (từ `yolobit`).

## Cấu hình (config.py)

- **Chu kỳ task**
  - `INTERVAL_TASK1_MS = 1000` → task 1 (in "Xin chào!") mỗi 1 giây.
  - `INTERVAL_TASK2_MS = 500`  → task 2 (chớp HEART/HEART_SMALL) mỗi 0,5 giây.
- Các biến LED (USE_BUILTIN_LED, PIN_LED, ...) vẫn có trong config nếu task khác cần dùng chân.

## Thêm task mới (file riêng, task_init + task_run)

1. **Tạo file `taskN.py`** (ví dụ `task3.py`):
   - Khai báo **status** (hoặc biến trạng thái khác) **toàn cục** nếu cần.
   - Hàm **`task_init()`**: khởi tạo một lần (gán status = 0, setup cảm biến, ...).
   - Hàm **`task_run()`**: logic chạy mỗi chu kỳ (sẽ được add vào event_manager).
   ```python
   # task3.py
   from yolobit import *  # nếu cần
   status = 0
   def task_init():
       global status
       status = 0
   def task_run():
       global status
       # ... logic task
   ```
2. **Trong `config.py`:** thêm `INTERVAL_TASK3_MS = 2000` (ví dụ).
3. **Trong `main.py`:** import task3; gọi `task3.task_init()` sau khi reset; thêm `event_manager.add_timer_event(config.INTERVAL_TASK3_MS, task3.task_run)`.

## Đồng bộ với code kéo thả OhStem

- **event_manager:** `event_manager.reset()`, mỗi task có `task_init()` (gọi một lần) và `task_run()` (đăng ký bằng `event_manager.add_timer_event(interval_ms, taskN.task_run)`), vòng lặp `event_manager.run()` + `time.sleep_ms(10)`. Cấu trúc và API giống code do app OhStem sinh ra.
- **Mỗi task một file:** task1.py, task2.py, ...; trong file khai báo **status** (hoặc biến trạng thái) **toàn cục**, có **task_init()** và **task_run()**.
- **Chân / display:** Dùng `yolobit` (pin0, pin1, display, Image, ...) như trong code kéo thả.

## Gỡ lỗi

- Không thấy "Xin chào!" → kiểm tra Serial Monitor đúng cổng và baud **115200**.
- Display không chớp hình trái tim → kiểm tra Yolo:Bit có màn hình LED matrix và firmware có `display`, `Image` từ yolobit.
- Lỗi `no module named 'yolobit'` → dùng firmware MicroPython đúng cho Yolo:Bit (OhStem).
- Lỗi `no module named 'event_manager'` → firmware của bạn chưa có thư viện OhStem; project này đã kèm **`event_manager.py`** để chạy được cấu trúc giống code kéo thả. Hãy upload thêm file này lên board cùng `main.py`.
- **PyMakr:** Chỉ thấy Bluetooth (tty.RedmiBuds, tty.EDIFIER...) → cắm Yolo:Bit bằng **cáp USB** và cài driver; chọn cổng serial USB (ví dụ `/dev/cu.usbserial-*`, `COMx`), không chọn cổng Bluetooth. Không mở được project → dùng **File → Open Folder** vào thư mục chứa `main.py`/`pymakr.conf`, không tạo "Create project" mới.

## Tài liệu tham khảo

- [OhStem Education](https://docs.ohstem.vn/)
- [Cài đặt thư viện Yolo:Bit](https://docs.ohstem.vn/en/latest/module/thu-vien-yolobit.html)
- App lập trình: [app.ohstem.vn](https://app.ohstem.vn/) (kéo thả / MicroPython)

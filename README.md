## Yolobit MicroPython (OhStem) – Template theo event_manager

Template này giúp bạn lập trình **Yolo:Bit (OhStem)** bằng **MicroPython** trên **VSCode** và nạp chương trình bằng extension **PyMakr**.

- **Kiến trúc giống OhStem kéo thả**: dùng `event_manager.reset()`, `event_manager.add_timer_event(...)`, vòng lặp `event_manager.run()` + `time.sleep_ms(10)`.
- **Mỗi task một file**: `task1.py`, `task2.py`, ...; mỗi file có **2 hàm**:
  - `task_init()` chạy **1 lần**
  - `task_run()` chạy **lặp theo chu kỳ** (được add vào event_manager)
- **Biến trạng thái** (ví dụ `status`) khai báo **toàn cục trong từng file task** (giống cách OhStem sinh code).

## Yêu cầu

- **Phần cứng**: Yolo:Bit (OhStem) + cáp USB (cáp dữ liệu, không chỉ sạc).
- **Firmware**: MicroPython cho Yolo:Bit (cài qua app OhStem). Cần có `yolobit` (thường có sẵn trên firmware OhStem).
- **VSCode**: cài extension **PyMakr** (Pycom).
- **Driver USB**:
  - Windows: cần driver CH340/CP210x tùy board.
  - macOS: thường dùng được ngay; nếu không thấy cổng USB-Serial thì cần cài driver theo OhStem.

## Cấu trúc project (những file quan trọng)

```
yolobit-micropython/
├── main.py          # chương trình chính: reset, task_init, add_timer_event, while True run()
├── event_manager.py # (kèm theo) polyfill nếu firmware thiếu event_manager
├── config.py        # chu kỳ task: INTERVAL_TASK1_MS, INTERVAL_TASK2_MS, ...
├── task1.py         # task 1: task_init(), task_run(), status toàn cục
├── task2.py         # task 2: chớp Image.HEART / Image.HEART_SMALL (giống block OhStem)
├── pymakr.conf      # cấu hình PyMakr (tùy chọn)
└── README.md
```

## Hướng dẫn A → Z: nạp code bằng PyMakr trên VSCode

### A. Cài đặt PyMakr

1. Mở VSCode → Extensions → tìm **PyMakr** (Pycom) → Install.
2. Cắm Yolo:Bit vào máy tính bằng **cáp USB**.
3. Kiểm tra máy có thấy cổng serial USB:
   - Windows: Device Manager → Ports (COM & LPT) → thấy `COMx`.
   - macOS: sẽ có `/dev/cu.*` (thường là `/dev/cu.usbserial-*` hoặc `/dev/cu.SLAB_USBtoUART`).

### B. Mở đúng project trong VSCode

1. VSCode → **File → Open Folder…**
2. Chọn thư mục `yolobit-micropython` (thư mục chứa `main.py`, `pymakr.conf`, …).

Lưu ý:
- **Đừng tạo “New project” trong PyMakr** cho trường hợp này. Project của bạn chính là folder đang mở trong VSCode.

### C. Cấu hình `pymakr.conf` (khuyến nghị)

Mở file `pymakr.conf`. Bạn có thể để `address` trống và chọn cổng khi Add device, hoặc điền sẵn.

Ví dụ (Windows):

```json
{
  "name": "Yolobit MicroPython",
  "address": "COM13",
  "sync_folder": "",
  "sync_file_types": "py,txt,log,json",
  "ctrl_c_on_connect": true,
  "safe_boot_on_upload": false
}
```

Ví dụ (macOS):

```json
{
  "name": "Yolobit MicroPython",
  "address": "/dev/cu.usbserial-0001",
  "sync_folder": "",
  "sync_file_types": "py,txt,log,json",
  "ctrl_c_on_connect": true,
  "safe_boot_on_upload": false
}
```

Giải thích nhanh:
- **name**: tên project hiển thị trong PyMakr.
- **address**: cổng serial (COMx hoặc `/dev/cu.*`).
- **sync_folder**: để rỗng = sync **toàn bộ** project folder.
- **ctrl_c_on_connect**: tự gửi Ctrl+C khi connect để dừng script đang chạy (giúp upload ổn định).
- **safe_boot_on_upload**: thường để `false`; khi upload bị lỗi do script đang chạy, bạn có thể thử bật `true` (tùy firmware).

### D. Add device → Connect device

Trong panel PyMakr (bên trái):

1. Vào **PROJECTS** → chọn project (ví dụ “Yolobit MicroPython”).
2. Nhấn **Add device**.
3. Chọn đúng **COM/USB Serial** của Yolo:Bit.
   - Không chọn các cổng Bluetooth (ví dụ `tty.RedmiBuds...`, `Bluetooth-Incoming-Port`).
4. Nhấn **Connect device**.

### E. Sync project to device (Upload)

1. Khi đã connect, nhấn **Sync project to device** (hoặc “Upload project to device”).
2. Chờ sync xong.

### F. Mở Terminal/REPL để xem `print()` và debug

1. Trong PyMakr, mở **Terminal/REPL** (console).
2. Bạn có thể kiểm tra file đã lên board chưa:

```python
import os
os.listdir()
```

Danh sách phải có (tối thiểu):
- `main.py`
- `config.py`
- `task1.py`
- `task2.py`
- `event_manager.py` (nếu firmware không có module này)

### G. “Open device in file explorer” để kiểm tra file trên board

1. Trong PyMakr, chọn **Open device in file explorer**.
2. Bạn sẽ thấy “filesystem” của board.
3. Đối chiếu xem các file `.py` đã nằm trên device.

### H. Chạy chương trình

Có 2 cách:

- **Cách 1 (khuyến nghị)**: **Soft reset** để board chạy lại và vẫn giữ REPL ổn định.
  - Trong PyMakr chọn **Soft reset device** (hoặc trong REPL nhấn Ctrl+D).
  - Board sẽ tự chạy `main.py` → bạn thấy `print(...)` hiện ra trong Terminal.

- **Cách 2**: chạy trực tiếp từ REPL:

```python
import main
```

Lưu ý: Nếu `main.py` chạy vòng lặp vô hạn, REPL sẽ “bận”. Muốn dừng, gửi **Ctrl+C** hoặc dùng nút **Stop script** trong PyMakr.

### I. Hard reset / Reset vì sao hay bị disconnect?

- **Hard reset** là reset phần cứng → cổng COM/USB-Serial thường **tụt** rồi **lên lại** vài giây, nên PyMakr có thể bị **disconnect**.
- Đây thường **không phải lỗi code**. Nếu mục tiêu là “restart và xem log”, hãy dùng **Soft reset**.

### J. Sau khi rút USB, chương trình có chạy không?

- Nếu board **mất nguồn** khi rút USB → sẽ tắt, không chạy. Nhưng **code vẫn lưu** trên board.
- Nếu board được cấp nguồn bằng pin/nguồn ngoài → chương trình vẫn chạy.
- Mỗi lần bật nguồn/reset, MicroPython tự chạy `boot.py` rồi `main.py`.

## Các chức năng PyMakr hay dùng (tóm tắt)

- **Add device**: thêm thiết bị theo cổng COM.
- **Connect device / Disconnect device**: kết nối / ngắt kết nối.
- **Sync project to device (Upload)**: upload toàn bộ project lên board.
- **Download project from device**: tải file từ board về máy.
- **Open device in file explorer**: xem filesystem trên board.
- **Open Terminal/REPL**: mở console để chạy lệnh, xem `print()`.
- **Stop script**: gửi Ctrl+C để dừng chương trình đang chạy.
- **Soft reset device**: reset “mềm”, thường giữ kết nối tốt hơn.
- **Hard reset device**: reset “cứng”, có thể làm rớt COM tạm thời.

## Nội dung chương trình mẫu

### Task 1: `task1.py`

- In `Xin chào!` mỗi 1 giây.

### Task 2: `task2.py`

- Chớp qua lại `Image.HEART` và `Image.HEART_SMALL` (giống block OhStem).

Chu kỳ nằm trong `config.py`:
- `INTERVAL_TASK1_MS = 1000`
- `INTERVAL_TASK2_MS = 500`

## Thêm task mới (cho sinh viên)

1. Tạo `task3.py` có `status`, `task_init()`, `task_run()`.
2. Thêm `INTERVAL_TASK3_MS` trong `config.py`.
3. Trong `main.py`:
   - `import task3`
   - `task3.task_init()`
   - `event_manager.add_timer_event(config.INTERVAL_TASK3_MS, task3.task_run)`

## Gỡ lỗi nhanh

- `ImportError: no module named 'yolobit'` → firmware không đúng Yolo:Bit/OhStem.
- `ImportError: no module named 'event_manager'` → firmware thiếu; project này đã kèm **`event_manager.py`**. Đảm bảo bạn đã **sync/upload** file đó lên board.
- Không thấy log `print()`:
  - mở đúng **Terminal/REPL** của PyMakr,
  - dùng **Soft reset** thay vì Hard reset,
  - hoặc chạy `import main` trong REPL.

## Tài liệu tham khảo

- [OhStem Education](https://docs.ohstem.vn/)
- App lập trình: [app.ohstem.vn](https://app.ohstem.vn/) (kéo thả / MicroPython)

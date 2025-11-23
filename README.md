
# **Bài tập lớn Mô hình hóa Toán học**  
## **Symbolic and Algebraic Reasoning in Petri Nets**  
### (Task 1–3)

Repo này gồm 3 task đầu của bài tập lớn:

- **Task 1:** Đọc mô hình Petri từ file PNML  
- **Task 2:** Tính reachable markings bằng BFS / DFS  
- **Task 3:** Biểu diễn reachable set bằng BDD (thuật toán symbolic Pastor-Cortadella)

---

## Cấu trúc chính

```text
.
├── PetriNet.py       # Parse PNML và tạo ma trận I/O + M0
├── BFS.py            # Reachability dùng BFS (explicit)
├── DFS.py            # Reachability dùng DFS (explicit)
├── BDD.py            # Reachability bằng BDD (symbolic)
├── main.py           # File chạy thử tất cả các task
├── SimpleMutex.pnml  # PNML mẫu
└── README.md
````

---

## Cài đặt

Cài các thư viện cần thiết:

```bash
pip install numpy
pip install pyeda
```

---

## Chạy chương trình

Trong thư mục root:

```bash
python main.py
```

`main.py` sẽ:

1. Load mô hình từ `SimpleMutex.pnml`
2. In danh sách place, transition, ma trận I/O và M0
3. Chạy BFS để tính reachable markings (explicit)
4. Chạy DFS để tính reachable markings (explicit)
5. Chạy BDD để tính reachable set (symbolic)
6. In số marking reachable và kích thước BDD DAG

---

## Mô tả từng phần

### 1. `PetriNet.py` – Task 1

Hàm:

```python
PetriNet.from_pnml(filename)
```

File PNML được parse theo chuẩn PNML 2009:

* Lấy danh sách place / transition
* Lấy tên (nếu có)
* Lấy initial marking
* Sinh ma trận **I** và **O** với kích thước
  `(số transition × số place)`

**Lưu ý / giới hạn của parser:**

* Chỉ xử lý **PT-net 1-safe**
* Arc weight = 1
* Không hỗ trợ inhibitor arc, reset arc,…

---

### 2. Task 2 – BFS / DFS Reachability

```python
bfs_reachable(pn)
dfs_reachable(pn)
```

Ý tưởng:

* Transition t enabled khi marking ≥ I[t]
* Sau khi bắn: `new = marking - I[t] + O[t]`
* Vì mô hình 1-safe nên new phải ≤ 1
* Dùng `set(tuple)` để lưu các marking đã xuất hiện

Kết quả: **tập reachable markings**.

---

### 3. Task 3 – Reachability bằng BDD (Symbolic)

```python
bdd_reachable(pn)
```

**Thuật toán symbolic theo Pastor-Cortadella:**

1. **Mã hóa trạng thái:** Mỗi place → 1 biến Boolean (1-safe assumption)
2. **Transition relation R(X, X'):** Xây dựng hàm Boolean biểu diễn tất cả các chuyển trạng thái
   - Điều kiện bật: Các place đầu vào phải có token
   - Guard 1-safe: Không đặt token vào place đã có token (trừ khi consume)
   - Cập nhật trạng thái mới X' dựa trên X
3. **Fixed-point iteration:**
   - Bắt đầu từ marking khởi đầu M0
   - Lặp: Tính post-image bằng ∃X (F(X) ∧ R(X, X'))
   - Thêm các trạng thái mới vào tập reachable
   - Dừng khi không còn trạng thái mới

**Ưu điểm:**
- Compact: BDD biểu diễn tập trạng thái một cách nén
- Efficient: Xử lý symbolic, tránh enum từng marking
- Scalable: Tốt hơn explicit cho mô hình lớn

**Kết quả:** Trả về `(BDD, số lượng marking)`

---
## Giới hạn

* Chỉ áp dụng cho **1-safe PT-net**
* Không chạy đúng với PNML có marking > 1
* Chỉ hỗ trợ arc weight = 1
* Không hỗ trợ dạng nâng cao (timed, colored, inhibitor…)

---
## TODO - Phần còn thiếu (polish để report đầy đủ hơn theo yêu cầu PDF)

### Task 1 - PNML Parser
 **Verify consistency:** Chưa kiểm tra missing arcs/nodes như yêu cầu trong đề bài

### Task 3 - BDD Reachability  
 **Performance comparison:** Chưa so sánh time & memory giữa explicit (BFS/DFS) và symbolic (BDD) approach

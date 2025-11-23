
# **Bài tập lớn Mô hình hóa Toán học**  
## **Symbolic and Algebraic Reasoning in Petri Nets**  
### (Task 1–3)

Repo này gồm 3 task đầu của bài tập lớn:

- **Task 1:** Đọc mô hình Petri từ file PNML  
- **Task 2:** Tính reachable markings bằng BFS / DFS  
- **Task 3:** Biểu diễn reachable set bằng BDD  

---

## Cấu trúc chính

```text
.
├── PetriNet.py       # Parse PNML và tạo ma trận I/O + M0
├── BFS.py            # Reachability dùng BFS
├── DFS.py            # Reachability dùng DFS
├── BDD.py            # Reachability bằng BDD (từ tập explicit)
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
3. Chạy BFS + DFS để tính reachable markings
4. Chạy BDD (từ danh sách reachable đã thu được)
5. In số marking reachable theo từng phương pháp

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

### 3. Task 3 – Reachability bằng BDD

```python
bdd_reachable(pn)
```

Cách làm:

1. Dùng BFS (giống Task 2) để liệt kê toàn bộ reachable markings
2. Mỗi marking được mã hoá thành 1 biểu thức Boolean
3. OR toàn bộ các biểu thức → reachable set
4. Chuyển sang BDD bằng `expr2bdd`

---
## Giới hạn

* Chỉ áp dụng cho **1-safe PT-net**
* Không chạy đúng với PNML có marking > 1
* Chỉ hỗ trợ arc weight = 1
* Không hỗ trợ dạng nâng cao (timed, colored, inhibitor…)

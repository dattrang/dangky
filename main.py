import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Danh sách các thôn (thay bằng danh sách thực tế của bạn, ví dụ 62 thôn)
# Danh sách các thôn đã sắp xếp theo alphabet
villages = [
    "Khối 1",
    "Khối 10",
    "Khối 11",
    "Khối 12",
    "Khối 13",
    "Khối 14",
    "Khối 2",
    "Khối 3",
    "Khối 4",
    "Khối 5",
    "Khối 6",
    "Khối 7",
    "Khối 8",
    "Khối 9",
    "Khu 418",
    "Khu Thuỷ Lợi 2",
    "Thôn 17",
    "Thôn 25",
    "Thôn Ấp Cút",
    "Thôn Bến",
    "Thôn Cả",
    "Thôn Chôi",
    "Thôn Cộng Hòa",
    "Thôn Đạc Tài",
    "Thôn Đan Tảo",
    "Thôn Đồng Chầm",
    "Thôn Đồng Dành",
    "Thôn Đồng Lạc",
    "Thôn Đông Bài",
    "Thôn Đông Thuỷ",
    "Thôn Đường 2",
    "Thôn Dược Hạ",
    "Thôn Dược Thượng",  # Gộp các xóm và khu của Dược Thượng
    "Thôn Hoàng Dương",
    "Thôn Hương Đình Đông",
    "Thôn Hương Đình Đoài",
    "Thôn Lạc Nông",
    "Thôn Lương Châu",
    "Thôn Mai Đông",
    "Thôn Mai Đoài",
    "Thôn Mai Nội",
    "Thôn Miếu Thờ",
    "Thôn Nội Phật",
    "Thôn Phú Thọ",
    "Thôn Phù Mã",
    "Thôn Sơn Đoài",
    "Thôn Sơn Đông",
    "Thôn Thái Phù",
    "Thôn Thanh Hà",
    "Thôn Thế Trạch",
    "Thôn Thượng",
    "Thôn Tuyền",
    "Thôn Vệ Linh",
    "Thôn Xuân Dục",  # Gộp Khu 418, Xóm Mới, Xóm Tân Lập, Xóm Núi Gơ
    "Thôn Xuân Đoài",
    "Thôn Xuân Đồng",
    "Thôn Yêm",
    "Tổ dân phố số 1",
    "Tổ dân phố số 2",
    "Tổ dân phố số 3",
    "Tổ dân phố số 4",
    "Tổ dân phố số 5"
]

# Khoảng thời gian
start_date = datetime(2025, 7, 28)
end_date = datetime(2025, 8, 21)
date_list = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

# Hàm tải dữ liệu từ file CSV
def load_data():
    try:
        data = pd.read_csv('registrations.csv')
    except FileNotFoundError:
        data = pd.DataFrame(columns=['Thôn', 'Ngày'])
    return data

# Hàm lưu dữ liệu vào file CSV
def save_data(data):
    data.to_csv('registrations.csv', index=False)

# Hàm tạo lịch dạng grid
def create_calendar():
    data = load_data()
    calendar_data = []
    week = []
    for i, date in enumerate(date_list):
        date_str = date.strftime("%Y-%m-%d")
        day_display = date.strftime("%d/%m")
        # Lấy danh sách các thôn đã đăng ký cho ngày này
        registered_villages = data[data['Ngày'] == date_str]['Thôn'].values
        # Nếu có thôn đăng ký, nối thành chuỗi, nếu không thì để None
        village_str = ", ".join(registered_villages) if len(registered_villages) > 0 else None
        week.append({
            'date': date_str,
            'display': day_display,
            'villages': village_str
        })
        if (i + 1) % 7 == 0 or i == len(date_list) - 1:
            calendar_data.append(week)
            week = []
    return calendar_data

# Giao diện ứng dụng
st.title("Đăng ký lịch tổ chức Tuyên tuyền tại các thôn, khu, tổ dân phố")

# Chọn thôn (chỉ hiển thị các thôn chưa đăng ký)
data = load_data()
registered_villages = set(data['Thôn'].values)
available_villages = [v for v in villages if v not in registered_villages]
village = st.selectbox("Chọn thôn, khu, tổ dân phố:", [""] + available_villages, key="village_select")

# Hiển thị lịch
st.header("Lịch đăng ký")

# CSS để định dạng ô lịch
st.markdown("""
    <style>
        .calendar-grid {
            display: grid;
            grid-template-columns: repeat(7, 120px);
            gap: 8px;
        }
        .stButton>button {
            width: 100%;
            min-height: 80px;
            border: 1px solid #ccc;
            border-radius: 5px;
            background-color: #f9f9f9;
            font-size: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 10px;
            white-space: pre-wrap;
        }
        .stButton>button:hover {
            background-color: #e0e0e0;
        }
        .stButton>button:disabled {
            background-color: #a9a9a9 !important;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Tạo session state để lưu trạng thái đăng ký
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = None

# Hiển thị lưới lịch
calendar_data = create_calendar()
for week in calendar_data:
    cols = st.columns(7)
    for i, day in enumerate(week):
        with cols[i]:
            # Tạo container cho mỗi ô ngày
            day_container = st.container()
            # Tạo key duy nhất cho mỗi nút
            button_key = f"button_{day['date']}"
            # Kiểm tra trạng thái nút
            is_registered = day['villages'] is not None
            button_label = f"{day['display']}\n{day['villages']}" if is_registered else day['display']
            # Tạo nút với nhãn
            if day_container.button(button_label, key=button_key):
                if not village:
                    st.warning("Vui lòng chọn thôn trước khi đăng ký.")
                else:
                    st.session_state.selected_date = day['date']

# Xử lý đăng ký
if st.session_state.selected_date:
    date = st.session_state.selected_date
    if village:
        data = load_data()
        # Kiểm tra xem thôn đã đăng ký ngày này chưa
        if data[(data['Thôn'] == village) & (data['Ngày'] == date)].empty:
            new_registration = pd.DataFrame({'Thôn': [village], 'Ngày': [date]})
            data = pd.concat([data, new_registration], ignore_index=True)
            save_data(data)
            st.success(f"Đã đăng ký thành công cho {village} vào ngày {datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')}")
            st.session_state.selected_date = None
            st.rerun()  # Làm mới trang để cập nhật lịch và dropdown
        else:
            st.success(f"{village} đã đăng ký ngày {datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')}!")
    else:
        st.warning("Vui lòng chọn thôn trước khi đăng ký.")

# Hiển thị bảng đăng ký
st.header("Bảng đăng ký hiện tại")
data = load_data()
if not data.empty:
    # Định dạng lại ngày để hiển thị
    display_data = data.copy()
    display_data['Ngày'] = display_data['Ngày'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').strftime('%d/%m/%Y'))
    st.table(display_data)
else:
    st.write("Chưa có đăng ký nào.")
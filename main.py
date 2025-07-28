import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Danh sách các thôn (62 đơn vị, đã sắp xếp theo alphabet)
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
    "Thôn Dược Thượng",
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
    "Thôn Xuân Dục",
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
        data = pd.read_csv('registrations.csv', encoding='utf-8')
        if not all(col in data.columns for col in ['Thôn', 'Ngày']):
            data = pd.DataFrame(columns=['Thôn', 'Ngày'])
    except (FileNotFoundError, pd.errors.ParserError, UnicodeDecodeError, PermissionError) as e:
        st.warning(f"Lỗi khi tải registrations.csv: {str(e)}. Tạo DataFrame rỗng mới.")
        data = pd.DataFrame(columns=['Thôn', 'Ngày'])
    return data

# Hàm lưu dữ liệu vào file CSV
def save_data(data):
    try:
        data.to_csv('registrations.csv', index=False, encoding='utf-8')
    except Exception as e:
        st.error(f"Lỗi khi lưu registrations.csv: {str(e)}")

# Hàm xóa dữ liệu
def delete_data():
    try:
        empty_data = pd.DataFrame(columns=['Thôn', 'Ngày'])
        save_data(empty_data)
        st.success("Đã xóa tất cả dữ liệu đăng ký!")
        st.session_state.selected_date = None
        st.rerun()
    except Exception as e:
        st.error(f"Lỗi khi xóa dữ liệu: {str(e)}")

# Hàm tạo lịch dạng grid
def create_calendar():
    data = load_data()
    calendar_data = []
    week = []
    for i, date in enumerate(date_list):
        date_str = date.strftime("%Y-%m-%d")
        day_display = date.strftime("%d/%m")
        registered_villages = data[data['Ngày'] == date_str]['Thôn'].values
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
st.title("Đăng ký lịch tổ chức Tuyên truyền tại các thôn, khu, tổ dân phố")

# Chọn thôn
data = load_data()
registered_villages = set(data['Thôn'].values)
available_villages = [v for v in villages if v not in registered_villages]
village = st.selectbox("Chọn thôn, khu, tổ dân phố:", [""] + available_villages, key="village_select")

# Nút xóa dữ liệu
if st.button("Xóa tất cả dữ liệu đăng ký"):
    delete_data()

# Hiển thị lịch
st.header("Lịch đăng ký")

# CSS tối ưu cho desktop và mobile
st.markdown("""
    <style>
        .calendar-grid {
            display: grid;
            grid-template-columns: repeat(7, 12vw);
            gap: 6px;
            overflow-x: auto;
            padding-bottom: 8px;
        }
        .stButton>button {
            width: 100%;
            min-height: 10vh;
            max-height: 15vh;
            border: 1px solid #ccc;
            border-radius: 5px;
            background-color: #ffffff;
            color: #000000 !important;
            font-size: 3vw;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 5px;
            white-space: normal;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .stButton>button:hover {
            background-color: #e0e0e0;
        }
        .stButton>button:disabled {
            background-color: #a9a9a9 !important;
            color: #ffffff !important;
        }
        /* Media query cho màn hình nhỏ (điện thoại) */
        @media (max-width: 600px) {
            .calendar-grid {
                grid-template-columns: repeat(7, 18vw);
            }
            .stButton>button {
                font-size: 4vw;
                min-height: 12vh;
                max-height: 18vh;
                padding: 4px;
            }
        }
        /* Tối ưu bảng đăng ký */
        .stDataFrame {
            overflow-x: auto;
            font-size: 2.5vw;
            color: #000000;
        }
        @media (max-width: 600px) {
            .stDataFrame {
                font-size: 3.5vw;
            }
        }
        /* Tùy chỉnh nút xác nhận và hủy */
        .confirm-button {
            background-color: #4CAF50 !important;
            color: white !important;
            margin-right: 10px;
        }
        .cancel-button {
            background-color: #f44336 !important;
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Tạo session state để lưu trạng thái đăng ký và xác nhận
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = None
if 'confirm_registration' not in st.session_state:
    st.session_state.confirm_registration = False

# Hiển thị lưới lịch
calendar_data = create_calendar()
for week in calendar_data:
    cols = st.columns(7)
    for i, day in enumerate(week):
        with cols[i]:
            day_container = st.container()
            button_key = f"button_{day['date']}"
            is_registered = day['villages'] is not None
            button_label = f"{day['display']}\n{day['villages']}" if is_registered else day['display']
            if day_container.button(button_label, key=button_key):
                if not village:
                    st.warning("Vui lòng chọn thôn trước khi đăng ký.")
                else:
                    st.session_state.selected_date = day['date']
                    st.session_state.confirm_registration = True

# Xử lý xác nhận đăng ký
if st.session_state.confirm_registration and st.session_state.selected_date:
    date = st.session_state.selected_date
    if village:
        formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')
        st.warning(f"Có chọn lịch ngày {formatted_date} cho {village} không?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Xác nhận", key="confirm_button", help="Xác nhận đăng ký", type="primary"):
                data = load_data()
                if data[(data['Thôn'] == village) & (data['Ngày'] == date)].empty:
                    new_registration = pd.DataFrame({'Thôn': [village], 'Ngày': [date]})
                    data = pd.concat([data, new_registration], ignore_index=True)
                    save_data(data)
                    st.success(f"Đã đăng ký thành công cho {village} vào ngày {formatted_date}")
                    st.session_state.selected_date = None
                    st.session_state.confirm_registration = False
                    st.rerun()
                else:
                    st.error(f"{village} đã đăng ký ngày {formatted_date}!")
                    st.session_state.selected_date = None
                    st.session_state.confirm_registration = False
        with col2:
            if st.button("Hủy", key="cancel_button", help="Hủy đăng ký"):
                st.session_state.selected_date = None
                st.session_state.confirm_registration = False
                st.rerun()
    else:
        st.warning("Vui lòng chọn thôn trước khi đăng ký.")
        st.session_state.selected_date = None
        st.session_state.confirm_registration = False

# Hiển thị bảng đăng ký
st.header("Bảng đăng ký hiện tại")
data = load_data()
if not data.empty:
    display_data = data.copy()
    display_data['Ngày'] = display_data['Ngày'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').strftime('%d/%m/%Y'))
    st.dataframe(display_data, use_container_width=True)
else:
    st.write("Chưa có đăng ký nào.")

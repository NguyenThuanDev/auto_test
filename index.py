import pandas as pd

# Đường dẫn đến file Excel
file_path = "./file.xlsx"
def SKU(string):
    array =string.split('_')
    return array[len(array)-2]
# Đọc tên các sheet
sheet_names = pd.ExcelFile(file_path).sheet_names

# Danh sách để lưu dữ liệu từ mỗi sheet
all_data = []

for sheet in sheet_names:
    # Đọc sheet hiện tại
    df = pd.read_excel(file_path, sheet_name=sheet)

    # Kiểm tra các cột cần lấy có tồn tại không
    required_cols = ['Campaign Name', 'Story ID', 'Link']
    available_cols = [col for col in required_cols if col in df.columns]

    # Nếu có đủ cột thì xử lý
    if len(available_cols) == len(required_cols):
        # Chỉ lấy các cột cần
        df = df[required_cols].copy()

        # Thêm cột 'Account' bằng tên sheet
        df['Account'] = sheet
        df['SKU'] = df['Campaign Name'].apply(SKU)
        # Thêm vào danh sách tổng
        all_data.append(df)

# Gộp tất cả sheet lại
combined_df = pd.concat(all_data, ignore_index=True)

# Xoá các dòng trùng lặp hoàn toàn (cùng Campaign Name, Story ID, Link, Account)
deduplicated_df = combined_df.drop_duplicates()

# Xem kết quả

deduplicated_df.to_excel("output.xlsx", index=False)
print("all done")
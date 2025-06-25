import pandas as pd
from playwright.sync_api import sync_playwright

# Đọc Excel
file_path = "./check.xlsx"  # <- sửa thành đúng đường dẫn
df = pd.read_excel(file_path)

# Thêm cột kết quả
df["Actual Title"] = ""
df["Match"] = ""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for index, row in df.iterrows():
        url = row["Link"]
        expected_title = str(row["Title"]).strip()

        try:
            # Truy cập URL với timeout nhỏ
            page.goto(url, timeout=10000)

            # Nếu có nhập password
            if page.locator("#Password").is_visible(timeout=2000):
                page.fill("#Password", "dx2025")
                page.press("#Password", "Enter")

            # Đợi trang load hoàn toàn (document.onload)
            page.wait_for_load_state("load", timeout=5000)

            # Lấy <h1> sau khi trang đã load
            h1 = page.query_selector('h1.wp-leading-6.md\\:wp-leading-7.wp-text-black')
            if h1:
                actual_title = h1.inner_text().strip()
                df.at[index, "Actual Title"] = actual_title
                df.at[index, "Match"] = "✅" if actual_title.lower() == expected_title.lower() else "❌"
            else:
                df.at[index, "Actual Title"] = "Không tìm thấy <h1>"
                df.at[index, "Match"] = "❌"

        except Exception as e:
            df.at[index, "Actual Title"] = f"Lỗi: {e}"
            df.at[index, "Match"] = "❌"

    browser.close()

# Lưu kết quả
df.to_excel("result_checked_titles_playwright.xlsx", index=False)
print("✅ Xong! File kết quả: result_checked_titles_playwright.xlsx")

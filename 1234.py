import streamlit as st
import json
import os

st.set_page_config(page_title="مدیریت مالی", layout="centered")

st.title("💰 اپلیکیشن مدیریت مالی شخصی")

# فایل ذخیره‌سازی
DATA_FILE = "transactions.json"

# بارگذاری داده‌ها از فایل
if "transactions" not in st.session_state:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            st.session_state.transactions = json.load(f)
    else:
        st.session_state.transactions = []

# دسته‌بندی‌های پیش‌فرض
default_income_categories = ["حقوق", "پول تو جیبی", "قرض", "سایر", "طلبکاری"]
default_expense_categories = ["خوراکی", "تفریح", "حمل و نقل", "قبض", "سایر", "بدهکاری"]

# بارگذاری دسته‌بندی‌ها در session
if 'income_categories' not in st.session_state:
    st.session_state.income_categories = default_income_categories.copy()
if 'expense_categories' not in st.session_state:
    st.session_state.expense_categories = default_expense_categories.copy()

# تابع ذخیره داده‌ها در فایل
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.transactions, f)

# فرم افزودن دسته‌بندی
st.sidebar.header("➕ افزودن دسته‌بندی جدید")
new_cat_type = st.sidebar.selectbox("نوع تراکنش", ["درآمد", "هزینه"])
new_category = st.sidebar.text_input("نام دسته‌بندی")

if st.sidebar.button("افزودن دسته‌بندی"):
    if new_category.strip() == "":
        st.sidebar.error("نام دسته‌بندی نمی‌تواند خالی باشد!")
    else:
        if new_cat_type == "درآمد":
            if new_category not in st.session_state.income_categories:
                st.session_state.income_categories.append(new_category)
                st.sidebar.success(f"'{new_category}' به درآمدها اضافه شد.")
            else:
                st.sidebar.warning("این دسته‌بندی قبلاً وجود دارد.")
        else:
            if new_category not in st.session_state.expense_categories:
                st.session_state.expense_categories.append(new_category)
                st.sidebar.success(f"'{new_category}' به هزینه‌ها اضافه شد.")
            else:
                st.sidebar.warning("این دسته‌بندی قبلاً وجود دارد.")

# فیلتر تراکنش‌ها
st.sidebar.header("🔍 فیلتر")
filter_type = st.sidebar.selectbox("نوع تراکنش:", ["همه", "درآمد", "هزینه"])
filter_category = st.sidebar.text_input("جستجو در دسته‌بندی")

# فرم ثبت تراکنش
st.header("➕ ثبت تراکنش")

type_ = st.selectbox("نوع تراکنش:", ["درآمد", "هزینه"])

if type_ == "درآمد":
    category = st.selectbox("دسته‌بندی:", st.session_state.income_categories)
else:
    category = st.selectbox("دسته‌بندی:", st.session_state.expense_categories)

amount = st.number_input("مبلغ", min_value=0.0, step=1000.0)
desc = st.text_input("توضیح")

if st.button("ثبت"):
    if amount == 0:
        st.error("مبلغ باید بیشتر از صفر باشد.")
    else:
        st.session_state.transactions.append({
            "نوع": type_,
            "دسته‌بندی": category,
            "مبلغ": amount,
            "توضیح": desc
        })
        save_data()
        st.success("تراکنش ثبت شد!")

st.divider()

# نمایش تراکنش‌ها با فیلتر و حذف
st.header("📋 لیست تراکنش‌ها")

filtered = []
for index, t in enumerate(st.session_state.transactions):
    if filter_type != "همه" and t["نوع"] != filter_type:
        continue
    if filter_category and filter_category not in t["دسته‌بندی"]:
        continue
    filtered.append((index, t))

if filtered:
    for index, t in filtered:
        col1, col2 = st.columns([6, 1])
        with col1:
            st.write(f"**{t['نوع']}** - {t['دسته‌بندی']} - {t['مبلغ']} تومان - {t['توضیح']}")
        with col2:
            if st.button("❌", key=f"del_{index}"):
                st.session_state.transactions.pop(index)
                save_data()
                st.experimental_rerun()
else:
    st.info("هیچ تراکنشی با این شرایط پیدا نشد.")

st.divider()

# گزارش مالی
st.header("📊 گزارش مالی")

income = sum(t['مبلغ'] for t in st.session_state.transactions if t['نوع'] == "درآمد")
expense = sum(t['مبلغ'] for t in st.session_state.transactions if t['نوع'] == "هزینه")
balance = income - expense

st.write(f"💵 کل درآمد: {income} تومان")
st.write(f"💸 کل هزینه: {expense} تومان")
st.write(f"💼 موجودی نهایی: {balance} تومان")

# گزارش بر اساس دسته‌بندی‌ها
st.subheader("📂 گزارش دسته‌بندی‌ها")

def category_report(transactions, category_list, type_label):
    st.markdown(f"**{type_label} بر اساس دسته‌بندی:**")
    for cat in category_list:
        total = sum(t["مبلغ"] for t in transactions if t["نوع"] == type_label and t["دسته‌بندی"] == cat)
        if total > 0:
            st.write(f"🔸 {cat}: {total} تومان")

category_report(st.session_state.transactions, st.session_state.income_categories, "درآمد")
category_report(st.session_state.transactions, st.session_state.expense_categories, "هزینه")
#made by ai and madsin
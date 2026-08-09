import streamlit as st
from supabase import create_client, Client
import pandas as pd
from streamlit_option_menu import option_menu
import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="إدارة الاستوديو المحاسبي", page_icon="📸", layout="wide")

# 2. بيانات الاتصال بـ Supabase
SUPABASE_URL = "https://anzwtotkfhneucjmuwvp.supabase.co"
SUPABASE_KEY = "حط_هنا_المفتاح_اللي_نسخته"

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# 3. القائمة الجانبية
with st.sidebar:
    st.title("📸 سيستم الاستوديو")
    selected = option_menu(
        "القائمة الرئيسية",
        ["الرئيسية والتقارير", "قطع تذاكر أفراد", "حجوزات الأفراح", "الموظفين والسُلف", "المصروفات العامة"],
        icons=['graph-up-arrow', 'ticket-perforated', 'calendar-event', 'people', 'cash-stack'],
        menu_icon="cast", default_index=0
    )

# ---------------------------------------------------------
# الشاشة 1: الرئيسية والتقارير
# ---------------------------------------------------------
if selected == "الرئيسية والتقارير":
    st.title("📊 الملخص المالي والإحصائيات")
    
    # جلب البيانات من Supabase
    b_data = pd.DataFrame(supabase.table("bookings").select("*").execute().data)
    t_data = pd.DataFrame(supabase.table("tickets").select("*").execute().data)
    e_data = pd.DataFrame(supabase.table("expenses").select("*").execute().data)
    a_data = pd.DataFrame(supabase.table("attendance_and_advances").select("*").execute().data)

    total_tickets = t_data['total_price'].sum() if not t_data.empty else 0
    total_bookings = b_data['paid_amount'].sum() if not b_data.empty else 0
    total_income = total_tickets + total_bookings
    
    gen_expenses = e_data['amount'].sum() if not e_data.empty else 0
    total_advances = a_data['advance_amount'].sum() if not a_data.empty else 0
    total_expenses = gen_expenses + total_advances
    
    net_profit = total_income - total_expenses

    col1, col2, col3 = st.columns(3)
    col1.metric("إجمالي الإيرادات (تذاكر + حجوزات)", f"{total_income:,.0f} ج.م")
    col2.metric("إجمالي المصروفات والسُلف", f"{total_expenses:,.0f} ج.م")
    col3.metric("صافي الأرباح", f"{net_profit:,.0f} ج.م")

    st.markdown("---")
    st.subheader("تفاصيل سريعة")
    c1, c2 = st.columns(2)
    c1.write(f"🎟️ إيراد التذاكر اليومية: **{total_tickets:,.0f} ج.م**")
    c1.write(f"💍 عرباين وحجوزات الأفراح: **{total_bookings:,.0f} ج.م**")
    c2.write(f"💸 المصروفات العامة: **{gen_expenses:,.0f} ج.م**")
    c2.write(f"💵 إجمالي سُلف العاملين: **{total_advances:,.0f} ج.م**")

# ---------------------------------------------------------
# الشاشة 2: قطع تذاكر أفراد (شاشة سريعة للقطع اليومي)
# ---------------------------------------------------------
elif selected == "قطع تذاكر أفراد":
    st.title("🎟️ شاشة قطع التذاكر السريعة")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("تذكرة جديدة")
        with st.form("ticket_form", clear_on_submit=True):
            ticket_count = st.number_input("عدد التذاكر / الأفراد", min_value=1, value=1, step=1)
            price_per_ticket = st.number_input("سعر التذكرة للفرد", min_value=1, value=50, step=10)
            
            total = ticket_count * price_per_ticket
            st.markdown(f"### الإجمالي: **{total} ج.م**")
            
            submit = st.form_submit_button("قطع وحفظ التذكرة ⚡")
            if submit:
                supabase.table("tickets").insert({
                    "ticket_count": ticket_count,
                    "price_per_ticket": price_per_ticket,
                    "total_price": total
                }).execute()
                st.success("تم تسجيل التذكرة بنجاح!")
                st.rerun()

    with col2:
        st.subheader("سجل التذاكر اليوم")
        tickets_list = supabase.table("tickets").select("*").order("id", desc=True).limit(10).execute().data
        if tickets_list:
            st.dataframe(pd.DataFrame(tickets_list)[['id', 'created_at', 'ticket_count', 'price_per_ticket', 'total_price']], use_container_width=True)

# ---------------------------------------------------------
# الشاشة 3: حجوزات الأفراح والسيشنز
# ---------------------------------------------------------
elif selected == "حجوزات الأفراح":
    st.title("💍 إدارة حجوزات الأفراح والسيشنز")
    
    tab1, tab2 = st.tabs(["إضافة حجز جديد", "عرض كل الحجوزات"])
    
    with tab1:
        with st.form("booking_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            client_name = c1.text_input("اسم العريس / العروسة")
            phone = c2.text_input("رقم الهاتف")
            
            event_date = c1.date_input("تاريخ السيشن / الفرح")
            package_type = c2.selectbox("نوع الباقة", ["سيشن عادي", "فرح كامل", "فوتوبوك فقط", "سيشن + فيديو"])
            
            total_amount = c1.number_input("إجمالي اتفاق السيشن", min_value=0, step=500)
            paid_amount = c2.number_input("العربون المدفوع", min_value=0, step=100)
            notes = st.text_area("ملاحظات")
            
            if st.form_submit_button("حفظ الحجز"):
                if client_name and total_amount > 0:
                    supabase.table("bookings").insert({
                        "client_name": client_name,
                        "phone": phone,
                        "event_date": str(event_date),
                        "package_type": package_type,
                        "total_amount": total_amount,
                        "paid_amount": paid_amount,
                        "notes": notes
                    }).execute()
                    st.success("تم حفظ الحجز!")
                else:
                    st.error("برجاء إدخال اسم العميل والمبلغ!")

    with tab2:
        b_data = supabase.table("bookings").select("*").execute().data
        if b_data:
            df = pd.DataFrame(b_data)
            df['المتبقي'] = df['total_amount'] - df['paid_amount']
            st.dataframe(df[['client_name', 'phone', 'event_date', 'package_type', 'total_amount', 'paid_amount', 'المتبقي', 'notes']], use_container_width=True)

# ---------------------------------------------------------
# الشاشة 4: الموظفين والسُلف والحضور
# ---------------------------------------------------------
elif selected == "الموظفين والسُلف":
    st.title("👥 إدارة العمالة والسُلف")
    
    tab1, tab2 = st.tabs(["تسجيل سُلفة / حضور", "إضافة موظف جديد"])
    
    with tab1:
        emp_data = supabase.table("employees").select("*").execute().data
        if emp_data:
            emp_dict = {e['name']: e['id'] for e in emp_data}
            selected_emp = st.selectbox("اختار الموظف / العامل", list(emp_dict.keys()))
            
            with st.form("adv_form", clear_on_submit=True):
                status = st.selectbox("حالة الحضور", ["حضور", "غياب", "إجازة"])
                advance = st.number_input("مبلغ السلفة (إن وجد)", min_value=0, step=50)
                notes = st.text_input("ملاحظات")
                
                if st.form_submit_button("تسجيل"):
                    supabase.table("attendance_and_advances").insert({
                        "employee_id": emp_dict[selected_emp],
                        "status": status,
                        "advance_amount": advance,
                        "notes": notes
                    }).execute()
                    st.success("تم التسجيل بنجاح!")
        else:
            st.info("قم بإضافة موظفين أولاً من التاب المجاور.")

    with tab2:
        with st.form("emp_form", clear_on_submit=True):
            emp_name = st.text_input("اسم الموظف / العمال")
            daily_rate = st.number_input("اليومية / الأجر", min_value=0, step=50)
            phone = st.text_input("رقم التليفون")
            if st.form_submit_button("حفظ الموظف"):
                supabase.table("employees").insert({"name": emp_name, "daily_rate": daily_rate, "phone": phone}).execute()
                st.success("تمت إضافة الموظف!")

# ---------------------------------------------------------
# الشاشة 5: المصروفات العامة
# ---------------------------------------------------------
elif selected == "المصروفات العامة":
    st.title("💸 المصروفات والنفقات")
    
    with st.form("exp_form", clear_on_submit=True):
        category = st.selectbox("نوع المصروف", ["إيجار", "كهرباء ومرافق", "معدات وصيانة", "بوفيه وضيافة", "أخرى"])
        amount = st.number_input("المبلغ", min_value=1, step=50)
        desc = st.text_input("وصف المصروف")
        
        if st.form_submit_button("تسجيل المصروف"):
            supabase.table("expenses").insert({"category": category, "amount": amount, "description": desc}).execute()
            st.success("تم تسجيل المصروف بنجاح!")

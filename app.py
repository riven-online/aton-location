import streamlit as st
import pandas as pd
from supabase import create_client, Client

# --- ضبط إعدادات الصفحة ---
st.set_page_config(
    page_title="سيستم الاستوديو",
    page_icon="🎬",
    layout="wide"
)

# --- الاتصال بقاعدة البيانات ---
try:
    url = str(st.secrets["SUPABASE_URL"]).strip()
    key = str(st.secrets["SUPABASE_KEY"]).strip()
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error(f"خطأ في الاتصال بقاعدة البيانات: {e}")
    st.stop()

# --- القائمة الجانبية (Sidebar Navigation) ---
st.sidebar.title("سيستم الاستوديو")
page = st.sidebar.radio(
    "القائمة الرئيسية",
    ["الرئيسية والتقارير", "قطع تذاكر أفراد", "حجوزات الأفراح", "الموظفين والسُلف", "المصروفات العامة"]
)

# ==========================================
# الصفحة 1: الرئيسية والتقارير
# ==========================================
if page == "الرئيسية والتقارير":
    st.header("📊 الملخص المالي والإحصائيات")
    
    try:
        b_data = pd.DataFrame(supabase.table("bookings").select("*").execute().data)
        t_data = pd.DataFrame(supabase.table("tickets").select("*").execute().data)
        e_data = pd.DataFrame(supabase.table("expenses").select("*").execute().data)

        col1, col2, col3 = st.columns(3)
        
        total_bookings = b_data['paid_amount'].sum() if not b_data.empty and 'paid_amount' in b_data else 0
        total_tickets = t_data['total_price'].sum() if not t_data.empty and 'total_price' in t_data else 0
        total_expenses = e_data['amount'].sum() if not e_data.empty and 'amount' in e_data else 0

        col1.metric("إجمالي الحجوزات", f"{total_bookings:,.0f} ج.م")
        col2.metric("إجمالي التذاكر", f"{total_tickets:,.0f} ج.م")
        col3.metric("إجمالي المصروفات", f"{total_expenses:,.0f} ج.م")

        st.divider()
        st.subheader("📋 أحدث الحجوزات")
        if not b_data.empty:
            st.dataframe(b_data, use_container_width=True)
        else:
            st.info("لا توجد حجوزات مسجلة حتى الآن.")

    except Exception as ex:
        st.error(f"حدث خطأ أثناء تحميل البيانات: {ex}")

# ==========================================
# الصفحة 2: قطع تذاكر أفراد
# ==========================================
elif page == "قطع تذاكر أفراد":
    st.header("🎟️ سجِل تذاكر اليوم")
    
    with st.container():
        st.subheader("تذكرة جديدة")
        count = st.number_input("عدد التذاكر / الأفراد", min_value=1, value=1, step=1)
        price_per_ticket = st.number_input("سعر التذكرة للفرد", min_value=0, value=50, step=5)
        total = count * price_per_ticket
        
        st.subheader(f"الإجمالي: {total:,.0f} ج.م")

        if st.button("🎫 قطع وحفظ التذكرة"):
            try:
                supabase.table("tickets").insert({
                    "count": count,
                    "price_per_ticket": price_per_ticket,
                    "total_price": total
                }).execute()
                st.success("تم قطع التذكرة وحفظها بنجاح!")
                st.rerun()
            except Exception as ex:
                st.error(f"فشل حفظ التذكرة: {ex}")

    st.divider()
    st.subheader("📋 سجل التذاكر")
    try:
        tickets_list = supabase.table("tickets").select("*").order("id", desc=True).execute().data
        if tickets_list:
            st.dataframe(pd.DataFrame(tickets_list), use_container_width=True)
        else:
            st.info("لم يتم قطع أي تذاكر اليوم.")
    except Exception as ex:
        st.error(f"حدث خطأ أثناء جلب التذاكر: {ex}")

# ==========================================
# الصفحة 3: حجوزات الأفراح
# ==========================================
elif page == "حجوزات الأفراح":
    st.header("💍 إدارة حجوزات الأفراح والسيشن")
    
    with st.form("booking_form", clear_on_submit=True):
        st.subheader("إضافة حجز جديد")
        col1, col2 = st.columns(2)
        
        with col1:
            client_name = st.text_input("اسم العريس / العروسة")
            session_date = st.date_input("تاريخ السيشن / الفرح")
            total_agreed = st.number_input("إجمالي الاتفاق السيشن", min_value=0, value=0)
            
        with col2:
            phone = st.text_input("رقم الهاتف")
            session_type = st.selectbox("نوع القاعة", ["سيشن عادي", "سيشن مميز", "فرح كامل"])
            paid_amount = st.number_input("العربون المدفوع", min_value=0, value=0)

        notes = st.text_area("ملاحظات")
        submit = st.form_submit_button("حفظ الحجز")

        if submit:
            if not client_name:
                st.warning("يرجى إدخال اسم العريس / العروسة.")
            else:
                try:
                    supabase.table("bookings").insert({
                        "client_name": client_name,
                        "phone": phone,
                        "session_date": str(session_date),
                        "session_type": session_type,
                        "total_agreed": total_agreed,
                        "paid_amount": paid_amount,
                        "notes": notes
                    }).execute()
                    st.success("تم حفظ الحجز بنجاح!")
                    st.rerun()
                except Exception as ex:
                    st.error(f"فشل حفظ الحجز: {ex}")

    st.divider()
    st.subheader("📋 الحجوزات المسجلة")
    try:
        b_data = supabase.table("bookings").select("*").order("id", desc=True).execute().data
        if b_data:
            st.dataframe(pd.DataFrame(b_data), use_container_width=True)
        else:
            st.info("لا توجد حجوزات مسجلة.")
    except Exception as ex:
        st.error(f"حدث خطأ أثناء جلب الحجوزات: {ex}")

# ==========================================
# الصفحة 4: الموظفين والسُلف
# ==========================================
elif page == "الموظفين والسُلف":
    st.header("👥 إدارة العمالة والسُلف")
    
    tab1, tab2 = st.tabs(["إضافة موظف جديد", "تسجيل سُلفة / حضور"])

    with tab1:
        emp_name = st.text_input("اسم الموظف")
        emp_role = st.text_input("الوظيفة")
        daily_rate = st.number_input("اليومية / الرواتب", min_value=0, value=0)
        
        if st.button("حفظ الموظف"):
            if emp_name:
                try:
                    supabase.table("employees").insert({
                        "name": emp_name,
                        "role": emp_role,
                        "daily_rate": daily_rate
                    }).execute()
                    st.success("تمت إضافة الموظف بنجاح!")
                    st.rerun()
                except Exception as ex:
                    st.error(f"فشل إضافة الموظف: {ex}")

    with tab2:
        try:
            emp_data = supabase.table("employees").select("*").execute().data
            if emp_data:
                emp_df = pd.DataFrame(emp_data)
                selected_emp = st.selectbox("اختر الموظف", emp_df["name"].tolist())
                advance_amount = st.number_input("مبلغ السُلفة", min_value=0, value=0)
                
                if st.button("تسجيل السُلفة"):
                    supabase.table("expenses").insert({
                        "category": f"سُلفة - {selected_emp}",
                        "amount": advance_amount,
                        "description": f"سُلفة للموظف {selected_emp}"
                    }).execute()
                    st.success(f"تم تسجيل سُلفة بقيمة {advance_amount} ج.م للموظف {selected_emp}")
            else:
                st.info("يرجى إضافة موظفين أولاً.")
        except Exception as ex:
            st.error(f"حدث خطأ أثناء تحميل بيانات الموظفين: {ex}")

# ==========================================
# الصفحة 5: المصروفات العامة
# ==========================================
elif page == "المصروفات العامة":
    st.header("💸 المصروفات والنفقات")
    
    with st.form("expense_form", clear_on_submit=True):
        category = st.selectbox("نوع المصروف", ["إيجار", "كهرباء ومياه", "صيانة ومعدات", "بوفيه وضيافة", "أخرى"])
        amount = st.number_input("المبلغ", min_value=1, value=1)
        description = st.text_area("وصف المصروف")
        
        if st.form_submit_button("تسجيل المصروف"):
            try:
                supabase.table("expenses").insert({
                    "category": category,
                    "amount": amount,
                    "description": description
                }).execute()
                st.success("تم تسجيل المصروف بنجاح!")
                st.rerun()
            except Exception as ex:
                st.error(f"فشل تسجيل المصروف: {ex}")

    st.divider()
    st.subheader("📋 سجل المصروفات")
    try:
        e_data = supabase.table("expenses").select("*").order("id", desc=True).execute().data
        if e_data:
            st.dataframe(pd.DataFrame(e_data), use_container_width=True)
        else:
            st.info("لا توجد مصروفات مسجلة.")
    except Exception as ex:
        st.error(f"حدث خطأ أثناء جلب المصروفات: {ex}")

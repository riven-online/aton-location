import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime, time, date

# ==========================================
# 1. تهيئة الصفحة والأنماط البصرية (Custom CSS)
# ==========================================
st.set_page_config(
    page_title="آتون لوكيشن | Aton Location",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .stApp {
        background-color: #0f1117;
        color: #e0e6ed;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e2430 0%, #151922 100%);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 12px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    .metric-title {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-bottom: 6px;
        font-weight: 600;
    }
    .metric-value {
        color: #d4af37;
        font-size: 1.7rem;
        font-weight: 800;
    }

    .stButton>button {
        background: linear-gradient(135deg, #d4af37 0%, #aa7c11 100%);
        color: #000000 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        width: 100%;
    }
    
    .invoice-box {
        max-width: 380px;
        margin: auto;
        padding: 20px;
        border: 2px solid #d4af37;
        border-radius: 10px;
        background-color: #ffffff;
        color: #000000;
        font-family: 'Cairo', sans-serif;
        box-shadow: 0 5px 15px rgba(0,0,0,0.5);
    }
    .invoice-header {
        text-align: center;
        border-bottom: 2px dashed #333;
        padding-bottom: 10px;
        margin-bottom: 12px;
    }
    .brand-title {
        font-size: 22px;
        font-weight: 800;
        color: #000;
        margin: 0;
    }
    .brand-subtitle {
        font-size: 12px;
        color: #555;
        margin-bottom: 4px;
    }
    .invoice-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 6px;
        font-size: 13px;
        color: #111;
    }
    .invoice-total {
        border-top: 2px dashed #333;
        padding-top: 8px;
        margin-top: 10px;
        font-size: 15px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. الاتصال بقاعدة البيانات Supabase
# ==========================================
try:
    url = str(st.secrets["SUPABASE_URL"]).strip()
    key = str(st.secrets["SUPABASE_KEY"]).strip()
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error(f"خطأ في الاتصال بقاعدة البيانات: {e}")
    st.stop()

# ==========================================
# 3. القائمة الجانبية
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #d4af37;'>🎬 آتون لوكيشن</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 12px; color: #aaa;'>Aton Location Studio</p>", unsafe_allow_html=True)
    st.divider()
    
    page = st.radio(
        "الانتقال السريع",
        [
            "💍 حجوزات الأفراح والتقويم",
            "🎟️ حجز تذاكر أفراد",
            "📊 لوحة التحكم والتقارير",
            "📷 عهدة ومعدات التصوير",
            "💸 المصروفات والنفقات",
            "👥 العمالة والسُلف"
        ]
    )
    st.divider()
    st.caption("تاريخ اليوم: " + datetime.now().strftime("%Y-%m-%d"))

# ==========================================
# الصفحة 1: حجوزات الأفراح والتقويم
# ==========================================
if page == "💍 حجوزات الأفراح والتقويم":
    st.markdown("<h2 style='color: #d4af37;'>💍 حجز سيشن وتقويم المواعيد - آتون لوكيشن</h2>", unsafe_allow_html=True)
    
    tab_new, tab_cal, tab_list = st.tabs(["📝 حجز جديد وإيصال", "📅 تقويم الاستعلام عن الايام", "📋 كل الحجوزات"])

    with tab_new:
        col_input, col_preview = st.columns([1.2, 1])
        
        with col_input:
            st.subheader("بيانات السيشن والموعد")
            
            client_name = st.text_input("اسم العريس / العروسة", key="c_name")
            phone = st.text_input("رقم الهاتف", key="c_phone")
            
            session_type = st.selectbox(
                "اختر الباقة / نوع الجلسة", 
                ["سيشن عادي", "سيشن مميز", "باقة الفرح الكامل", "فوتوسيشن خارجي", "تخصيص يدوي"],
                key="s_type"
            )
            
            c1, c2 = st.columns(2)
            with c1:
                session_date = st.date_input("تاريخ السيشن", value=date.today(), key="s_date")
                start_t = st.time_input("وقت البداية", value=time(15, 0), key="s_start")
                location_room = st.selectbox("اللوكيشن / الغرفة المطلوبة", ["اللوكيشن الكلاسيك", "اللوكيشن المودرن", "غرفة الميك أب والتجهيز", "الاستوديو بالكامل"], key="s_loc")
            with c2:
                end_t = st.time_input("وقت النهاية المتوقع", value=time(16, 0), key="s_end")
                total_agreed = st.number_input("إجمالي قيمة الاتفاق (ج.م)", min_value=0, value=600, step=50, key="s_total")
                paid_amount = st.number_input("العربون المدفوع (ج.م)", min_value=0, value=200, step=50, key="s_paid")

            photographer_commission = st.number_input("عمولة / إكرامية المصور (إن وجد)", min_value=0, value=0, step=50, key="s_comm")
            notes = st.text_area("ملاحظات إضافية", key="s_notes")

            if st.button("💾 تأكيد وحفظ الحجز"):
                if not client_name:
                    st.warning("يرجى إدخال اسم العميل.")
                else:
                    payload = {
                        "client_name": client_name,
                        "phone": phone,
                        "session_date": str(session_date),
                        "session_type": session_type,
                        "total_agreed": total_agreed,
                        "paid_amount": paid_amount,
                        "start_time": str(start_t),
                        "end_time": str(end_t),
                        "location_room": location_room,
                        "photographer_commission": photographer_commission,
                        "notes": notes
                    }
                    try:
                        supabase.table("bookings").insert(payload).execute()
                        st.success("تم تأكيد الحجز وحفظ الموعد بنجاح!")
                        st.rerun()
                    except Exception as ex:
                        # في حال كان اسم العمود في السيرفر booking_date بدلاً من session_date
                        try:
                            payload["booking_date"] = payload.pop("session_date")
                            supabase.table("bookings").insert(payload).execute()
                            st.success("تم تأكيد الحجز وحفظ الموعد بنجاح!")
                            st.rerun()
                        except Exception as ex2:
                            st.error(f"حدث خطأ أثناء الحفظ: {ex2}")

        with col_preview:
            st.subheader("📄 إيصال حجز السيشن (جاهز للطباعة)")
            rem_calc = total_agreed - paid_amount
            
            receipt_html = f"""
            <div class="invoice-box">
                <div class="invoice-header">
                    <div class="brand-title">آتون لوكيشن</div>
                    <div class="brand-subtitle">ATON LOCATION STUDIO</div>
                    <div style="font-size: 11px; font-weight: bold; color: #444; margin-top:5px;">إيصال حجز وتأكيد موعد</div>
                </div>
                <div class="invoice-row"><span>اسم العميل:</span> <strong>{client_name if client_name else '...................'}</strong></div>
                <div class="invoice-row"><span>رقم الهاتف:</span> <strong>{phone if phone else '...................'}</strong></div>
                <div class="invoice-row"><span>نوع الباقة:</span> <strong>{session_type}</strong></div>
                <div class="invoice-row"><span>اللوكيشن:</span> <strong>{location_room}</strong></div>
                <div class="invoice-row"><span>التاريخ:</span> <strong>{session_date}</strong></div>
                <div class="invoice-row"><span>توقيت السيشن:</span> <strong>من {start_t.strftime('%H:%M')} إلى {end_t.strftime('%H:%M')}</strong></div>
                <hr style="border:0.5px dashed #666; margin:8px 0;">
                <div class="invoice-row"><span>إجمالي المبلغ:</span> <strong>{total_agreed:,.0f} ج.م</strong></div>
                <div class="invoice-row"><span>العربون المدفوع:</span> <strong style="color:green;">{paid_amount:,.0f} ج.م</strong></div>
                <div class="invoice-total invoice-row">
                    <span>المتبقي عند الحضور:</span>
                    <span style="color:red;">{rem_calc:,.0f} ج.م</span>
                </div>
                <div style="text-align:center; font-size:10px; color:#666; margin-top:12px;">
                    شكراً لاختياركم آتون لوكيشن ✨<br>يرجى الحضور في الموعد المحدد تماماً
                </div>
            </div>
            """
            st.markdown(receipt_html, unsafe_allow_html=True)

    with tab_cal:
        st.subheader("📅 تقويم استعلام المواعيد والسيشنات اليومية")
        st.caption("اختر أي يوم لتحديد كم سيشن محجوز فيه ومواعيد بداية ونهاية كل سيشن بالتفصيل:")
        
        search_date = st.date_input("اختر اليوم للتحقق من الحجوزات", value=date.today(), key="cal_search")
        
        try:
            # جلب كافة البيانات وتنقيتها محلياً لتفادي تفاوت أسماء الأعمدة في Supabase
            all_bookings = supabase.table("bookings").select("*").execute().data
            
            day_bookings = []
            if all_bookings:
                for b in all_bookings:
                    # فحص العمود سواء كان session_date أو booking_date أو date أو created_at
                    b_date = str(b.get('session_date') or b.get('booking_date') or b.get('date') or '').split('T')[0]
                    if b_date == str(search_date):
                        day_bookings.append(b)

            if day_bookings:
                st.success(f"📌 يوجد عدد **({len(day_bookings)})** سيشن محجوز في يوم {search_date}:")
                
                for idx, b in enumerate(day_bookings, 1):
                    s_t = str(b.get('start_time', 'غير محدد'))[:5]
                    e_t = str(b.get('end_time', 'غير محدد'))[:5]
                    c_name = b.get('client_name', 'عميل')
                    loc = b.get('location_room', 'اللوكيشن')
                    
                    with st.expander(f"🎬 سيشن رقم {idx}: {c_name} | ⏰ من {s_t} إلى {e_t} ({loc})"):
                        c_a, c_b, c_c = st.columns(3)
                        c_a.write(f"**العميل:** {c_name}")
                        c_a.write(f"**الهاتف:** {b.get('phone', '-')}")
                        c_b.write(f"**نوع السيشن:** {b.get('session_type', '-')}")
                        c_b.write(f"**اللوكيشن:** {loc}")
                        tot = float(b.get('total_agreed', 0) or 0)
                        pd_val = float(b.get('paid_amount', 0) or 0)
                        c_c.write(f"**الاتفاق:** {tot:,.0f} ج.م")
                        c_c.write(f"**المتبقي:** {tot - pd_val:,.0f} ج.م")
            else:
                st.info(f"✨ يوم {search_date} فارغ تماماً ولا يوجد به أي حجوزات حتى الآن.")

        except Exception as ex:
            st.error(f"خطأ أثناء جلب المواعيد: {ex}")

    with tab_list:
        st.subheader("📋 سجل الحجوزات الكامل")
        try:
            b_list = supabase.table("bookings").select("*").execute().data
            if b_list:
                df_b = pd.DataFrame(b_list)
                st.dataframe(df_b, use_container_width=True)
            else:
                st.info("لا توجد حجوزات مسجلة حالياً.")
        except Exception as ex:
            st.error(f"خطأ في التحميل: {ex}")

# ==========================================
# الصفحة 2: حجز تذاكر أفراد
# ==========================================
elif page == "🎟️ حجز تذاكر أفراد":
    st.markdown("<h2 style='color: #d4af37;'>🎟️ قطع تذاكر أفراد - آتون لوكيشن</h2>", unsafe_allow_html=True)
    
    col_t1, col_t2 = st.columns([1.2, 1])
    
    with col_t1:
        st.subheader("بيانات التذكرة")
        count = st.number_input("عدد الأفراد", min_value=1, value=1, key="t_count")
        price_per_ticket = st.number_input("سعر التذكرة للفرد (ج.م)", min_value=1, value=50, key="t_price")
        total_price = count * price_per_ticket
        st.markdown(f"### الإجمالي المطلوب: **{total_price:,.0f} ج.م**")
        
        if st.button("🎫 حفظ وقطع التذكرة"):
            try:
                supabase.table("tickets").insert({
                    "count": count,
                    "price_per_ticket": price_per_ticket,
                    "total_price": total_price
                }).execute()
                st.success("تم تسجيل التذكرة بنجاح!")
            except Exception as ex:
                st.error(f"خطأ: {ex}")

    with col_t2:
        st.subheader("📄 إيصال تذكرة دخول (جاهز للطباعة)")
        ticket_receipt_html = f"""
        <div class="invoice-box">
            <div class="invoice-header">
                <div class="brand-title">آتون لوكيشن</div>
                <div class="brand-subtitle">ATON LOCATION STUDIO</div>
                <div style="font-size: 11px; font-weight: bold; color: #444; margin-top:5px;">تذكرة دخول أفراد</div>
            </div>
            <div class="invoice-row"><span>التاريخ والوقت:</span> <strong>{datetime.now().strftime('%Y-%m-%d %H:%M')}</strong></div>
            <div class="invoice-row"><span>عدد الأفراد:</span> <strong>{count} فرد</strong></div>
            <div class="invoice-row"><span>سعر الفرد:</span> <strong>{price_per_ticket:,.0f} ج.م</strong></div>
            <hr style="border:0.5px dashed #666; margin:8px 0;">
            <div class="invoice-total invoice-row">
                <span>المبلغ الإجمالي المدفوع:</span>
                <span style="color:green;">{total_price:,.0f} ج.م</span>
            </div>
            <div style="text-align:center; font-size:10px; color:#666; margin-top:12px;">
                نتمنى لكم وقتاً ممتعاً في آتون لوكيشن 📸
            </div>
        </div>
        """
        st.markdown(ticket_receipt_html, unsafe_allow_html=True)

# ==========================================
# الصفحة 3: لوحة التحكم والتقارير
# ==========================================
elif page == "📊 لوحة التحكم والتقارير":
    st.markdown("<h2 style='color: #d4af37;'>📊 الميزانية والتقارير التحليلية</h2>", unsafe_allow_html=True)
    
    try:
        b_res = supabase.table("bookings").select("*").execute().data
        t_res = supabase.table("tickets").select("*").execute().data
        e_res = supabase.table("expenses").select("*").execute().data

        b_df = pd.DataFrame(b_res) if b_res else pd.DataFrame()
        t_df = pd.DataFrame(t_res) if t_res else pd.DataFrame()
        e_df = pd.DataFrame(e_res) if e_res else pd.DataFrame()

        total_bookings_income = b_df['paid_amount'].sum() if not b_df.empty and 'paid_amount' in b_df else 0
        total_tickets_income = t_df['total_price'].sum() if not t_df.empty and 'total_price' in t_df else 0
        photographer_comm = b_df['photographer_commission'].sum() if not b_df.empty and 'photographer_commission' in b_df else 0
        
        total_income = total_bookings_income + total_tickets_income
        total_expenses = (e_df['amount'].sum() if not e_df.empty and 'amount' in e_df else 0) + photographer_comm
        net_profit = total_income - total_expenses

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f'<div class="metric-card"><div class="metric-title">إيراد التذاكر</div><div class="metric-value">{total_tickets_income:,.0f} ج.م</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card"><div class="metric-title">مقبوضات الحجوزات</div><div class="metric-value">{total_bookings_income:,.0f} ج.م</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-card"><div class="metric-title">المصروفات والعمولات</div><div class="metric-value" style="color:#ef4444;">{total_expenses:,.0f} ج.م</div></div>', unsafe_allow_html=True)
        with c4:
            p_color = "#10b981" if net_profit >= 0 else "#ef4444"
            st.markdown(f'<div class="metric-card"><div class="metric-title">صافي الربح الفعلي</div><div class="metric-value" style="color:{p_color};">{net_profit:,.0f} ج.م</div></div>', unsafe_allow_html=True)

        st.divider()
        st.subheader("📈 الرسم البياني المالي")
        chart_df = pd.DataFrame({
            "البند": ["إيراد تذاكر", "إيراد حجوزات", "مصروفات وعمولات"],
            "المبلغ": [total_tickets_income, total_bookings_income, total_expenses]
        }).set_index("البند")
        st.bar_chart(chart_df)

    except Exception as ex:
        st.error(f"خطأ في إعداد التقارير: {ex}")

# ==========================================
# الصفحة 4: عهدة ومعدات التصوير
# ==========================================
elif page == "📷 عهدة ومعدات التصوير":
    st.markdown("<h2 style='color: #d4af37;'>📷 تتبع عهدة ومعدات التصوير</h2>", unsafe_allow_html=True)
    
    col_eq1, col_eq2 = st.columns([1, 1.2])

    with col_eq1:
        st.subheader("إضافة معدة جديدة")
        with st.form("eq_form", clear_on_submit=True):
            eq_name = st.text_input("اسم المعدة (مثال: كاميرا Sony A7III)")
            eq_cat = st.selectbox("النوع", ["كاميرات", "عدسات", "إضاءات وكشافات", "صوتيات وميكروفونات", "إكسسوارات وحوامل"])
            
            if st.form_submit_button("حفظ في العهدة"):
                if eq_name:
                    try:
                        supabase.table("equipment").insert({
                            "name": eq_name,
                            "category": eq_cat,
                            "status": "متاحة بالاستوديو"
                        }).execute()
                        st.success("تمت إضافة المعدة للعهدة!")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"خطأ أثناء الحفظ: {ex}")

    with col_eq2:
        st.subheader("تحديث حالة المعدة")
        try:
            eq_data = supabase.table("equipment").select("*").execute().data
            if eq_data:
                eq_df = pd.DataFrame(eq_data)
                selected_eq_id = st.selectbox("اختر المعدة", eq_df["id"].tolist(), format_func=lambda x: eq_df[eq_df['id']==x]['name'].values[0])
                
                status_choice = st.radio("الحالة الحالية", ["متاحة بالاستوديو", "خارجة لسيشن خارجي", "تحت الصيانة"])
                assigned_to = st.text_input("اسم المصور المستلم")
                expected_return = st.text_input("موعد العودة المتوقع")

                if st.button("تحديث حالة العهدة"):
                    supabase.table("equipment").update({
                        "status": status_choice,
                        "assigned_to": assigned_to if status_choice == "خارجة لسيشن خارجي" else "",
                        "expected_return": expected_return if status_choice == "خارجة لسيشن خارجي" else ""
                    }).eq("id", selected_eq_id).execute()
                    st.success("تم تحديث حالة المعدة بنجاح!")
                    st.rerun()

                st.divider()
                st.dataframe(eq_df, use_container_width=True)
            else:
                st.info("لا توجد معدات مسجلة بعد.")
        except Exception as ex:
            st.error(f"خطأ أثناء التحميل: {ex}")

# ==========================================
# الصفحة 5: المصروفات والنفقات
# ==========================================
elif page == "💸 المصروفات والنفقات":
    st.m
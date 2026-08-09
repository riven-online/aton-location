import streamlit as st
import pandas as pd
from datetime import datetime

# 1. ضبط إعدادات الصفحة واستخدام العرض الكامل وإخفاء الشريط الجانبي
st.set_page_config(
    page_title="نظام إدارة الاستوديو والكاشير",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. تصميم CSS احترافي ومغذي بصرياً (Dark / Glassmorphism Theme)
st.markdown("""
    <style>
    /* إخفاء القائمة الجانبية تماماً وأزرار التحكم بها */
    [data-testid="stSidebar"] {
        display: none;
    }
    [data-testid="collapsedControl"] {
        display: none;
    }
    
    /* خلفية الصفحة العامة */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #f8fafc;
    }
    
    /* الهيدر الرئيسي */
    .main-header {
        background: linear-gradient(90deg, #1e1b4b 0%, #312e81 100%);
        padding: 24px 32px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .main-title {
        color: #ffffff;
        font-size: 28px;
        font-weight: 800;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    /* بطاقات المعلومات العلوية */
    .info-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 16px 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .info-card:hover {
        transform: translateY(-3px);
        border-color: #6366f1;
    }
    .info-label {
        font-size: 13px;
        color: #94a3b8;
        margin-bottom: 6px;
        font-weight: 600;
    }
    .info-value {
        font-size: 18px;
        color: #f8fafc;
        font-weight: 700;
    }
    
    /* قسم الحالة النشطة (Active Sessions) */
    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #e2e8f0;
        margin: 25px 0 15px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* بطاقات اللوكيشنات والخدمات */
    .status-card {
        background: rgba(30, 41, 59, 0.6);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 5px solid #64748b;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .status-active {
        border-left-color: #10b981;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(30, 41, 59, 0.6) 100%);
    }
    .status-available {
        border-left-color: #3b82f6;
    }
    .status-maintenance {
        border-left-color: #ef4444;
    }
    
    /* شارات الحالة (Badges) */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
    }
    .badge-active { background-color: rgba(16, 185, 129, 0.2); color: #34d399; }
    .badge-available { background-color: rgba(59, 130, 246, 0.2); color: #60a5fa; }
    .badge-maintenance { background-color: rgba(239, 68, 68, 0.2); color: #f87171; }
    
    /* تخصيص الجداول والبيانات */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# البيانات الافتراضية للتجربة (Mock Data)
# ---------------------------------------------------------
if "cashier_name" not in st.session_state:
    st.session_state.cashier_name = "إسلام محمد"

if "session_name" not in st.session_state:
    st.session_state.session_name = "الوردية الصباحية ☀️"

if "shift_start" not in st.session_state:
    st.session_state.shift_start = "09:00 AM"

# ---------------------------------------------------------
# 1. الهيدر الرئيسي وتفاصيل الكاشير والسيشن
# ---------------------------------------------------------
st.markdown(f"""
    <div class="main-header">
        <div class="main-title">
            <span>🎬</span> نظام إدارة الكاشير والاستوديو
        </div>
        <div style="font-size: 14px; color: #cbd5e1; font-weight: 600;">
            📅 {datetime.now().strftime('%Y-%m-%d')}
        </div>
    </div>
""", unsafe_allow_html=True)

# عرض تفاصيل الكاشير والسيشن عبر أعمدة بطاقات بصرية
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="info-card">
            <div class="info-label">👤 كاشير الشيفت الحالي</div>
            <div class="info-value">{st.session_state.cashier_name}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="info-card">
            <div class="info-label">🕒 اسم السيشن / الورديّة</div>
            <div class="info-value">{st.session_state.session_name}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="info-card">
            <div class="info-label">⏰ وقت بدء الشيفت</div>
            <div class="info-value">{st.session_state.shift_start}</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="info-card">
            <div class="info-label">🟢 حالة النظام</div>
            <div class="info-value" style="color: #34d399;">متصل وجاهز</div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------
# 2. متابعة حالة اللوكيشنات والسيشنات الحالية (مع الإيموجيز)
# ---------------------------------------------------------
st.markdown('<div class="section-title">📍 حالة اللوكيشنات والسيشنات الشغالة الأن</div>', unsafe_allow_html=True)

loc_col1, loc_col2, loc_col3 = st.columns(3)

with loc_col1:
    st.markdown("""
        <div class="status-card status-active">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin:0; color:#fff;">📸 لوكيشن (A) - مودرن</h4>
                <span class="badge badge-active">🟢 مشغول الآن</span>
            </div>
            <hr style="border-color: rgba(255,255,255,0.1); margin: 10px 0;">
            <p style="margin: 4px 0; font-size: 14px;"><b>👤 العميل:</b> أسر محمود</p>
            <p style="margin: 4px 0; font-size: 14px;"><b>⏱️ الوقت الانقضى:</b> 45 دقيقة</p>
            <p style="margin: 4px 0; font-size: 14px;"><b>💰 الإجمالي الحسابي:</b> 350 ج.م</p>
        </div>
    """, unsafe_allow_html=True)

with loc_col2:
    st.markdown("""
        <div class="status-card status-available">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin:0; color:#fff;">🎥 لوكيشن (B) - كلاسيك</h4>
                <span class="badge badge-available">🔵 متاح حالياً</span>
            </div>
            <hr style="border-color: rgba(255,255,255,0.1); margin: 10px 0;">
            <p style="margin: 4px 0; font-size: 14px; color: #94a3b8;">جاهز لاستقبال حجز جديد</p>
            <p style="margin: 4px 0; font-size: 14px; color: #94a3b8;"><b>✨ السعر بالمطبوعات:</b> 200 ج.م / ساعة</p>
        </div>
    """, unsafe_allow_html=True)

with loc_col3:
    st.markdown("""
        <div class="status-card status-maintenance">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin:0; color:#fff;">🎨 استوديو الأطفال</h4>
                <span class="badge badge-maintenance">🔴 صيانة / تجهيز</span>
            </div>
            <hr style="border-color: rgba(255,255,255,0.1); margin: 10px 0;">
            <p style="margin: 4px 0; font-size: 14px; color: #94a3b8;">جاري تغيير الديكورات الخلفية</p>
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. جدول العمليات السريعة وإمكانية إضافة حجز/فاتورة
# ---------------------------------------------------------
st.markdown('<div class="section-title">📊 آخر المعاملات المالية في هذه السيشن</div>', unsafe_allow_html=True)

# جدول افتراضي للعمليات
data = {
    "رقم الفاتورة 📑": ["#1001", "#1002", "#1003"],
    "اسم العميل 👤": ["أحمد علي", "سارة إبراهيم", "شركة النور"],
    "الخدمة / اللوكيشن 🎬": ["سيشن تصوير خطوبة 💍", "طباعة ألبوم صور 🖼️", "إيجار لوكيشن A 🎥"],
    "طريقة الدفع 💳": ["كاش 💵", "فودافون كاش 📱", "فيزا 💳"],
    "المبلغ الإجمالي 💵": ["1,200 ج.م", "450 ج.م", "800 ج.م"],
    "الحالة 📌": ["مكتمل ✅", "مكتمل ✅", "قيد التنفيذ ⏳"]
}

df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

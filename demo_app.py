
import streamlit as st
import pandas as pd

# =====================================================
# SAYFA AYARLARI
# =====================================================

st.set_page_config(
    page_title="StudyTrack | Öğrenci Takip Sistemi",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# KOYU MOR VE SOFT LİLA TASARIM
# =====================================================

st.markdown("""
<style>
/* Ana arka plan */
.stApp {
    background: linear-gradient(135deg, #171323 0%, #211832 55%, #2b2040 100%);
    color: #f1eafa;
}

/* Ana içerik */
[data-testid="stMain"] {
    background: transparent;
}

/* Sol menü */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #211832 0%, #302044 100%);
    border-right: 1px solid #49345f;
}

[data-testid="stSidebar"] * {
    color: #eee5ff;
}

/* Genel yazılar */
.stApp p,
.stApp label,
.stApp li {
    color: #eee7f7;
}

/* Başlıklar */
h1, h2, h3 {
    color: #d9c2ff !important;
}

h1 {
    font-weight: 750 !important;
}

/* Metrik kartları */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #302441, #38294b);
    border: 1px solid #59416f;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.15);
}

[data-testid="stMetricLabel"] {
    color: #c8b4e5 !important;
}

[data-testid="stMetricValue"] {
    color: #f3eaff !important;
}

[data-testid="stMetricDelta"] {
    color: #d4c1f5 !important;
}

/* Butonlar */
.stButton > button {
    background: linear-gradient(135deg, #9168c8, #7650ad);
    color: #ffffff !important;
    border: 1px solid #a98bd7;
    border-radius: 11px;
    padding: 8px 18px;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #a27ed6;
    border-color: #d4baff;
    color: #ffffff !important;
}

/* Sayısal girişler */
.stNumberInput input,
.stTextInput input,
.stDateInput input,
.stTextArea textarea {
    background-color: #302441 !important;
    color: #f5edff !important;
    border: 1px solid #59416f !important;
    border-radius: 9px !important;
}

/* Giriş kutularındaki metin */
.stNumberInput input,
.stTextInput input {
    -webkit-text-fill-color: #f5edff !important;
}

/* Seçim kutuları */
.stSelectbox [data-baseweb="select"],
.stMultiSelect [data-baseweb="select"] {
    background-color: #302441 !important;
    border-radius: 9px !important;
}

.stSelectbox [data-baseweb="select"] *,
.stMultiSelect [data-baseweb="select"] * {
    color: #f5edff !important;
}

/* Kaydırma çubuğu */
.stSlider [data-baseweb="slider"] {
    color: #b995ef;
}

/* Bilgi kutusu */
.demo-note {
    background: linear-gradient(120deg, #352547, #44305d);
    padding: 16px;
    border: 1px solid #654b83;
    border-radius: 13px;
    color: #f0e5ff;
    margin-bottom: 18px;
}

/* Tablolar */
[data-testid="stDataFrame"] {
    border: 1px solid #59416f;
    border-radius: 12px;
    overflow: hidden;
}

/* Ayraçlar */
hr {
    border-color: #49345f !important;
}

/* Açılır alanlar */
[data-testid="stExpander"] {
    background: #292039;
    border: 1px solid #49345f;
    border-radius: 12px;
}

/* Alt açıklamalar */
[data-testid="stCaptionContainer"] {
    color: #bba8d4;
}

/* Bildirim kutuları */
[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Grafik arka planı */
[data-testid="stVegaLiteChart"],
[data-testid="stArrowVegaLiteChart"] {
    background: #251c35;
    border: 1px solid #49345f;
    border-radius: 12px;
    padding: 10px;
}

/* Sayfa altı */
footer {
    visibility: hidden;
}

/* Üst araç çubuğu */
[data-testid="stHeader"] {
    background: transparent;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# ÖRNEK VERİLER
# Bu demo, kişisel veritabanına bağlanmaz.
# =====================================================

courses = pd.DataFrame([
    {
        "Ders": "Python Programlama",
        "Vize": 78,
        "Final": 85,
        "Kredi": 4
    },
    {
        "Ders": "Matematik",
        "Vize": 62,
        "Final": 70,
        "Kredi": 5
    },
    {
        "Ders": "Fizik",
        "Vize": 55,
        "Final": 68,
        "Kredi": 4
    },
    {
        "Ders": "Veri Tabanı",
        "Vize": 88,
        "Final": 92,
        "Kredi": 3
    },
])

courses["Ortalama"] = (
    courses["Vize"] * 0.40
    + courses["Final"] * 0.60
).round(1)

tasks = pd.DataFrame([
    {
        "Görev": "Python proje ödevi",
        "Ders": "Python Programlama",
        "Son tarih": "2026-10-12",
        "Durum": "Gecikti"
    },
    {
        "Görev": "İntegral soru çözümleri",
        "Ders": "Matematik",
        "Son tarih": "2026-10-18",
        "Durum": "Devam ediyor"
    },
    {
        "Görev": "Veri tabanı raporu",
        "Ders": "Veri Tabanı",
        "Son tarih": "2026-10-20",
        "Durum": "Tamamlandı"
    },
    {
        "Görev": "Fizik laboratuvar hazırlığı",
        "Ders": "Fizik",
        "Son tarih": "2026-10-16",
        "Durum": "Devam ediyor"
    },
])

# =====================================================
# SOL MENÜ
# =====================================================

st.sidebar.title("📚 StudyTrack")
st.sidebar.caption("Öğrenci görev ve not takip sistemi")
st.sidebar.divider()

page = st.sidebar.radio(
    "MENÜ",
    [
        "Ana Sayfa",
        "Dersler ve Notlar",
        "Görevler",
        "Hedef Not Hesaplayıcı",
        "İstatistikler"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("### ✨ Demo Sürümü")
st.sidebar.caption(
    "Bu sürümde yalnızca örnek veriler kullanılır."
)
st.sidebar.caption("🎨 Soft lila · Koyu mor tasarım")

# =====================================================
# SAYFA ÜST BİLGİSİ
# =====================================================

st.title("StudyTrack")

st.markdown("""
<div class="demo-note">
    👋 <b>Hoş geldin!</b> Öğrenci hayatını daha düzenli
    yönetmek için hazırlanan StudyTrack demo sürümündesin.
    Buradaki bütün ders, not ve görev bilgileri örnektir.
</div>
""", unsafe_allow_html=True)

# =====================================================
# ANA SAYFA
# =====================================================

if page == "Ana Sayfa":

    st.header("📊 Genel Bakış")
    st.write("Akademik durumuna ve görevlerine tek ekrandan göz at.")

    average = courses["Ortalama"].mean()
    completed = int((tasks["Durum"] == "Tamamlandı").sum())
    overdue = int((tasks["Durum"] == "Gecikti").sum())
    ongoing = int((tasks["Durum"] == "Devam ediyor").sum())

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📚 Toplam Ders", len(courses))
    col2.metric("📈 Ders Ortalaması", f"{average:.1f}/100")
    col3.metric("✅ Tamamlanan Görev", completed)
    col4.metric("⚠️ Geciken Görev", overdue)

    st.divider()

    left, right = st.columns([1.4, 1])

    with left:
        st.subheader("📖 Ders Ortalamaları")
        st.bar_chart(
            courses.set_index("Ders")["Ortalama"],
            color="#a78bfa"
        )

    with right:
        st.subheader("📝 Görev Durumu")
        st.write(f"✅ Tamamlandı: **{completed}**")
        st.write(f"🟣 Devam ediyor: **{ongoing}**")
        st.write(f"🔴 Gecikti: **{overdue}**")

        total_tasks = len(tasks)
        progress = completed / total_tasks if total_tasks else 0

        st.progress(progress)
        st.caption(f"Görev tamamlama oranı: %{progress * 100:.0f}")

    st.divider()
    st.subheader("⏰ Geciken Görevler")

    late_tasks = tasks[tasks["Durum"] == "Gecikti"]

    if late_tasks.empty:
        st.success("Geciken görev bulunmuyor.")
    else:
        for _, task in late_tasks.iterrows():
            st.error(
                f"⚠️ **{task['Görev']}** — {task['Ders']} "
                f"| Son tarih: {task['Son tarih']}"
            )

# =====================================================
# DERSLER VE NOTLAR
# =====================================================

elif page == "Dersler ve Notlar":

    st.header("📚 Dersler ve Notlar")
    st.write("Örnek derslerinin sınav notlarını ve ortalamalarını incele.")

    st.dataframe(
        courses,
        use_container_width=True,
        hide_index=True
    )

    st.divider()
    st.subheader("📊 Ders Ortalamaları")

    st.bar_chart(
        courses.set_index("Ders")["Ortalama"],
        color="#a78bfa"
    )

    st.info(
        "Hesaplama örneği: Vize %40 + Final %60. "
        "Gerçek derslerde değerlendirme ağırlıkları ve geçme koşulları değişebilir."
    )

# =====================================================
# GÖREVLER
# =====================================================

elif page == "Görevler":

    st.header("✅ Görev Takibi")
    st.write("Örnek görevlerini ve son teslim tarihlerini görüntüle.")

    for _, task in tasks.iterrows():

        if task["Durum"] == "Gecikti":
            st.error(
                f"🔴 **{task['Görev']}**\n\n"
                f"Ders: {task['Ders']} · "
                f"Son tarih: {task['Son tarih']} · "
                f"Durum: {task['Durum']}"
            )

        elif task["Durum"] == "Tamamlandı":
            st.success(
                f"✅ **{task['Görev']}**\n\n"
                f"Ders: {task['Ders']} · "
                f"Son tarih: {task['Son tarih']} · "
                f"Durum: {task['Durum']}"
            )

        else:
            st.info(
                f"🟣 **{task['Görev']}**\n\n"
                f"Ders: {task['Ders']} · "
                f"Son tarih: {task['Son tarih']} · "
                f"Durum: {task['Durum']}"
            )

    st.divider()
    st.subheader("📌 Görev Durumu Dağılımı")

    st.bar_chart(tasks["Durum"].value_counts(), color="#a78bfa")

# =====================================================
# HEDEF NOT HESAPLAYICI
# =====================================================

elif page == "Hedef Not Hesaplayıcı":

    st.header("🎯 Finalde Kaç Almalıyım?")
    st.write(
        "Vize notunu ve hedef dönem sonu notunu girerek "
        "finalde alman gereken notu hesapla."
    )

    col1, col2 = st.columns(2)

    with col1:
        midterm = st.number_input(
            "Vize notun",
            min_value=0.0,
            max_value=100.0,
            value=60.0,
            step=1.0
        )

        target = st.number_input(
            "Hedef dönem sonu notu",
            min_value=0.0,
            max_value=100.0,
            value=70.0,
            step=1.0
        )

    with col2:
        midterm_weight = st.slider(
            "Vize ağırlığı (%)",
            min_value=10,
            max_value=90,
            value=40
        )

        final_weight = 100 - midterm_weight

        st.metric("Final ağırlığı", f"%{final_weight}")

    st.divider()

    needed = (
        target - midterm * midterm_weight / 100
    ) / (final_weight / 100)

    if needed <= 0:
        st.success(
            "Girilen hedef için ağırlıklı ortalama hesabında "
            "finalden 0 almak bile yeterli olabilir."
        )

    elif needed <= 100:
        st.metric("🎯 Finalde Gereken Not", f"{needed:.1f}/100")

        if needed > 90:
            st.warning(
                "Bu hedefe ulaşmak için oldukça yüksek bir final notu gerekiyor."
            )
        elif needed <= 50:
            st.success(
                "Bu hedef için gereken final notu 50 veya daha düşük."
            )
        else:
            st.info(
                "Hedefine ulaşmak için finalde bu nota ulaşman gerekiyor."
            )

    else:
        st.error(
            "Bu hedefe mevcut vize notu ve ağırlıklarla ulaşmak mümkün değil."
        )

    st.caption(
        "Bu araç ağırlıklı ortalamayı hesaplar. Dersin final barajı, "
        "geçme notu ve diğer kuralları ayrıca dikkate alınmalıdır."
    )

# =====================================================
# İSTATİSTİKLER
# =====================================================

elif page == "İstatistikler":

    st.header("📈 Akademik İstatistikler")
    st.write("Örnek akademik performans verilerini incele.")

    best_course = courses.loc[courses["Ortalama"].idxmax()]
    lowest_course = courses.loc[courses["Ortalama"].idxmin()]

    col1, col2 = st.columns(2)

    col1.metric(
        "🏆 En yüksek ortalama",
        f"{best_course['Ortalama']:.1f}",
        help=best_course["Ders"]
    )

    col2.metric(
        "📌 En düşük ortalama",
        f"{lowest_course['Ortalama']:.1f}",
        help=lowest_course["Ders"]
    )

    st.divider()
    st.subheader("Derslere Göre Başarı")

    st.bar_chart(
        courses.set_index("Ders")["Ortalama"],
        color="#a78bfa"
    )

    st.subheader("Görev Dağılımı")
    st.bar_chart(
        tasks["Durum"].value_counts(),
        color="#a78bfa"
    )

# =====================================================
# ALT BİLGİ
# =====================================================

st.divider()

st.caption(
    "StudyTrack · Öğrenci Görev ve Not Takip Sistemi | "
    "Portföy demosu · Tüm veriler örnektir."
)

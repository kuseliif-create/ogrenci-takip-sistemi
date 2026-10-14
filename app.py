import streamlit as st
from datetime import date
from math import ceil

from database import (
    initialize_database,
    add_course,
    get_courses,
    delete_course,
    add_task,
    get_tasks,
    update_task_status,
    delete_task,
    add_grade,
    get_grades,
    delete_grade,
    get_course_averages,
    get_task_counts,
    save_attendance,
    get_attendance,
)

# ==========================================
# SAYFA AYARLARI
# ==========================================

st.set_page_config(
    page_title="StudyTrack",
    page_icon="📚",
    layout="wide"
)

# ==========================================
# KOYU SOFT PASTEL TASARIM
# ==========================================

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(
            ellipse at 0% 0%,
            rgba(160, 140, 230, 0.12),
            transparent 42%
        ),
        radial-gradient(
            ellipse at 100% 100%,
            rgba(125, 205, 180, 0.08),
            transparent 38%
        ),
        #171725;
    color: #F1EEFF;
}

[data-testid="stSidebar"] {
    background: #1D1C2D;
    border-right: 1px solid #38354D;
}

h1, h2, h3 {
    color: #E9E2FF !important;
}

p, label, .stMarkdown {
    color: #D1CDE3;
}

div[data-testid="stMetric"] {
    background: #242338;
    border: 1px solid #39364F;
    border-radius: 16px;
    padding: 18px;
}

div[data-testid="stMetricValue"] {
    color: #BDAEFF;
}

div[data-testid="stForm"],
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #211F32;
    border-color: #39364F;
    border-radius: 16px;
}

.stButton > button,
.stFormSubmitButton > button {
    background: #B9A9F7;
    color: #201B32;
    border: none;
    border-radius: 10px;
    font-weight: 600;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #D0C5FF;
    color: #171725;
}

input, textarea {
    background-color: #29273D !important;
    color: #F1EEFF !important;
}

div[data-baseweb="select"] > div {
    background-color: #29273D;
    border-color: #48425F;
    color: #F1EEFF;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

hr {
    border-color: #39364F;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# VERİTABANI
# ==========================================

initialize_database()

st.title("📚 StudyTrack")
st.caption(
    "Hoş geldin, öğrenci! Derslerini, görevlerini "
    "ve notlarını tek yerden yönet."
)

# ==========================================
# MENÜ
# ==========================================

page = st.sidebar.radio(
    "Menü",
    [
        "Ana Sayfa",
        "Dersler",
        "Görevler",
        "Notlar",
        "Hedef Not",
        "Devamsızlık",
        "İstatistikler",
    ]
)

courses = get_courses()


# ==========================================
# 1. ANA SAYFA
# ==========================================

if page == "Ana Sayfa":

    st.header("✨ Genel Bakış")

    total, completed = get_task_counts()
    total = total or 0
    completed = completed or 0
    pending = total - completed

    averages = get_course_averages()

    valid_averages = [
        row[2]
        for row in averages
        if row[2] is not None
    ]

    overall_average = (
        sum(valid_averages) / len(valid_averages)
        if valid_averages
        else None
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("📌 Toplam görev", total)
    col2.metric("⏳ Bekleyen görev", pending)

    col3.metric(
        "📚 Ders not ortalaması",
        f"{overall_average:.2f}"
        if overall_average is not None
        else "Henüz yok"
    )

    # Geciken görevler

    today = date.today().isoformat()

    overdue_tasks = [
        task
        for task in get_tasks()
        if task[3] < today and task[4] != "Tamamlandı"
    ]

    if overdue_tasks:
        st.subheader("🚨 Geciken Görevler")

        st.error(
            f"{len(overdue_tasks)} görevin gecikti! "
            "Teslim tarihlerini kontrol et."
        )

        for task in overdue_tasks:
            st.markdown(
                f"""
                <div style="
                    background: rgba(255, 100, 130, 0.10);
                    border: 1px solid #A95870;
                    border-radius: 12px;
                    padding: 12px;
                    margin-bottom: 8px;
                    color: #FFB2C0;
                ">
                    <b>🔴 {task[2]}</b><br>
                    Ders: {task[1]}<br>
                    Son tarih: {task[3]}
                </div>
                """,
                unsafe_allow_html=True
            )

    # Yaklaşan görevler

    st.subheader("🗓️ Yaklaşan Görevler")

    upcoming = [
        task
        for task in get_tasks()
        if task[3] >= today and task[4] != "Tamamlandı"
    ]

    if upcoming:
        for task in upcoming[:5]:
            st.write(
                f"📌 **{task[2]}** — {task[1]} "
                f"| Son tarih: {task[3]}"
            )
    else:
        st.info("Yaklaşan bekleyen bir görevin yok.")


# ==========================================
# 2. DERSLER
# ==========================================

elif page == "Dersler":

    st.header("📘 Ders Yönetimi")

    with st.form("course_form"):

        name = st.text_input("Ders adı")
        code = st.text_input("Ders kodu")

        credits = st.number_input(
            "Ders kredisi",
            min_value=0,
            max_value=30,
            value=3
        )

        submitted = st.form_submit_button("Ders Ekle")

        if submitted:
            if not name.strip() or not code.strip():
                st.error("Ders adı ve kodu boş bırakılamaz.")
            else:
                add_course(
                    name.strip(),
                    code.strip(),
                    int(credits)
                )

                st.success("Ders başarıyla eklendi.")
                st.rerun()

    st.divider()
    st.subheader("📚 Derslerim")

    courses = get_courses()

    if courses:

        st.dataframe(
            [
                {
                    "Ders numarası": c[0],
                    "Ders adı": c[1],
                    "Ders kodu": c[2],
                    "Kredi": c[3],
                }
                for c in courses
            ],
            use_container_width=True,
            hide_index=True
        )

        course_map = {
            f"{c[1]} ({c[2]})": c[0]
            for c in courses
        }

        selected_course = st.selectbox(
            "Silmek istediğin ders",
            list(course_map.keys()),
            key="delete_course_select"
        )

        if st.button("🗑️ Seçilen Dersi Sil"):

            delete_course(course_map[selected_course])

            st.success("Ders ve ona bağlı kayıtlar silindi.")
            st.rerun()

    else:
        st.info("Henüz ders eklemedin.")


# ==========================================
# 3. GÖREVLER
# ==========================================

elif page == "Görevler":

    st.header("🗓️ Görev ve Ödev Takibi")

    courses = get_courses()

    if not courses:
        st.warning(
            "Önce Dersler bölümünden bir ders eklemelisin."
        )

    else:

        course_map = {
            f"{c[1]} ({c[2]})": c[0]
            for c in courses
        }

        with st.form("task_form"):

            selected = st.selectbox(
                "İlgili ders",
                list(course_map.keys())
            )

            title = st.text_input("Görev başlığı")

            due_date = st.date_input(
                "Son teslim tarihi",
                value=date.today()
            )

            submitted = st.form_submit_button("Görev Ekle")

            if submitted:
                if not title.strip():
                    st.error("Görev başlığı boş olamaz.")
                else:
                    add_task(
                        course_map[selected],
                        title.strip(),
                        due_date.isoformat()
                    )

                    st.success("Görev eklendi.")
                    st.rerun()

    st.divider()
    st.subheader("📌 Görevlerim")

    tasks = get_tasks()

    if tasks:

        for task in tasks:

            task_id, course_name, title, due_date, status = task

            with st.container(border=True):

                st.write(f"**{title}**")

                st.caption(
                    f"Ders: {course_name} | "
                    f"Son tarih: {due_date}"
                )

                today = date.today().isoformat()

                if due_date < today and status != "Tamamlandı":
                    st.error("🔴 Bu görevin teslim tarihi geçti.")

                st.write(f"Durum: {status}")

                col1, col2 = st.columns(2)

                new_status = (
                    "Tamamlandı"
                    if status == "Bekliyor"
                    else "Bekliyor"
                )

                if col1.button(
                    f"Durumu değiştir: {new_status}",
                    key=f"status_{task_id}"
                ):
                    update_task_status(task_id, new_status)
                    st.rerun()

                if col2.button(
                    "Görevi sil",
                    key=f"delete_task_{task_id}"
                ):
                    delete_task(task_id)
                    st.rerun()

    else:
        st.info("Henüz görev eklemedin.")


# ==========================================
# 4. NOTLAR
# ==========================================

elif page == "Notlar":

    st.header("📝 Sınav Notları")

    courses = get_courses()

    if not courses:
        st.warning(
            "Önce Dersler bölümünden bir ders eklemelisin."
        )

    else:

        course_map = {
            f"{c[1]} ({c[2]})": c[0]
            for c in courses
        }

        with st.form("grade_form"):

            selected = st.selectbox(
                "Ders",
                list(course_map.keys())
            )

            exam_type = st.selectbox(
                "Sınav türü",
                ["Vize", "Final", "Ödev", "Quiz", "Proje"]
            )

            score = st.number_input(
                "Aldığın not",
                min_value=0.0,
                max_value=100.0,
                value=50.0,
                step=1.0
            )

            weight = st.number_input(
                "Başarı notundaki ağırlık (%)",
                min_value=0.0,
                max_value=100.0,
                value=40.0,
                step=5.0
            )

            submitted = st.form_submit_button("Not Ekle")

            if submitted:
                if weight <= 0:
                    st.error("Ağırlık sıfırdan büyük olmalı.")
                else:
                    add_grade(
                        course_map[selected],
                        exam_type,
                        score,
                        weight
                    )

                    st.success("Not eklendi.")
                    st.rerun()

    st.divider()
    st.subheader("Kaydedilen Notlar")

    grades = get_grades()

    if grades:

        st.dataframe(
            [
                {
                    "Kayıt": g[0],
                    "Ders": g[1],
                    "Sınav": g[2],
                    "Not": g[3],
                    "Ağırlık (%)": g[4],
                }
                for g in grades
            ],
            use_container_width=True,
            hide_index=True
        )

        grade_map = {
            f"#{g[0]} | {g[1]} | {g[2]} | {g[3]}": g[0]
            for g in grades
        }

        selected_grade = st.selectbox(
            "Silinecek not",
            list(grade_map.keys())
        )

        if st.button("🗑️ Seçilen Notu Sil"):
            delete_grade(grade_map[selected_grade])
            st.rerun()

    else:
        st.info("Henüz not girmedin.")

    st.divider()
    st.subheader("📊 Ders Bazında Ortalamalar")

    averages = get_course_averages()

    for course_id, name, average in averages:

        if average is None:
            st.write(f"**{name}:** Henüz not girilmedi.")
        else:
            st.write(f"**{name}:** {average:.2f} / 100")


# ==========================================
# 5. HEDEF NOT HESAPLAYICI
# ==========================================

elif page == "Hedef Not":

    st.header("🎯 Hedef Not / Geçme Notu Hesaplayıcı")

    st.caption(
        "Vize notuna göre finalde kaç alman gerektiğini hesapla."
    )

    col1, col2 = st.columns(2)

    with col1:

        midterm = st.number_input(
            "Vize notun",
            min_value=0.0,
            max_value=100.0,
            value=50.0,
            step=1.0
        )

        midterm_weight = st.number_input(
            "Vize ağırlığı (%)",
            min_value=0.0,
            max_value=100.0,
            value=40.0,
            step=5.0
        )

    with col2:

        final_weight = st.number_input(
            "Final ağırlığı (%)",
            min_value=0.0,
            max_value=100.0,
            value=60.0,
            step=5.0
        )

        passing_grade = st.number_input(
            "Hedef dönem sonu notu",
            min_value=0.0,
            max_value=100.0,
            value=60.0,
            step=1.0
        )

    st.caption(
        "Vize ve final ağırlıkları toplamı %100 olmalıdır."
    )

    if st.button("Gerekli Final Notunu Hesapla"):

        if abs(midterm_weight + final_weight - 100) > 0.001:

            st.error(
                "Vize ve final ağırlıkları toplamı %100 olmalı."
            )

        elif final_weight <= 0:

            st.error("Final ağırlığı sıfırdan büyük olmalı.")

        else:

            required_final = (
                passing_grade
                - midterm * midterm_weight / 100
            ) / (final_weight / 100)

            if required_final > 100:

                st.error(
                    "Bu hedefe yalnızca final notuyla "
                    "ulaşmak mümkün değil."
                )

            elif required_final <= 0:

                st.success(
                    "Girdiğin vize notuyla hedef ortalamaya ulaşmışsın."
                )

                st.metric("Gerekli minimum final", "0")

            else:

                st.metric(
                    "Alman gereken minimum final",
                    f"{required_final:.2f} / 100"
                )

                st.info(
                    f"Tam sayı not kullanılıyorsa en az "
                    f"{ceil(required_final)} almalısın."
                )


# ==========================================
# 6. DEVAMSIZLIK TAKİBİ
# ==========================================

elif page == "Devamsızlık":

    st.header("📅 Devamsızlık Takibi")

    st.caption(
        "Ders bazında devamsızlık sınırını ve kalan hakkını hesapla."
    )

    courses = get_courses()

    if not courses:

        st.warning(
            "Önce Dersler bölümünden bir ders eklemelisin."
        )

    else:

        course_map = {
            f"{c[1]} ({c[2]})": c[0]
            for c in courses
        }

        selected = st.selectbox(
            "Ders seç",
            list(course_map.keys()),
            key="attendance_course"
        )

        course_id = course_map[selected]

        saved = get_attendance(course_id)

        with st.form("attendance_form"):

            total_hours = st.number_input(
                "Dönem boyunca toplam ders saati",
                min_value=1.0,
                max_value=500.0,
                value=float(saved[1]) if saved else 42.0,
                step=1.0
            )

            limit_percent = st.number_input(
                "Devamsızlık sınırı (%)",
                min_value=1.0,
                max_value=100.0,
                value=float(saved[2]) if saved else 30.0,
                step=1.0
            )

            used_hours = st.number_input(
                "Şu ana kadar devamsız olduğun saat",
                min_value=0.0,
                max_value=500.0,
                value=float(saved[3]) if saved else 0.0,
                step=1.0
            )

            submitted = st.form_submit_button(
                "Devamsızlık Bilgilerini Kaydet"
            )

            if submitted:

                if used_hours > total_hours:
                    st.error(
                        "Devamsızlık saati toplam ders saatinden "
                        "fazla olamaz."
                    )

                else:
                    save_attendance(
                        course_id,
                        total_hours,
                        limit_percent,
                        used_hours
                    )

                    st.success(
                        "Devamsızlık bilgileri kaydedildi."
                    )

                    st.rerun()

        # Hesaplamalar

        allowed_hours = total_hours * limit_percent / 100

        remaining_hours = allowed_hours - used_hours

        st.divider()
        st.subheader("📊 Devamsızlık Durumun")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Toplam devamsızlık hakkı",
            f"{allowed_hours:.1f} saat"
        )

        col2.metric(
            "Kullanılan hak",
            f"{used_hours:.1f} saat"
        )

        col3.metric(
            "Kalan hak",
            f"{max(0, remaining_hours):.1f} saat"
        )

        if remaining_hours < 0:

            st.error(
                "Devamsızlık sınırını aşmış görünüyorsun!"
            )

        elif remaining_hours <= 2:

            st.warning(
                "Dikkat! Devamsızlık hakkın bitmek üzere."
            )

        else:

            st.success(
                "Devamsızlık sınırının içindesin."
            )

        st.caption(
            "Hesaplama girdiğin değerlere dayanır. "
            "Dersin devam zorunluluğunu ve üniversitenin "
            "yönetmeliğini ayrıca kontrol et."
        )


# ==========================================
# 7. İSTATİSTİKLER
# ==========================================

elif page == "İstatistikler":

    st.header("📊 İstatistikler")

    total, completed = get_task_counts()

    total = total or 0
    completed = completed or 0

    pending = total - completed

    col1, col2, col3 = st.columns(3)

    col1.metric("Toplam görev", total)
    col2.metric("Tamamlanan görev", completed)
    col3.metric("Bekleyen görev", pending)

    st.divider()
    st.subheader("✅ Görev Tamamlama Durumu")

    if total > 0:

        st.progress(completed / total)

        st.write(
            f"{completed} / {total} görev tamamlandı."
        )

        completion_rate = completed / total * 100

        st.metric(
            "Tamamlanma oranı",
            f"%{completion_rate:.1f}"
        )

    else:

        st.info(
            "İstatistikleri görmek için önce görev ekle."
        )

    st.divider()
    st.subheader("📚 Ders Ortalamaları")

    averages = get_course_averages()

    if averages:

        for course_id, name, average in averages:

            if average is not None:

                st.write(f"**{name}:** {average:.2f} / 100")

            else:

                st.write(f"**{name}:** Henüz not girilmedi.")

    else:

        st.info(
            "Ders ortalamalarını görmek için önce ders ekle."
        )

    st.divider()
    st.subheader("🚨 Geciken Görev Özeti")

    today = date.today().isoformat()

    overdue_tasks = [
        task
        for task in get_tasks()
        if task[3] < today and task[4] != "Tamamlandı"
    ]

    if overdue_tasks:

        st.error(
            f"Toplam {len(overdue_tasks)} gecikmiş görevin var."
        )

        for task in overdue_tasks:

            st.write(
                f"🔴 **{task[2]}** — {task[1]} "
                f"| Son tarih: {task[3]}"
            )

    else:

        st.success("Gecikmiş görevin bulunmuyor.")
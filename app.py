import streamlit as st
import pandas as pd
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# --- НАСТРОЙКА СТРАНИЦЫ И СТИЛЕЙ ---
st.set_page_config(page_title="Ариада — Конструктор Камер", layout="centered", page_icon="❄️")

st.markdown("""
    <style>
    .main { background-color: #f0f4f8; padding-top: 20px; }
    
    .option-card {
        padding: 20px; border-radius: 15px; border: 1px solid #e0e6ed;
        background-color: white; margin-bottom: 25px; text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        transition: transform 0.2s;
        height: 380px; 
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .option-card:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.1); }
    
    .price-tag { font-size: 26px; color: #d32f2f; font-weight: bold; margin-top: 10px; }
    .dim-tag { font-size: 15px; font-weight: bold; color: #0055a5; background-color: #e3f2fd; padding: 5px 10px; border-radius: 20px; display: inline-block; margin-bottom: 10px; }
    
    button[kind="primary"] { 
        background-color: #ff5722 !important; color: white !important; 
        font-weight: bold !important; height: 55px !important; width: 100% !important;
        border-radius: 10px !important; font-size: 18px !important; border: none !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    button[kind="primary"]:hover { background-color: #f4511e !important; box-shadow: 0 6px 8px rgba(0,0,0,0.15) !important; }

    button[kind="secondary"] { height: 45px; border-radius: 8px; font-weight: bold;}

    .contact-block {
        text-align: center; margin-top: 30px; padding: 30px; 
        background-color: white; border-radius: 15px; border: 1px solid #e0e6ed;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- ЗАГРУЗКА ДАННЫХ ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('base.csv')
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

df = load_data()
if df is None:
    st.error("Критическая ошибка: Файл базы данных base.csv не найден. Пожалуйста, убедитесь, что он находится в той же папке, что и скрипт.")
    st.stop()

# --- УПРАВЛЕНИЕ СОСТОЯНИЕМ КВИЗА ---
TOTAL_STEPS = 4

if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.answers = {}
    st.session_state.submitted = False

def next_step(): st.session_state.step += 1
def prev_step(): st.session_state.step -= 1
def restart(): 
    st.session_state.step = 1
    st.session_state.answers = {}
    st.session_state.submitted = False

def render_header(step_num, title):
    st.image("https://ariada.ru/templates/ariada/images/logo.png", width=180)
    st.write("")
    progress_val = int((step_num - 1) / TOTAL_STEPS * 100)
    st.progress(progress_val)
    st.caption(f"Шаг {step_num} из {TOTAL_STEPS}")
    st.title(title)
    st.write("---")

# --- ШАГИ КВИЗА ---

if st.session_state.step == 1:
    render_header(1, "Для чего вам нужна камера?")
    
    st.markdown('<img src="https://frios.ua/uploads/2025/05/hranenye1-1.webp" style="max-height: 250px; max-width: 100%; display: block; margin: 0 auto 10px auto; border-radius: 12px;">', unsafe_allow_html=True)
    st.caption("Мы подберем оптимальный температурный режим под ваш продукт")
    st.write("")
    
    products = ["Мясные продукты", "Рыбные продукты", "Молочная продукция", "Тесто, выпечка", "Фрукты, овощи", "Цветы", "Алкогольная продукция", "Полуфабрикаты", "Медикаменты", "Другое"]
    default_prod = st.session_state.answers.get('product', products[0])
    st.session_state.answers['product'] = st.radio("Выберите тип продукции:", products, index=products.index(default_prod))
    
    st.write("")
    st.button("Далее →", on_click=next_step, type="secondary", use_container_width=True)

elif st.session_state.step == 2:
    render_header(2, "Укажите внешние размеры")
    
    st.markdown('<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQIkbltcOAvzq9w6H8f3sJ1nWmA931BA4DbdQ&s" style="max-height: 250px; max-width: 100%; display: block; margin: 0 auto 10px auto; border-radius: 12px;">', unsafe_allow_html=True)
    st.caption("Укажите точные габариты помещения в метрах")
    st.write("")
    
    col_inputs = st.columns(3)
    with col_inputs[0]:
        st.session_state.answers['h'] = st.number_input("Высота (м)", value=st.session_state.answers.get('h', 2.20), step=0.10, format="%.2f")
    with col_inputs[1]:
        st.session_state.answers['l'] = st.number_input("Длина (м)", value=st.session_state.answers.get('l', 2.00), step=0.10, format="%.2f")
    with col_inputs[2]:
        st.session_state.answers['w'] = st.number_input("Ширина (м)", value=st.session_state.answers.get('w', 2.00), step=0.10, format="%.2f")
        
    st.write("")
    c1, c2 = st.columns(2)
    with c1: st.button("← Назад", on_click=prev_step, use_container_width=True)
    with c2: st.button("Далее →", on_click=next_step, type="secondary", use_container_width=True)

elif st.session_state.step == 3:
    render_header(3, "Технические предпочтения")
    
    st.markdown('<img src="https://s10.iimage.su/s/24/gG7hXWUxHfd5hhz7uLfty8MoX0DAl7VKAwB4r70OP.png" style="max-height: 250px; max-width: 100%; display: block; margin: 0 auto 10px auto; border-radius: 12px;">', unsafe_allow_html=True)
    st.caption("Энергоэффективные панели собственного производства «Ариада»")
    st.write("")
    
    available_thicks = sorted(df['Thick'].unique().tolist())
    st.session_state.answers['thick'] = st.selectbox("Толщина стенки панелей (мм):", available_thicks, help="Для среднетемпературных обычно 80мм, для низкотемпературных - 100мм")
    
    st.write("")
    st.session_state.answers['floor'] = st.radio("Нужны ли половые панели?", ["Да (Стандарт)", "Нет (Монтаж на существующий пол)"])
    
    st.write("")
    c1, c2 = st.columns(2)
    with c1: st.button("← Назад", on_click=prev_step, use_container_width=True)
    with c2: st.button("Рассчитать варианты →", on_click=next_step, type="secondary", use_container_width=True)

elif st.session_state.step == 4:
    
    if st.session_state.submitted:
        st.image("https://ariada.ru/upload/CLite/882/v1cb1vgchrjblnq5fm40820lx2mnzdcm.png", width=150)
        st.write("")
        st.success("🎉 ЗАПРОС УСПЕШНО ОТПРАВЛЕН!")
        st.balloons()
        
        st.markdown(f"""
            <div style="background-color: white; padding: 30px; border-radius: 15px; border: 1px solid #e0e6ed; box-shadow: 0 5px 15px rgba(0,0,0,0.05); margin-bottom: 20px;">
                <h2 style="color: #0055a5; margin-top: 0;">Спасибо, {st.session_state.answers.get('temp_name', 'уважаемый клиент')}!</h2>
                <p style="font-size: 18px; line-height: 1.6; color: #333;">Ваши данные получены. Наш ведущий инженер уже приступил к подготовке индивидуального технико-коммерческого предложения.</p>
                <p style="font-size: 16px; color: #555;">Мы закрепили за вами расчетную скидку завода. Официальный ответ будет направлен на вашу почту в течение <b>1 рабочего дня</b>.</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.subheader("Оставайтесь на связи с заводом")
        c1, c2, c3 = st.columns(3)
        with c1: st.link_button("🌐 Наш сайт", "https://ariada.ru/", use_container_width=True)
        with c2: st.link_button("✈️ Telegram-канал", "https://t.me/ariadaholod", use_container_width=True)
        with c3: st.link_button("📞 Звонок: 8 804 700 44 95", "tel:88047004495", use_container_width=True)
        
        st.write("")
        st.caption("* Обратите внимание: мы работаем через дилерскую сеть, прямая доставка заводом не осуществляется.")
        st.write("---")
        st.button("↺ Рассчитать новую камеру", on_click=restart, type="secondary", use_container_width=True)
    
    else:
        render_header(4, "Предварительные варианты")
        
        uT, uH, uL, uW = st.session_state.answers['thick'], st.session_state.answers['h'], st.session_state.answers['l'], st.session_state.answers['w']
        
        subset_by_thick = df[df['Thick'] == uT]
        if subset_by_thick.empty:
            st.warning("В базе данных нет камер с выбранной толщиной панели.")
            st.button("Начать сначала", on_click=restart)
            st.stop()

        all_heights = subset_by_thick['Height_Ext'].unique()
        nearest_h = all_heights[(np.abs(all_heights - uH)).argmin()]
        final_subset = subset_by_thick[subset_by_thick['Height_Ext'] == nearest_h].copy()
        
        def fits(row, l, w): return (row['Length_Ext'] >= l and row['Width_Ext'] >= w) or (row['Length_Ext'] >= w and row['Width_Ext'] >= l)
        def is_smaller(row, l, w): return (row['Length_Ext'] <= l and row['Width_Ext'] <= w) or (row['Length_Ext'] <= w and row['Width_Ext'] <= l)

        opt_choices = final_subset[final_subset.apply(lambda r: fits(r, uL, uW), axis=1)]
        rOpt = opt_choices.sort_values(by='Volume_Intermal').head(1)

        eco_choices = final_subset[final_subset.apply(lambda r: is_smaller(r, uL, uW), axis=1)]
        rEco = eco_choices.sort_values(by='Volume_Intermal', ascending=False).head(1)
        if rEco.empty and not rOpt.empty: rEco = rOpt

        if not rOpt.empty:
            vOpt = rOpt['Volume_Intermal'].values[0]
            rPre = final_subset[final_subset['Volume_Intermal'] > vOpt].sort_values(by='Volume_Intermal').head(1)
        else:
            rPre = pd.DataFrame()

        st.caption(f"Расчет выполнен для ближайшей стандартной высоты сэндвич-панели: {nearest_h:.2f} м")
        st.write("")
        
        cols_results = st.columns(3)
        titles, colors = ["ЭКОНОМ", "ОПТИМАЛЬНО", "КОМФОРТ"], ["#fffde7", "#f1f8e9", "#e3f2fd"]
        
        for i, row in enumerate([rEco, rOpt, rPre]):
            with cols_results[i]:
                if not row.empty:
                    # Замена запятой на пробел в цене
                    price_str = f"{int(row['Price_RRC'].values[0]):,}".replace(",", " ")
                    
                    st.markdown(f'''
                        <div class="option-card" style="background-color: {colors[i]};">
                            <div>
                                <div style="height: 45px; display: flex; align-items: center; justify-content: center; margin-bottom: 5px;">
                                    <h3 style="color: #333; margin:0; line-height: 1.1;">{titles[i]}</h3>
                                </div>
                                <div class="dim-tag">{row['Height_Ext'].values[0]:.2f} x {row['Length_Ext'].values[0]:.2f} x {row['Width_Ext'].values[0]:.2f} м</div>
                                <p style="margin: 15px 0; color: #555;">Полезный объем:<br><b style="font-size: 20px; color: #333;">{row['Volume_Intermal'].values[0]:.2f} м³</b></p>
                            </div>
                            <div>
                                <div class="price-tag">{price_str} ₽</div>
                                <p style="font-size: 12px; color: #888; margin-top: 10px;">*Рекомендованная розница</p>
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="option-card" style="background-color: {colors[i]}; opacity: 0.6;"><div><div style="height: 45px; display: flex; align-items: center; justify-content: center; margin-bottom: 5px;"><h3 style="color: #333; margin:0;">{titles[i]}</h3></div></div><div><p style="color: #777;">Вариант не найден</p></div></div>', unsafe_allow_html=True)

        st.write("---")
        st.markdown("""
            <div style="background-color: #fff3e0; border-left: 10px solid #ff9800; padding: 25px; border-radius: 12px; margin: 10px 0 30px 0;">
                <h3 style="color: #e65100; margin-top: 0; font-size: 22px;">💰 Хотите цену ниже РРЦ?</h3>
                <p style="font-size: 16px; color: #333; line-height: 1.5; margin-bottom: 0;">Указанные цены - базовые. Оставьте заявку ниже: инженер пересчитает смету с учетом <b>максимальной скидки завода</b> и подготовит официальное КП за 15 минут.</p>
            </div>
        """, unsafe_allow_html=True)

        with st.form("final_lead", clear_on_submit=False):
            st.subheader("📩 Получить официальное КП со скидкой")
            
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                f_name = st.text_input("Ваше Имя / Компания*", placeholder="Иван Иванов / ООО Спектр")
                f_email = st.text_input("Email для ответа*", placeholder="example@mail.ru")
            with col_f2:
                f_phone = st.text_input("Номер телефона*", placeholder="+7 (999) 000-00-00")
                f_city = st.text_input("Город поставки*", placeholder="Нижний Новгород")
            
            st.write("")
            f_files = st.file_uploader("Прикрепить чертеж помещения или ТЗ (необязательно)", accept_multiple_files=True)
            st.write("")
            
            st.session_state.answers['temp_name'] = f_name if f_name else "уважаемый клиент"
            
            submit_final = st.form_submit_button("ПОЛУЧИТЬ ПРЕДЛОЖЕНИЕ СО СКИДКОЙ ДЛЯ БИЗНЕСА →", type="primary")
            
            if submit_final:
                if f_name and f_email and f_phone and f_city:
                    ans = st.session_state.answers
                    mail_body = f"НОВАЯ ЗАЯВКА ИЗ КОНСТРУКТОРА КАМЕР\n\n--- КОНТАКТЫ ---\nИмя/Компания: {f_name}\nТелефон: {f_phone}\nEmail: {f_email}\nГород: {f_city}\n\n--- ДАННЫЕ РАСЧЕТА ---\nНазначение: {ans.get('product')}\nГабариты (ВхДхШ): {ans.get('h')}x{ans.get('l')}x{ans.get('w')} м\nТолщина: {ans.get('thick')} мм\nПол: {ans.get('floor')}"
                    
                    msg = MIMEMultipart()
                    msg['Subject'] = f"🔔 Заявка Ариада (Конструктор): {f_name} ({f_city})"
                    sender_email = "marketing@ariada.ru" 
                    sender_password = "czvtubzwvaztqtwy" # <--- СГЕНЕРИРУЙ НОВЫЙ В ЯНДЕКСЕ И ВСТАВЬ СЮДА
                    
                    msg['From'] = sender_email
                    msg['To'] = "marketing@ariada.ru"
                    msg.attach(MIMEText(mail_body, 'plain', 'utf-8'))
                    
                    if f_files:
                        for f in f_files:
                            try:
                                part = MIMEApplication(f.read(), Name=f.name)
                                part['Content-Disposition'] = f'attachment; filename="{f.name}"'
                                msg.attach(part)
                            except:
                                st.error(f"Не удалось прикрепить файл: {f.name}")
                            
                    try:
                        server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
                        server.login(sender_email, sender_password)
                        server.send_message(msg)
                        server.quit()
                        st.session_state.submitted = True
                        st.rerun() 
                    except Exception as e:
                        st.error(f"Ошибка отправки почты. Проверьте настройки SMTP или пароль приложения. Ошибка: {e}")
                else:
                    st.error("Пожалуйста, заполните все обязательные поля, отмеченные звездочкой (*). Город критичен для расчета логистики.")

        st.write("")
        cb1, cb2 = st.columns(2)
        with cb1: st.button("← Изменить параметры", type="secondary", on_click=prev_step, use_container_width=True)
        with cb2: st.button("↺ Начать заново", type="secondary", on_click=restart, use_container_width=True)
        cb1, cb2 = st.columns(2)
        with cb1: st.button("← Изменить параметры", type="secondary", on_click=prev_step, use_container_width=True)
        with cb2: st.button("↺ Начать заново", type="secondary", on_click=restart, use_container_width=True)

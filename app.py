import streamlit as st
import google.generativeai as genai
from PIL import Image

# הגדרות דף ועיצוב RTL לעברית
st.set_page_config(page_title="EduCheck AI - Personalized", layout="wide")
st.markdown("""<style>body { direction: rtl; text-align: right; }</style>""", unsafe_allow_index=True)

st.title("📝 EduCheck AI: למידת כתב יד אישי")

# חיבור API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("נא להגדיר מפתח API ב-Secrets")

# סרגל צד ל"לימוד המערכת"
st.sidebar.header("🎓 לימוד המערכת (אופציונלי)")
st.sidebar.write("העלה דוגמה לכתב יד כדי שה-AI יבין אותו טוב יותר")
example_img = st.sidebar.file_uploader("צילום אות/מילה לדוגמה:", type=['png', 'jpg', 'jpeg'], key="example")
example_text = st.sidebar.text_input("מה כתוב בדוגמה?", placeholder="למשל: האות א'")

# מסך ראשי
col1, col2 = st.columns(2)

with col1:
    rubric = st.text_area("הכנס מחוון (בעברית או אנגלית):")
    test_img = st.file_uploader("העלה את צילום המבחן המלא:", type=['png', 'jpg', 'jpeg'], key="test")

if st.button("בדוק מבחן ⚡"):
    if test_img and rubric:
        with st.spinner('מנתח...'):
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # בניית הפקודה (Prompt) עם למידה מהדוגמה
            prompt = [f"אתה מורה מקצועי. השווה את המבחן למחוון: {rubric}. ענה בעברית."]
            
            if example_img and example_text:
                prompt.append(f"לצורך זיהוי כתב היד, הנה דוגמה: בתמונה הזו כתוב '{example_text}'")
                prompt.append(Image.open(example_img))
            
            prompt.append("הנה המבחן המלא לבדיקה:")
            prompt.append(Image.open(test_img))
            
            try:
                response = model.generate_content(prompt)
                st.success("הבדיקה הושלמה!")
                st.write(response.text)
            except Exception as e:
                st.error(f"שגיאה בבדיקה: {e}")

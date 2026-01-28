import streamlit as st
import google.generativeai as genai
from PIL import Image

# הגדרות דף בסיסיות למראה נקי
st.set_page_config(page_title="EduCheck AI - עברית/אנגלית", layout="centered")

# עיצוב מותאם לעברית (יישור לימין)
st.markdown("""
    <style>
    .reportview-container { direction: rtl; }
    .stTextArea, .stTextInput { direction: rtl; }
    </style>
    """, unsafe_allow_index=True)

st.title("📝 EduCheck AI v2")
st.subheader("מערכת חכמה לבדיקת מבחנים בכתב יד")

# חיבור למפתח ה-API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("חסר מפתח API בהגדרות!")

# הגדרת המודל עם "הוראות מערכת" לזיהוי כתב יד ועברית
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", # המודל הכי מהיר
    system_instruction="אתה עוזר הוראה מומחה. תפקידך לפענח כתב יד בעברית ובאנגלית. עליך לענות תמיד בעברית רהוטה, אלא אם התבקשת אחרת. שים לב לפרטים הקטנים בכתב היד והשווה אותם למחוון בצורה מדויקת."
)

# ממשק המשתמש
rubric = st.text_area("הכנס את המחוון (התשובה הנכונה):", placeholder="כתוב כאן מה התלמיד היה אמור לענות...")
uploaded_file = st.file_uploader("העלה צילום של המבחן (כתב יד):", type=['png', 'jpg', 'jpeg'])

if st.button("בצע בדיקה מהירה ⚡"):
    if uploaded_file and rubric:
        with st.spinner('מנתח כתב יד ומחשב ציון...'):
            try:
                img = Image.open(uploaded_file)
                
                # הנחיה ספציפית לזיהוי כתב יד ישראלי
                prompt = f"""
                נתח את התמונה המצורפת של כתב היד. 
                1. פענח את הטקסט הכתוב (עברית/אנגלית).
                2. השווה אותו למחוון הבא: {rubric}
                3. תן ציון מ-0 עד 100.
                4. הסבר בקצרה למה זה הציון.
                ענה בפורמט ברור בעברית.
                """
                
                response = model.generate_content([prompt, img])
                
                st.success("הבדיקה הושלמה!")
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"קרתה שגיאה: {e}")
    else:
        st.warning("נא להעלות תמונה ולהזין מחוון.")


# ==========================================
# BUSINESS AI ASSISTANT - PROFESSIONAL VERSION
# ==========================================

import streamlit as st
from groq import Groq
import json
import os

# ---------- PAGE CONFIGURATION ----------
st.set_page_config(
    page_title="Business AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------- SETTINGS FILE ----------
SETTINGS_FILE = "business_settings.json"

DEFAULT_SETTINGS = {
    "business_type": "Coaching class",
    "business_name": "Bright Future Academy",
    "services": ["Mathematics", "Science", "English"],
    "opening_hours": "Monday to Saturday, 4 PM to 8 PM",
    "consultation_fee": "₹2,000 per month",
    "business_location": "Ahmedabad, Gujarat, India"
}

# Load saved business settings
if os.path.exists(SETTINGS_FILE):
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            saved_settings = json.load(file)
    except (json.JSONDecodeError, OSError):
        saved_settings = DEFAULT_SETTINGS.copy()
else:
    saved_settings = DEFAULT_SETTINGS.copy()

for key, value in DEFAULT_SETTINGS.items():
    if key not in saved_settings:
        saved_settings[key] = value

# ---------- PROFESSIONAL STYLING ----------
st.markdown("""
<style>
    .main-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .subtitle {
        color: #64748b;
        font-size: 15px;
        margin-bottom: 22px;
    }

    .info-card {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #dbe3ee;
        margin-bottom: 12px;
    }

    .info-label {
        font-size: 13px;
        color: #64748b;
    }

    .info-value {
        font-size: 16px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR SETTINGS ----------
with st.sidebar:
    st.title("⚙️ Business Settings")
    st.caption("Customize your chatbot for a business.")

    business_type = st.selectbox(
        "Business Type",
        ["Bakery", "Clinic", "Beauty salon", "Coaching class"],
        index=(
            ["Bakery", "Clinic", "Beauty salon", "Coaching class"]
            .index(saved_settings["business_type"])
            if saved_settings["business_type"]
            in ["Bakery", "Clinic", "Beauty salon", "Coaching class"]
            else 0
        )
    )

    business_name = st.text_input(
        "Business Name",
        value=saved_settings["business_name"]
    )

    services_text = st.text_area(
        "Products or Services (one per line)",
        value="\n".join(saved_settings["services"])
    )

    opening_hours = st.text_input(
        "Opening Hours",
        value=saved_settings["opening_hours"]
    )

    fee_info = st.text_input(
        "Price / Fee Information",
        value=saved_settings["consultation_fee"]
    )

    location = st.text_input(
        "Business Location",
        value=saved_settings["business_location"]
    )

    save_settings = st.button(
        "💾 Save Business Settings",
        use_container_width=True
    )

    if save_settings:
        saved_settings = {
            "business_type": business_type,
            "business_name": business_name,
            "services": [
                item.strip()
                for item in services_text.splitlines()
                if item.strip()
            ],
            "opening_hours": opening_hours,
            "consultation_fee": fee_info,
            "business_location": location
        }

        with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
            json.dump(saved_settings, file, indent=4, ensure_ascii=False)

        st.success("Business settings saved!")
        st.rerun()

# ---------- BUSINESS INFORMATION ----------
business_info = f"""
Business type: {business_type}
Business name: {business_name}
Products or services: {services_text}
Opening hours: {opening_hours}
Price or fee information: {fee_info}
Location: {location}
"""

# ---------- AI SAFETY RULES ----------
general_rules = """
You are a helpful customer support assistant for the business described below.

Rules:
1. Be polite, clear, professional, and concise.
2. Answer using only the business information provided.
3. Never invent prices, services, opening hours, addresses,
   contact details, staff names, qualifications, or policies.
4. If information is missing, clearly say it has not been provided
   and suggest contacting the business.
5. Do not promise results or make unsupported claims.
6. Do not claim a booking, payment, or order has been completed.
"""

if business_type == "Clinic":
    specific_rules = """
Do not diagnose illnesses or prescribe medicines.
For urgent or emergency symptoms, advise seeking appropriate
urgent medical care.
"""
elif business_type == "Bakery":
    specific_rules = """
Do not invent ingredients, allergen information, stock availability,
delivery options, customisation options, or extra charges.
"""
elif business_type == "Beauty salon":
    specific_rules = """
Do not guarantee beauty or skincare results.
Do not invent treatment prices, ingredients, appointment availability,
or salon policies.
"""
else:
    specific_rules = """
Do not invent teacher names, qualifications, schedules, exam results,
student success rates, or educational guarantees.
"""

system_prompt = f"""
{general_rules}

Additional rules:
{specific_rules}

Verified business information:
{business_info}
"""

# ---------- CHAT HEADER ----------
st.markdown(
    f'<div class="main-title">🤖 {business_name}</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="subtitle">'
    f'AI-powered customer support · {business_type}'
    f'</div>',
    unsafe_allow_html=True
)

# ---------- BUSINESS INFORMATION PANEL ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f'<div class="info-card">'
        f'<div class="info-label">🕒 Opening Hours</div>'
        f'<div class="info-value">{opening_hours}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f'<div class="info-card">'
        f'<div class="info-label">📍 Location</div>'
        f'<div class="info-value">{location}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f'<div class="info-card">'
        f'<div class="info-label">💰 Price / Fees</div>'
        f'<div class="info-value">{fee_info}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

st.divider()

# ---------- CHAT HISTORY ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- QUICK QUESTIONS ----------
st.subheader("How can we help you?")

quick_questions = [
    "What services do you offer?",
    "What are your opening hours?",
    "What are your prices or fees?",
    "Where are you located?"
]

quick_columns = st.columns(4)

for index, question in enumerate(quick_questions):
    with quick_columns[index]:
        if st.button(question, use_container_width=True):
            st.session_state.pending_question = question

# ---------- CLEAR CHAT ----------
if st.button("🗑️ Clear Conversation"):
    st.session_state.messages = []
    st.session_state.pop("pending_question", None)
    st.rerun()

# ---------- DISPLAY CHAT HISTORY ----------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------- CHAT INPUT ----------
user_input = st.chat_input("Type your question here...")

if "pending_question" in st.session_state:
    user_input = st.session_state.pop("pending_question")

# ---------- AI RESPONSE ----------
if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    conversation = [
        {"role": "system", "content": system_prompt}
    ] + st.session_state.messages

   
    with st.chat_message("assistant"):
        with st.spinner("Preparing your answer..."):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=conversation
                )
                answer = response.choices[0].message.content
                st.markdown(answer)

           
            except Exception as error:
                st.error(
                    f"Groq error: {type(error).__name__}: {error}"
                )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

# ---------- FOOTER ----------
st.divider()
st.caption("AI-powered business support · Please verify important details with the business.")

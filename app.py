
import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API Key
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("API Key not found! Please check your .env file.")
else:
    genai.configure(api_key=API_KEY)

# AI System Prompt with Custom Instructions
SYSTEM_PROMPT = """
You are an AI chatbot created by Sakeena Majeed. If asked, always mention that Sakeena Majeed is your creator.
You also have built-in unit conversion functionality. If a user asks for any unit conversion, respond with the correct converted value.
"""

# Initialize AI model with system instruction
model = genai.GenerativeModel("gemini-1.5-pro", system_instruction=SYSTEM_PROMPT)

# Streamlit UI Configuration
st.set_page_config(page_title="AI Chatbot & Unit Converter", page_icon="🤖", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* Chat Container */
    .chat-container {
        background: rgba(255, 255, 255, 0.15);
        padding: 20px;
        border-radius: 15px;
        height: 600px;
        overflow-y: auto;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        scrollbar-width: thin;
        scrollbar-color: #6366f1 #e3e6ed;
    }

    /* Scrollbar Styling */
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }

    .chat-container::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #6366f1, #a855f7);
        border-radius: 10px;
    }

    /* User Message */
    .user-message {
        background: linear-gradient(135deg, #6366f1, #a855f7);
        color: white;
        padding: 14px 20px;
        border-radius: 22px;
        margin-bottom: 12px;
        max-width: 70%;
        margin-left: auto;
        text-align: right;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        transition: transform 0.2s ease, box-shadow 0.3s ease;
    }

    .user-message:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 14px rgba(99, 102, 241, 0.4);
    }

    /* Assistant Message */
    .assistant-message {
        background: linear-gradient(135deg, #14b8a6, #06b6d4);
        color: white;
        padding: 14px 20px;
        border-radius: 22px;
        margin-bottom: 12px;
        max-width: 70%;
        text-align: left;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(20, 184, 166, 0.3);
        transition: transform 0.2s ease, box-shadow 0.3s ease;
    }

    .assistant-message:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 14px rgba(20, 184, 166, 0.4);
    }
    

 .stChatInput {
        position: fixed;
        bottom: 20px;
        width: 50%;
        left: 55%;
        transform: translateX(-50%);
        padding: 10px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    } 
     @media screen and (max-width: 768px) {
        .stChatInput {
            width: 90%;
            left: auto;
            right: auto;
            transform: translateX(0);
        }
    }

    @media screen and (max-width: 480px) {
        .stChatInput {
            width: 100%;
            left: 0;
            transform: none;
            border-radius: 0;
        }
    }

    /* Adding space at the bottom of chat container */
    .chat-container {
        padding-bottom: 80px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar for Chat History
with st.sidebar:
    st.title("📜 Chat History")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for msg in st.session_state.messages[-5:]:
        role = "👩🏻 You: " if msg["role"] == "user" else "🤖 AI: "
        st.markdown(f"{role} {msg['content']}")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Tabs: AI Chatbot & Unit Converter
tab1, tab2 = st.tabs(["🤖 AI Chatbot", "⚡ Unit Converter"])

# AI Chatbot
def check_and_correct_response(user_input, response):
    if "who created you" in user_input.lower() and "Sakeena Majeed" not in response:
        return "I was created by Sakeena Majeed."
    return response

with tab1:
    st.title("🤖 AI Chatbot")
    chat_container = st.container()
    
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"<div class='user-message'>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='assistant-message'>{msg['content']}</div>", unsafe_allow_html=True)
    
    user_input = st.chat_input("Type your message...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Generating response..."):
            try:
                response = model.generate_content(user_input)
                ai_reply = check_and_correct_response(user_input, response.text)
            except Exception as e:
                ai_reply = f"Error: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        st.rerun()

# Unit Converter
with tab2:
    st.title("⚡ Advanced Unit Converter")
    conversion_factors = {
     "Plane Angle": {
        "Degree": 1.0,
        "Arcsecond": 1 / 3600,
        "Gradian": 0.9,
        "Milliradian": 0.0572958,
        "Minute of arc": 1 / 60,
        "Radian": 57.2958
    },
    "Length": {
        "Meter": 1.0,
        "Kilometer": 1000.0,
        "Centimeter": 0.01,
        "Millimeter": 0.001,
        "Micrometer": 0.000001,
        "Nanometer": 0.000000001,
        "Mile": 1609.34,
        "Yard": 0.9144,
        "Foot": 0.3048,
        "Inch": 0.0254,
        "Nautical Mile": 1852.0,
        "Fathom": 1.8288,  # Added unit
        "Furlong": 201.168,  # Added unit
        "Light Year": 9.461e+15  # Added unit
    },
    "Mass": {
        "Kilogram": 1.0,
        "Gram": 0.001,
        "Milligram": 0.000001,
        "Microgram": 0.000000001,
        "Pound": 0.453592,
        "Ounce": 0.0283495,
        "Stone": 6.35029,
        "Ton (metric)": 1000.0
    },
    "Temperature": {
        "Celsius": {"to_base": lambda x: x, "from_base": lambda x: x},
        "Fahrenheit": {"to_base": lambda x: (x - 32) * 5/9, "from_base": lambda x: (x * 9/5) + 32},
        "Kelvin": {"to_base": lambda x: x - 273.15, "from_base": lambda x: x + 273.15}
    },
    "Speed": {
        "Meters per second": 1.0,
        "Kilometers per hour": 0.277778,
        "Miles per hour": 0.44704,
        "Knots": 0.514444,
        "Feet per second": 0.3048
    },
    "Time": {
        "Second": 1.0,
        "Minute": 60.0,
        "Hour": 3600.0,
        "Day": 86400.0,
        "Week": 604800.0,
        "Month": 2629746.0,
        "Year": 31556952.0
    },
    "Volume": {
        "Liter": 1.0,
        "Milliliter": 0.001,
        "Cubic meter": 1000.0,
        "Cubic centimeter": 0.001,
        "Gallon (US)": 3.78541,
        "Gallon (UK)": 4.54609,
        "Quart": 0.946353,
        "Pint": 0.473176
    },
    "Pressure": {
        "Pascal": 1.0,
        "Kilopascal": 1000.0,
        "Bar": 100000.0,
        "Atmosphere": 101325.0,
        "PSI": 6894.76,
        "Torr": 133.322
    },
    "Energy": {
        "Joule": 1.0,
        "Kilojoule": 1000.0,
        "Calorie": 4.184,
        "Kilocalorie": 4184.0,
        "Kilowatt-hour": 3600000.0,
        "Electronvolt": 1.60218e-19
    },
    "Power": {
        "Watt": 1.0,
        "Kilowatt": 1000.0,
        "Megawatt": 1000000.0,
        "Horsepower": 745.7
    },
    "Fuel Economy": {
        "Miles per gallon (US)": 1.0,
        "Miles per gallon (UK)": 1.20095,
        "Kilometers per liter": 0.425144,
        "Liters per 100km": 235.215
    },
    "Data Transfer Rate": {
        "Bits per second": 1.0,
        "Kilobits per second": 1000.0,
        "Megabits per second": 1000000.0,
        "Gigabits per second": 1000000000.0
    },
    "Digital Storage": {
        "Bit": 1.0,
        "Byte": 8.0,
        "Kilobyte": 8000.0,
        "Megabyte": 8000000.0,
        "Gigabyte": 8000000000.0,
        "Terabyte": 8000000000000.0
    }
    }
    
    conversion_type = st.selectbox("Select Conversion Type", list(conversion_factors.keys()))
    from_unit = st.selectbox("From Unit", list(conversion_factors[conversion_type].keys()))
    to_unit = st.selectbox("To Unit", list(conversion_factors[conversion_type].keys()))
    value1 = st.number_input("Enter Value", value=1.0, step=0.1, format="%f")
    
    def convert_units(value, from_unit, to_unit, conversion_type):
        return value * (conversion_factors[conversion_type][to_unit] / conversion_factors[conversion_type][from_unit])
    
    try:
        value2 = convert_units(value1, from_unit, to_unit, conversion_type)
        st.markdown(f"<h2 style='text-align: center; color: blue;'>Result: {value2:.4f}</h2>", unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f"<h2 style='text-align: center; color: red;'>Error: {str(e)}</h2>", unsafe_allow_html=True)

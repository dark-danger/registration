import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- Google Sheets Setup ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["gcp"]  # 'gcp' key in secrets.toml
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

sheet = client.open("GDSC_Registrations").sheet1  # replace with your sheet name

def add_registration(data):
    """data = [Name, Email, Phone, Roll, Dept, Event]"""
    sheet.append_row(data)

# --- Page Config ---
st.set_page_config(
    page_title="GDSC Event Registration",
    page_icon="images/gdsc.png",  # local path works in dev
    layout="wide"
)

# --- Custom CSS ---
st.markdown("""
<style>
body { background-color: #f9f9f9; font-family: 'Segoe UI', sans-serif; }
.header-container { display:flex; justify-content:space-between; align-items:center; 
                    padding:15px 30px; background-color:#ffffff; border-radius:12px; 
                    margin:auto; margin-bottom:30px; max-width:1000px; box-shadow:0 2px 6px rgba(0,0,0,0.1);}
.header-title { font-size:26px; font-weight:bold; color:#202124; }
.center-container { max-width:900px; margin:auto; }
.event-card { background:#fff; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.08); 
              padding:15px; margin-bottom:25px; text-align:center; transition: transform 0.2s ease-in-out; }
.event-card:hover { transform: translateY(-4px); box-shadow:0 4px 12px rgba(0,0,0,0.15); }
.event-title { font-size:18px; font-weight:600; margin:10px 0; color:#111; }
.event-buttons { display:flex; justify-content:space-around; margin-top:10px; }
</style>
""", unsafe_allow_html=True)

# --- Events Data ---
events = [
    {"name": "Google Sparks", 
     "image": "https://i.postimg.cc/QNvRLvvB/1.png", 
     "desc": "Participate in a thrilling city-wide scavenger hunt and solve tech challenges along the way.", 
     "rules": ["ppt must be made using google slides", "Follow the marked route", "No use of vehicles", "Stay in teams of 2-4"]},

    {"name": "Tech Quizathon", 
     "image": "https://i.postimg.cc/GhkgWtF0/2.png", 
     "desc": "Test your tech knowledge in this rapid-fire quiz competition with prizes for winners.", 
     "rules": ["Each team: max 3 members", "No external help allowed", "Time limit for each question", "Be on time"]},

    {"name": "Robo War", 
     "image": "https://i.postimg.cc/htsyGYZJ/3.png", 
     "desc": "Showcase your robotics skills as your robots battle in an arena to claim victory.", 
     "rules": ["Register in teams", "Use approved robot dimensions", "Safety first: goggles mandatory", "No external interference"]},

    {"name": "Startup Pitch", 
     "image": "https://i.postimg.cc/YCMDM73s/4.png", 
     "desc": "Pitch your innovative startup idea to judges and get feedback or funding opportunities.", 
     "rules": ["Pitch time: 5 minutes", "Slides allowed (max 5)", "Judges Q&A mandatory", "Original ideas only"]}
]

# --- Session State ---
if "view" not in st.session_state:
    st.session_state.view = "gallery"
if "selected_event" not in st.session_state:
    st.session_state.selected_event = None

# --- Navigation Functions ---
def go_to_form(event): st.session_state.selected_event, st.session_state.view = event, "form"
def go_to_info(event): st.session_state.selected_event, st.session_state.view = event, "info"
def go_back(): st.session_state.selected_event, st.session_state.view = None, "gallery"

# --- Header ---
st.markdown(f"""
<div class="header-container" style="display:flex; align-items:center; gap:10px;">
    <img src="https://geetauniversity.com/assets/images/logo.png" width="80" alt="My Logo">
    <div class="header-title">GDSC Event Registration</div>
    <img src="https://i.postimg.cc/zGKXhCYY/gdsc.png" width="120" alt="Geeta University Logo">
</div>
""", unsafe_allow_html=True)

# --- Gallery View ---
if st.session_state.view == "gallery":
    st.markdown('<div class="center-container">', unsafe_allow_html=True)
    st.subheader("🔥 Events")
    
    for i in range(0, len(events), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(events):
                ev = events[i + j]
                with cols[j]:
                    st.markdown(f"""
                        <div class="event-card">
                            <img src="{ev['image']}" width="100%">
                            <div class="event-title">{ev['name']}</div>
                            <p style="font-size:14px; color:#555;">{ev['desc']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    col_btn1, col_btn2 = st.columns([1,1])
                    with col_btn1:
                        if st.button("Register", key=f"reg_{i+j}"): go_to_form(ev["name"])
                    with col_btn2:
                        if st.button("Event Info", key=f"info_{i+j}"): go_to_info(ev["name"])
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Registration Form View ---
elif st.session_state.view == "form":
    st.markdown('<div class="center-container">', unsafe_allow_html=True)
    st.subheader(f"📝 Register for {st.session_state.selected_event}")
    
    with st.form("registration_form"):
        full_name = st.text_input("Full Name", "")
        email = st.text_input("Email Address", "")
        contact = st.text_input("Contact Number", "")
        roll = st.text_input("Roll Number", "")
        depart = st.text_input("Department", "")
        
        event = st.selectbox("Select Event", ["Google Sparks", "Tech Quizathon", "Robo War", "Startup Pitch"])
        waiver = st.checkbox("I agree to the rules and regulations")
        
        submit = st.form_submit_button("Submit")
        
        if submit:
            if not waiver:
                st.warning("You must agree to the rules to register.")
            else:
                add_registration([full_name, email, contact, roll, depart, event])
                st.success("Registration successful!")

# --- Event Info View ---
elif st.session_state.view == "info":
    ev = next(e for e in events if e["name"] == st.session_state.selected_event)
    st.markdown('<div class="center-container">', unsafe_allow_html=True)
    
    st.subheader(f"📘 {ev['name']} Info")
    st.markdown(f"**Description:** {ev['desc']}")
    st.markdown("**Rules:**")
    for r in ev["rules"]:
        st.markdown(f"- {r}")
    
    if st.button("⬅ Back to Events"): go_back()
    st.markdown('</div>', unsafe_allow_html=True)

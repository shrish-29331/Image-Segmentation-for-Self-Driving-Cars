import streamlit as st
from pymongo import MongoClient

# --- MongoDB CONNECTION ---
client = MongoClient("mongodb+srv://jaspreetps1984:g3vvKhpxv7jEigl2@cluster0.ycbkoir.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['test_database']
users = db['users']

# --- Write Role and Username to constants.py ---
def write_constants(ta_flag):
    with open("constants.py", "w") as f:
        f.write(f"TA = {ta_flag}\n")
        f.write(f"username = '{st.session_state['username']}'\n")

# --- UI TITLE ---
st.title("🔐 Welcome to Assignment Portal")

# --- Form UI ---
with st.form("login_form"):
    st.text_input("👤 Username", key="username")
    st.text_input("🔑 Password", type="password", key="password")
    role = st.selectbox("🎓 Select Role", ["student", "ta"], key="role")
    submitted = st.form_submit_button("Login")

# --- Handle Submission ---
if submitted:
    uname = st.session_state["username"].strip()
    pwd = st.session_state["password"].strip()
    selected_role = st.session_state["role"]

    user = users.find_one({"username": uname})

    if not user:
        st.error("❌ Invalid username or password.")
    elif user.get("password") != pwd:
        st.error("❌ Invalid username or password.")
    elif user.get("role") != selected_role:
        st.error(f"❌ Incorrect role. You are registered as a {user.get('role')}.")
    else:
        st.success(f"✅ Logged in as {uname} ({selected_role})")
        write_constants(0 if selected_role == "student" else 1)
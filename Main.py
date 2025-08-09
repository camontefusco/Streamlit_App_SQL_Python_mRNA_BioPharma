import streamlit as st
from streamlit_option_menu import option_menu
import random

# Import internal pages
import Home
import Create
import Read
import Update
import Delete
import Visualize
import Map

# ----- PAGE CONFIG -----
st.set_page_config(page_title="mRNA BioPharma App", layout="wide")

# ---------- OPTIMIZED PHARMA BACKGROUND ----------
# Generate floating molecules only once
molecule_html = ""
for _ in range(12):  # fewer elements = faster rendering
    size = random.randint(8, 18)
    x = random.randint(0, 100)
    y = random.randint(0, 100)
    duration = random.uniform(10, 25)
    molecule_html += f"""
    <div class="molecule" style="
        width:{size}px;
        height:{size}px;
        left:{x}%;
        top:{y}%;
        animation-duration:{duration}s;
    "></div>
    """

st.markdown(
    f"""
    <style>
    /* Main background gradient */
    .stApp {{
        background: radial-gradient(circle at center, #0d1b2a 0%, #050d16 100%) !important;
        color: #e0f7fa !important;
    }}

    /* Sidebar background */
    section[data-testid="stSidebar"] > div {{
        background: linear-gradient(180deg, rgba(13,27,42,0.95) 0%, rgba(5,13,22,0.95) 100%);
        border-right: 1px solid rgba(255,255,255,0.05);
    }}

    /* DNA background image */
    .dna {{
        position: fixed;
        top: -150px;
        right: -150px;
        width: 500px;
        height: 1000px;
        background: url('https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/DNA_double_helix_vertical.png/320px-DNA_double_helix_vertical.png') no-repeat center;
        background-size: contain;
        opacity: 0.05;
        animation: dnaScroll 50s linear infinite;
        pointer-events: none;
        z-index: 0;
    }}

    @keyframes dnaScroll {{
        from {{ transform: translateY(0); }}
        to {{ transform: translateY(150px); }}
    }}

    /* Floating molecules */
    .molecule {{
        position: fixed;
        border-radius: 50%;
        background-color: rgba(173, 216, 230, 0.5);
        box-shadow: 0 0 4px rgba(173, 216, 230, 0.6);
        animation: float 12s infinite ease-in-out;
        pointer-events: none;
        z-index: 0;
    }}

    @keyframes float {{
        0% {{ transform: translateY(0px) translateX(0px); }}
        50% {{ transform: translateY(-15px) translateX(8px); }}
        100% {{ transform: translateY(0px) translateX(0px); }}
    }}
    </style>

    <div class="dna"></div>
    {molecule_html}
    """,
    unsafe_allow_html=True
)
# ---------- END BACKGROUND ----------

# ---------- SIDEBAR MENU ----------
with st.sidebar:
    selected = option_menu(
        menu_title="📊 mRNA BioPharma Navigation",
        options=[
            "Home", "Add Data", "View Data", "Update", "Delete", "Visualize", "Map"
        ],
        icons=[
            "house", "plus-circle", "table", "pencil-square", "trash", "bar-chart", "geo-alt"
        ],
        menu_icon="capsule-pill",
        default_index=0
    )

# ---------- PAGE ROUTER ----------
if selected == "Home":
    Home.show()
elif selected == "Add Data":
    Create.show()
elif selected == "View Data":
    Read.show()
elif selected == "Update":
    Update.show()
elif selected == "Delete":
    Delete.show()
elif selected == "Visualize":
    Visualize.show()
elif selected == "Map":
    Map.show()

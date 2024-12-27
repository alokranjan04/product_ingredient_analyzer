import streamlit as st
import os
from PIL import Image
from io import BytesIO
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.tavily import TavilyTools
from tempfile import NamedTemporaryFile
from constants import SYSTEM_PROMPT, INSTRUCTIONS

# Environment variables setup


os.environ['TAVILY_API_KEY'] =  st.secrets['TAVILY_KEY'] 
os.environ['GOOGLE_API_KEY'] =  st.secrets['GEMINI_KEY'] 

MAX_IMAGE_WIDTH = 300
def main():
    st.markdown("""
        <style>
        /* App background and container */
        .stApp {
            background: #f5f7fa;
        }
        
        /* Title and header */
        .stMarkdown h1 {
            color: #2193b0;
            font-size: 2.5em;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
            padding: 0.5rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding: 0 20px;
            background: white;
            border-radius: 8px;
            color: #2193b0;
        }
        
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            background: linear-gradient(90deg, #2193b0, #6dd5ed);
            color: white;
        }
        
        /* Product cards */
        .product-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            text-align: center;
            margin-bottom: 1rem;
        }
        
        /* Buttons */
        .stButton > button {
            width: 100%;
            background: linear-gradient(90deg, #2193b0, #6dd5ed);
            color: white;
            padding: 0.8rem 1.5rem;
            border-radius: 8px;
            border: none;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(33, 147, 176, 0.3);
        }
        
        /* Upload section */
        .upload-section {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # Title Section
    st.markdown("""
        <div class="title-container">
            <h1 class="title-text">🔍 Product Ingredient Analyzer</h1>
        </div>
    """, unsafe_allow_html=True)
    # Initialize session state for selected product
    if 'selected_product' not in st.session_state:
        st.session_state.selected_product = None


    tabs = st.tabs(["📚 Example Products", "📤 Upload Image", "📸 Take Photo"])
    
    with tabs[0]:
        products = {
            "🍫 Chocolate Bar": "./images/hide_and_seek.jpg",
            "🥤 Energy Drink": "./images/bournvita.jpg",
            "🥔 Potato Chips": "./images/lays.jpg",
            "🧴 Shampoo": "./images/shampoo.jpg"
        }
        
        # Create a clean card layout
        st.markdown('<div class="product-grid">', unsafe_allow_html=True)
        cols = st.columns(4)
        for idx, (name, image_path) in enumerate(products.items()):
            with cols[idx]:
                # Display product card without image
                st.markdown(f"""
                    <div style="padding: 1rem; border-radius: 10px; border: 1px solid #eee; text-align: center;">
                        <div style="font-size: 2rem;">{name[0]}</div>
                        <div style="margin-top: 0.5rem;">{name[2:]}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Analyze button
                if st.button("Analyze", key=f"analyze_{idx}"):
                    st.session_state.selected_product = image_path
                
                # Show image only if this product is selected
                if st.session_state.selected_product == image_path:
                    try:
                        image = Image.open(image_path)
                        st.image(image, caption=name[2:], width=300)
                        analyze_image(image_path)
                    except Exception as e:
                        st.warning(f"Unable to load image: {image_path}")

    
    with tabs[1]:
        uploaded_file = st.file_uploader("Upload product image", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Image", width=300)
            if st.button("Analyze Upload", key="analyze_upload"):
                analyze_image(uploaded_file)
    
    with tabs[2]:
        camera_photo = st.camera_input("Take a photo")
        if camera_photo:
            st.image(camera_photo, caption="Captured Photo", width=300)
            if st.button("Analyze Photo", key="analyze_camera"):
                analyze_image(camera_photo)

def analyze_product(image_path):
    st.session_state.selected_example = image_path
    analyze_image(image_path)

def analyze_image(image):
    with st.spinner('Analyzing ingredients...'):
        agent = get_agent()
        if isinstance(image, str):
            response = agent.run("Analyze the given image", images=[image])
        else:
            temp_path = save_uploaded_file(image)
            response = agent.run("Analyze the given image", images=[temp_path])
            os.unlink(temp_path)
        st.markdown(response.content)

def display_product_image(image_path):
    try:
        image = Image.open(image_path)
        st.image(image, caption="Product Image", width=300)
    except Exception as e:
        st.warning("Product image not available")


@st.cache_resource
def get_agent():
    return Agent(
        model=Gemini(id="gemini-2.0-flash-exp"),
        system_prompt=SYSTEM_PROMPT,
        instructions=INSTRUCTIONS,
        tools=[TavilyTools(api_key=os.getenv("TAVILY_API_KEY"))],
        markdown=True,
    )

def save_uploaded_file(uploaded_file):
    with NamedTemporaryFile(dir='.', suffix='.jpg', delete=False) as f:
        f.write(uploaded_file.getbuffer())
        return f.name

if __name__ == "__main__":
    st.set_page_config(
        page_title="Product Ingredient Analyzer",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    main()

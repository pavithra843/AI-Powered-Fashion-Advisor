import streamlit as st
from transformers import CLIPProcessor as HF_CLIPProcessor, CLIPModel
from PIL import Image

# Set the page configuration for a premium look
st.set_page_config(
    page_title="Style Finder",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load Hugging Face models
@st.cache_resource
def load_models():
    clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    clip_processor = HF_CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    return clip_model, clip_processor

clip_model, clip_processor = load_models()

# Function to analyze and return style details
def analyze_style(image):
    styles = [
        "elegant", "casual", "bold", "trendy", "minimalist", 
        "vintage", "colorful", "athleisure", "formal", 
        "bohemian", "grunge", "preppy", "streetwear", 
        "monochromatic", "futuristic", "romantic", "edgy"
    ]
    
    inputs = clip_processor(text=styles, images=image, return_tensors="pt", padding=True)
    outputs = clip_model(**inputs)
    logits_per_image = outputs.logits_per_image
    scores = logits_per_image.softmax(dim=1).tolist()[0]
    
    max_index = scores.index(max(scores))
    rating = round(7 + max(scores) * 3, 1)
    detected_style = styles[max_index]
    
    style_comments = {
        "elegant": "A showcase of timeless elegance. Your outfit screams sophistication with refined cuts and polished textures.",
        "casual": "Effortless and comfortable, perfect for coffee dates or quick errands. It blends practicality with style.",
        "bold": "Daring and unapologetic! Vibrant colors and strong cuts make this a statement look.",
        "trendy": "You're ahead of the curve. This outfit reflects the latest runway inspirations with a chic touch.",
        "minimalist": "Understated yet powerful. Clean lines and neutral colors embody the less-is-more philosophy.",
        "vintage": "A nod to the past, your look captures retro vibes with a modern twist.",
        "colorful": "Bright and cheerful! This outfit is a celebration of fun and vibrant hues.",
        "athleisure": "Comfort meets style! Perfect for both workouts and lounging in trend.",
        "formal": "Tailored perfection. This outfit is polished, professional, and ideal for high-profile events.",
        "bohemian": "Free-spirited and dreamy. Your look is a mix of earthy tones, patterns, and flowing fabrics.",
        "grunge": "Rebellious and raw! Think oversized pieces, dark tones, and an effortlessly cool attitude.",
        "preppy": "Clean, classy, and collegiate. Your outfit reflects a timeless school-inspired style.",
        "streetwear": "Edgy and urban! This look is all about sneakers, hoodies, and bold graphics.",
        "monochromatic": "A masterclass in one-tone styling. Simple yet striking.",
        "futuristic": "Ahead of its time! Metallics, sleek cuts, and innovative designs define your style.",
        "romantic": "Soft, delicate, and feminine. Think floral prints, pastels, and flowing fabrics.",
        "edgy": "Unconventional and daring. Your look combines sharp lines and unexpected elements."
    }
    
    return rating, detected_style, style_comments[detected_style]

# Enhanced UI Design
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Sans+Pro:wght@300;400;700&display=swap');
        body {
            font-family: 'Source Sans Pro', sans-serif;
            color: #2c2c2c;
            background-color: #ffffff;
        }
        .header-title {
            font-family: 'Playfair Display', serif;
            font-size: 56px;
            font-weight: 700;
            color: #1a1a1a;
            text-align: center;
            margin: 20px 0;
        }
        .subheader {
            font-size: 20px;
            color: #6c757d;
            text-align: center;
            margin-bottom: 30px;
        }
        .upload-btn {
            background-color: #1a1a1a;
            color: #ffffff;
            padding: 12px 24px;
            font-size: 16px;
            border-radius: 30px;
            border: none;
            cursor: pointer;
            display: block;
            margin: 20px auto;
        }
        .upload-btn:hover {
            background-color: #4a4a4a;
        }
        .image-container img {
            display: block;
            margin: 20px auto;
            width: 300px; 
            height: auto/* Smaller image size */
            border-radius: 16px; /* Soft corners */
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); /* Subtle shadow */
        }
        .rating-box {
            font-family: 'Playfair Display', serif;
            font-size: 36px;
            font-weight: bold;
            color: #C08497;
            text-align: center;
            margin: 20px 0;
        }
        .style-comment {
            font-size: 18px;
            font-style: italic;
            color: #444444;
            margin: 20px auto;
            width: 80%;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="header-title">Get your fits rated!!</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Let AI review your oufits</div>', unsafe_allow_html=True)
st.markdown("---")

# Image Upload Section
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if uploaded_file:
    image = Image.open(uploaded_file)
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image(image, caption="Uploaded Outfit", use_container_width=False)
    st.markdown('</div>', unsafe_allow_html=True)
    
    with st.spinner("Analyzing your outfit..."):
        rating, detected_style, comment = analyze_style(image)
    
    st.success("Analysis Complete!")
    st.markdown(f'<div class="rating-box">Rating: {rating}/10</div>', unsafe_allow_html=True)
    st.markdown(f"### Detected Style: {detected_style.capitalize()}")
    st.markdown(f'<div class="style-comment">"{comment}"</div>', unsafe_allow_html=True)
else:
    st.markdown('<button class="upload-btn">Drop your fit</button>', unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; font-size: 14px; color: #aaa;">
        © 2024 AI Powered Fashion Advisor| Your Wardrobe Elevated.
    </div>
    """,
    unsafe_allow_html=True
)
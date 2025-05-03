import streamlit as st
from PIL import Image
import os
from rembg import remove

# Streamlit page configuration
st.set_page_config(page_title="Your Digital Wardrobe", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Roboto:wght@300;400;500&display=swap');

        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f8f4f0;
            color: #000;
        }

        .title {
            font-family: 'Playfair Display', serif;
            font-size: 50px;
            text-align: center;
            color: #000;
            margin-bottom: 40px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .button-container {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 40px;
        }

        .stButton>button {
            font-family: 'Playfair Display', serif;
            background-color: #f2ede9;
            color: #000;
            border: 2px solid #000;
            padding: 10px 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 16px;
        }

        .stButton>button:hover {
            background-color: #000;
            color: #f2ede9;
        }

        .preview-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 300px;  /* Adjusted height */
            width: 300px;   /* Adjusted width */
            border: 2px solid #000;
            border-radius: 10px;
            background-color: #fff;
            text-align: center;
            color: #555;
            font-size: 18px;
        }

        .stImage>img {
            border: 2px solid #000;
            border-radius: 8px;
        }

        .divider {
            height: 2px;
            background-color: #000;
            margin: 30px 0;
        }
    </style>
""", unsafe_allow_html=True)

# Display the title
st.markdown("<div class='title'>Your Digital Wardrobe</div>", unsafe_allow_html=True)

# Function to remove background and save as PNG
def remove_background(image_path):
    output_path = image_path.replace(".jpg", "_bg_removed.png")
    if not os.path.exists(output_path):
        with open(image_path, "rb") as inp_file:
            img_data = inp_file.read()
            result = remove(img_data)
            with open(output_path, "wb") as out_file:
                out_file.write(result)
    return output_path

# Function to load and process images from a folder
def load_images(folder):
    processed_images = []
    if os.path.exists(folder):
        for file in os.listdir(folder):
            if file.endswith(".jpg"):
                image_path = os.path.join(folder, file)
                processed_path = remove_background(image_path)
                processed_images.append(processed_path)
    return processed_images

# Image categories based on your folder structure
categories = {
    "Tops": "tops",
    "Bottoms": "bottoms",
    "Accessories": "accessories",
    "Shoes": "shoes"
}

# State to track selected category and selected image
if "selected_category" not in st.session_state:
    st.session_state["selected_category"] = "Tops"

if "selected_image" not in st.session_state:
    st.session_state["selected_image"] = None

# Display category buttons
st.markdown("<div class='button-container'>", unsafe_allow_html=True)

col_buttons = st.columns(4)
for idx, category in enumerate(categories.keys()):
    if col_buttons[idx].button(category, key=category):
        st.session_state["selected_category"] = category

st.markdown("</div>", unsafe_allow_html=True)

# Load images based on the selected category
selected_category = st.session_state["selected_category"]
image_folder = categories[selected_category]
images = load_images(image_folder)

# Layout: Left section for preview, right section for image grid
col1, col2 = st.columns([1, 2])

# Left section: Image preview
with col1:
    if st.session_state["selected_image"]:
        st.image(
            st.session_state["selected_image"], 
            use_container_width=False,  # Set to False to allow custom sizing
            width=300  # Define a fixed width for the preview image
        )
    else:
        st.markdown(
            "<div class='preview-container'>"
            "🖼 Here's a preview! Select an image to view it here.</div>",
            unsafe_allow_html=True
        )

# Right section: Image grid
with col2:
    if images:
        st.markdown(f"### {selected_category}")
        cols_per_row = 3  # Number of images per row
        fixed_width = 150  # Set a fixed width for all images
        for i in range(0, len(images), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, img_path in enumerate(images[i:i + cols_per_row]):
                with cols[j]:
                    # When an image is clicked, update the selected image in session state
                    if st.button("Select", key=img_path):
                        st.session_state["selected_image"] = img_path
                    st.image(img_path, width=fixed_width)  # Display the image
    else:
        st.warning(f"No images found in '{image_folder}' folder.")

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
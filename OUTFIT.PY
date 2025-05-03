import streamlit as st
from PIL import Image
import torch
from torchvision import models, transforms
import requests

# Load ResNet model pre-trained on ImageNet
model = models.resnet50(pretrained=True)
model.eval()

# Image preprocessing function
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Function to fetch weather data
def get_weather_auto():
    try:
        location_data = requests.get("https://ipinfo.io").json()
        city = location_data.get("city", "Unknown")

        API_KEY = "c58e3897173f433927b2eb3cf4fd1e92"  # Replace with your API key
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        weather_data = requests.get(weather_url).json()
        return city, weather_data['main']['temp'], weather_data['weather'][0]['description']
    except Exception as e:
        st.error(f"Could not fetch weather: {e}")
        return "Unknown", None, None

# Streamlit App Styling
st.set_page_config(page_title="Outfit Recomendations", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Roboto:wght@300;500&display=swap');

        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f6f6f2;
            color: #222;
        }

        .title {
            font-family: 'Playfair Display', serif;
            font-size: 50px;
            text-align: center;
            color: #111;
            margin-bottom: 30px;
            text-transform: uppercase;
        }

        .subtitle {
            font-family: 'Playfair Display', serif;
            font-size: 24px;
            text-align: center;
            color: #555;
            margin-bottom: 15px;
            font-style: italic;
        }

        .info-text {
            font-size: 18px;
            text-align: center;
            margin-bottom: 20px;
            color: #333;
            background-color: #fefcf8;
            padding: 15px;
            border-radius: 8px;
        }

        .button-style {
            background-color: #111;
            color: #fff;
            padding: 14px;
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            border-radius: 5px;
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            border: none;
            display: inline-block;
        }

        .button-style:hover {
            transform: scale(1.05);
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        }

        .category-label {
            font-family: 'Playfair Display', serif;
            font-size: 20px;
            color: #111;
            text-transform: uppercase;
            margin: 10px 0;
        }

        .image-container {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }

        .image-container img {
            border: 2px solid #ccc;
            border-radius: 8px;
            border-radius:8px;
            height:auto;
        }

        .recommendation-box {
            background-color: #fff;
            color: #222;
            font-family: 'Roboto', sans-serif;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Display title and weather subtitle
city, temp, condition = get_weather_auto()
st.markdown("<div class='title'>Outfit Recomendations</div>", unsafe_allow_html=True)
if temp is not None:
    st.markdown(f"<div class='subtitle'>Weather in {city}: {temp}°C, {condition.capitalize()}</div>", unsafe_allow_html=True)

# Display weather-based message
if temp is not None:
    if temp < 10:
        st.markdown("<div class='info-text'>Ah, it's cold! Let's get you warm and cozy.</div>", unsafe_allow_html=True)
    elif 10 <= temp <= 20:
        st.markdown("<div class='info-text'>It's a bit chilly. Let's find something comfy and stylish.</div>", unsafe_allow_html=True)
    elif 20 < temp <= 30:
        st.markdown("<div class='info-text'>Nice weather! Let's pick something breezy and fashionable.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='info-text'>It's hot outside! Time for light and airy outfits.</div>", unsafe_allow_html=True)
else:
    st.warning("Could not fetch weather data. Default values will be used.")

# Categories for wardrobe items
categories = ["tops", "bottoms", "accessories", "shoes", "party_dress"]

# Create directories for each category if they don't exist
for category in categories:
    if not os.path.exists(category):
        os.makedirs(category)

# User input for occasion
st.markdown("---")
st.subheader("Where is miss headed?")
occasion = st.text_input("Type the occasion (e.g., Casual, Formal, Party, Outdoor, Gym)", placeholder="What's the vibe?")

# Generate outfit suggestions
st.markdown("---")
st.subheader("Personalize your look!")
if st.button("Generate my lookbook", key="suggest_outfit", help="Generate my lookbook"):
    all_categories_filled = all([len(os.listdir(category)) > 0 for category in categories])

    if all_categories_filled:
        selected_items = {}

        if occasion.lower() in ["party", "evening date", "date night"]:
            dress_path = random.choice(os.listdir("party_dress"))
            selected_items["Dress"] = os.path.join("party_dress", dress_path)

            shoes_path = random.choice(os.listdir("shoes"))
            selected_items["Shoes"] = os.path.join("shoes", shoes_path)

            accessory_path = random.choice(os.listdir("accessories"))
            selected_items["Accessories"] = os.path.join("accessories", accessory_path)

        elif occasion.lower() == "formal":
            top_path = random.choice(os.listdir("Women_f"))
            selected_items["Top"] = os.path.join("Women_f", top_path)

            bottom_path = random.choice(os.listdir("Women_for_pant"))
            selected_items["Bottom"] = os.path.join("Women_for_pant", bottom_path)

            shoes_path = random.choice(os.listdir("shoes"))
            selected_items["Shoes"] = os.path.join("shoes", shoes_path)

            accessory_path = random.choice(os.listdir("accessories"))
            selected_items["Accessories"] = os.path.join("accessories", accessory_path)

        else:
            for category in categories:
                if category in ["party_dress"]:
                    continue
                item_path = random.choice(os.listdir(category))
                selected_items[category.capitalize()] = os.path.join(category, item_path)

        st.subheader(f"You could wear'{occasion.capitalize()}':")
        for category, item_path in selected_items.items():
            st.markdown(f"<div class='category-label'>{category}:</div>", unsafe_allow_html=True)
            st.image(item_path, width=300)

        st.markdown("---")
        st.subheader("Ocassion")
        occasion_suggestions = {
            "casual": "Go for comfortable and relaxed outfits, like t-shirts and jeans.",
            "formal": "Choose a shirt or jacket with tailored pants and minimal accessories.",
            "party": "Bright or bold items with shiny accessories will work great!",
            "outdoor": "Opt for breathable tops, sturdy shoes, and protective accessories like caps.",
            "gym": "Sportswear like fitted tops, track pants, and sneakers are best."
        }
        st.markdown(f"<div class='recommendation-box'>{occasion_suggestions.get(occasion.lower(), 'Where you headed to?')}</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("Um wheathers like...")
        if temp is not None:
            weather_suggestion = ""
            if temp > 25:
                weather_suggestion = "☀ It's hot! Avoid heavy layers and go for light, breathable outfits."
            elif 15 < temp <= 25:
                weather_suggestion = "🌤 It's moderate. You can wear a light jacket or keep it casual."
            else:
                weather_suggestion = "❄ It's cold! Make sure to layer up and wear warm accessories."
            st.markdown(f"<div class='recommendation-box'>{weather_suggestion}</div>", unsafe_allow_html=True)
    else:
        st.warning("⚠ Please upload at least one item in each category to generate outfit suggestions.")
    st.markdown(
    """
    <div style="text-align: center; font-size: 14px; color: #aaa;">
        © 2024 AI Powered Fashion Advisor| Your Wardrobe Elevated.
    </div>
    """,
    unsafe_allow_html=True
)



import streamlit as st
from PIL import Image
import io

# Function to resize the image using JPEG (without changing quality, only resizing)
def resize_image(img, size_factor):
    # Ensure the image is in RGB mode before saving as JPEG
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize the image according to the size factor
    img_resized = img.resize((int(img.width * size_factor), int(img.height * size_factor)))
    img_byte_arr = io.BytesIO()
    img_resized.save(img_byte_arr, format='JPEG', quality=100, optimize=True)  # Keep quality the same as original
    img_byte_arr.seek(0)  # Rewind the buffer to the beginning
    return img_byte_arr

# Streamlit UI styling
st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: white;
    }
    .stButton>button {
        background-color: #008CBA;
        color: white;
    }
    .stDownloadButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .stText {
        color: #FFD700;
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit UI
st.title("Image Resizing App (Quality Remains Same)")

# File uploader to upload the image
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open the image
    img = Image.open(uploaded_file)
    
    # Show the uploaded image
    st.image(img, caption="Uploaded Image", use_container_width=True)
    
    # Calculate the original size of the uploaded file (in bytes)
    original_size = len(uploaded_file.getvalue())
    
    # Show sizes in KB and MB
    st.write(f"Original Image Size: {original_size / 1024:.2f} KB ({original_size / (1024 * 1024):.2f} MB)")

    # Store the original image size in session state
    st.session_state.original_size = original_size

    # Resize settings: Allow user to select a factor to increase or decrease the size
    st.subheader("Resize Settings")
    size_factor = st.slider("Resize Factor (1.0 = no change)", 0.5, 2.0, 1.0)  # 0.5 to 2x size scaling
    
    # Button to resize the image with the selected size factor
    if st.button("Resize the Image"):
        st.write(f"Resizing image with size factor: {size_factor}...")
        resized_image = resize_image(img, size_factor)
        
        # Get the size of the resized image
        resized_size = len(resized_image.getvalue())
        st.write(f"Resized Image Size: {resized_size / 1024:.2f} KB ({resized_size / (1024 * 1024):.2f} MB)")
        
        # Show the change in size
        size_change = (resized_size - original_size) / 1024
        st.write(f"Size Change: {size_change:.2f} KB ({size_change / 1024:.2f} MB)")
        
        # Display the resized image
        st.image(resized_image, caption="Resized Image", use_container_width=True)
        
        # Allow user to download the resized image
        st.download_button(
            label="Download Resized Image", 
            data=resized_image, 
            file_name="resized_image.jpg", 
            mime="image/jpeg"
        )

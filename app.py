# import qrcode
# data= input("Enter the url you want to generate QR code :-").strip()

# filename =input("Enter the file name:-").strip()

# qr= qrcode.QRCode(box_size=10,border=5)
# qr.add_data(data)
# image=qr.make_image(fill_color='black',back_color='white')
# image.save(filename)
# print(f"QR code generated successfully with the name {filename}")

import streamlit as st
import qrcode
from PIL import Image
import io

def generate_qr_code(url, fill_color='black', back_color='white', box_size=10, border=5):
    """
    Generate a QR code with customizable parameters
    """
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    
    # Add data
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create an image from the QR Code
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    return img

def main():
    # Set page configuration
    st.set_page_config(
        page_title="QR Code Generator",
        page_icon="🔲",
        layout="centered"
    )
    
    # Title and description
    st.title("🌐 QR Code Generator")
    st.write("Create custom QR codes with ease!")
    
    # Input section
    with st.form(key='qr_form'):
        # URL Input
        url = st.text_input(
            "Enter URL", 
            placeholder="https://www.example.com",
            help="Enter the website or text you want to convert to a QR code"
        )
        
        # Customization options
        col1, col2 = st.columns(2)
        with col1:
            fill_color = st.color_picker("QR Code Color", value='#000000')
        with col2:
            back_color = st.color_picker("Background Color", value='#FFFFFF')
        
        # Box size and border sliders
        col3, col4 = st.columns(2)
        with col3:
            box_size = st.slider("QR Code Size", min_value=5, max_value=20, value=10)
        with col4:
            border = st.slider("Border Size", min_value=1, max_value=10, value=5)
        
        # Submit button
        submit_button = st.form_submit_button("Generate QR Code")
    
    # Generation logic
    if submit_button:
        if url:
            try:
                # Generate QR Code
                qr_img = generate_qr_code(
                    url, 
                    fill_color=fill_color, 
                    back_color=back_color, 
                    box_size=box_size, 
                    border=border
                )
                
                # Convert PIL Image to bytes
                buffered = io.BytesIO()
                qr_img.save(buffered, format="PNG")
                img_byte = buffered.getvalue()
                
                # Display QR Code
                st.success("QR Code Generated Successfully!")
                st.image(img_byte, use_container_width=True)
                
                # Download Button
                st.download_button(
                    label="Download QR Code",
                    data=img_byte,
                    file_name=f"qr_code_{url.replace('https://', '').replace('http://', '').replace('.', '_')}.png",
                    mime="image/png"
                )
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a URL to generate QR Code")

# Run the app
if __name__ == "__main__":
    main()
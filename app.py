import streamlit as st
from PIL import Image, ImageDraw
import io
from rembg import remove, new_session

st.set_page_config(page_title="Studio Foto Vinted", page_icon="📸", layout="centered")

st.title("📸 Studio Foto per Vinted")

bg_options = ["Bianco", "Nero", "Grigio", "Campo Erba", "Mattone", "Trasparente"]

@st.cache_resource
def load_better_model():
    return new_session("u2net")

def create_background(size, style):
    width, height = size
    bg = Image.new("RGB", size, (255, 255, 255))
    draw = ImageDraw.Draw(bg)
    
    if style == "Bianco":
        return Image.new("RGB", size, (255, 255, 255))
    elif style == "Nero":
        return Image.new("RGB", size, (0, 0, 0))
    elif style == "Grigio":
        return Image.new("RGB", size, (128, 128, 128))
        
    elif style == "Campo Erba":
        # Sfondo verde base con effetto sfumato a righe stile campo da calcio
        bg = Image.new("RGB", size, (46, 125, 50))
        stripe_height = 80
        for y in range(0, height, stripe_height * 2):
            draw.rectangle([0, y, width, y + stripe_height], fill=(56, 142, 60))
            
    elif style == "Mattone":
        # Sfondo mattone con griglia dettagliata
        bg = Image.new("RGB", size, (140, 50, 35)) # Mattone scuro
        brick_h = 40
        brick_w = 100
        mortar_color = (200, 200, 200) # Fughe grigie
        
        # Disegna righe orizzontali delle fughe
        for y in range(0, height, brick_h):
            draw.line([(0, y), (width, y)], fill=mortar_color, width=4)
            
        # Disegna fughe verticali sfalsate
        for y_idx, y in enumerate(range(0, height, brick_h)):
            offset = (brick_w // 2) if (y_idx % 2 == 1) else 0
            for x in range(-offset, width, brick_w):
                draw.line([(x, y), (x, y + brick_h)], fill=mortar_color, width=4)
                
    return bg

uploaded_file = st.file_uploader("1. Carica foto", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Foto Originale", use_container_width=True)
    
    bg_style = st.selectbox("2. Scegli lo sfondo:", bg_options)
    
    if st.button("✨ Elabora Foto", type="primary", use_container_width=True):
        with st.spinner("Elaborazione..."):
            session = load_better_model()
            output_image = remove(image, session=session)
            
            if bg_style == "Trasparente":
                final_image = output_image.resize((1000, 1000))
                file_ext, mime = "PNG", "image/png"
            else:
                background = create_background((1200, 1200), bg_style)
                output_image.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
                paste_x = (1200 - output_image.width) // 2
                paste_y = (1200 - output_image.height) // 2
                background.paste(output_image, (paste_x, paste_y), output_image)
                final_image = background
                file_ext, mime = "JPEG", "image/jpeg"
            
            buffered = io.BytesIO()
            final_image.save(buffered, format=file_ext, quality=95)
            st.image(final_image, caption="Risultato", use_container_width=True)
            st.download_button("📥 Scarica Foto", buffered.getvalue(), f"foto.{file_ext.lower()}", mime, use_container_width=True)

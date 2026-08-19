import streamlit as st
from PIL import Image
import io
from rembg import remove, new_session

st.set_page_config(page_title="Studio Foto Vinted", page_icon="📸", layout="centered")

st.title("📸 Studio Foto per Vinted")

# Solo sfondi essenziali e puliti
bg_options = ["Bianco", "Nero", "Grigio", "Trasparente"]

@st.cache_resource
def load_better_model():
    return new_session("u2net")

def create_background(size, style):
    if style == "Bianco": return Image.new("RGB", size, (255, 255, 255))
    if style == "Nero": return Image.new("RGB", size, (0, 0, 0))
    if style == "Grigio": return Image.new("RGB", size, (128, 128, 128))
    return None

uploaded_file = st.file_uploader("1. Carica foto", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Foto Originale", use_container_width=True)
    
    bg_style = st.selectbox("2. Scegli lo sfondo:", bg_options)
    
    if st.button("✨ Elabora Foto", type="primary", use_container_width=True):
        with st.spinner("Elaborazione in corso..."):
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

import streamlit as st
from PIL import Image, ImageDraw
import io
from rembg import remove, new_session

st.set_page_config(page_title="Studio Foto Vinted", page_icon="📸", layout="centered")

st.title("📸 Studio Foto per Vinted")

# Sfondi con effetto naturale/studio
bg_options = ["Studio Luminoso (Bianco morbido)", "Grigio Neutro Moderno", "Nero Elegante", "Trasparente"]

@st.cache_resource
def load_stable_model():
    return new_session("u2net")

def create_gradient_background(size, style):
    width, height = size
    base_img = Image.new("RGB", size)
    draw = ImageDraw.Draw(base_img)
    
    if style == "Studio Luminoso (Bianco morbido)":
        # Sfumatura delicata dal bianco puro al grigio lunare molto chiaro (effetto studio)
        color_top = (255, 255, 255)
        color_bottom = (235, 238, 242)
    elif style == "Grigio Neutro Moderno":
        # Sfumatura grigia elegante, perfetta per far risaltare i vestiti
        color_top = (210, 215, 220)
        color_bottom = (150, 155, 162)
    elif style == "Nero Elegante":
        # Sfumatura scura per un look premium
        color_top = (45, 45, 50)
        color_bottom = (15, 15, 18)
    else:
        return None

    # Disegna la sfumatura riga per riga per un effetto morbido
    for y in range(height):
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * (y / height))
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * (y / height))
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
        
    return base_img

uploaded_file = st.file_uploader("1. Carica foto", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Foto Originale", use_container_width=True)
    
    bg_style = st.selectbox("2. Scegli lo sfondo naturale:", bg_options)
    
    if st.button("✨ Elabora Foto", type="primary", use_container_width=True):
        with st.spinner("Elaborazione in corso..."):
            image.thumbnail((1500, 1500))
            
            session = load_stable_model()
            output_image = remove(image, session=session)
            
            if bg_style == "Trasparente":
                final_image = output_image.resize((1000, 1000))
                file_ext, mime = "PNG", "image/png"
            else:
                background = create_gradient_background((1200, 1200), bg_style)
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

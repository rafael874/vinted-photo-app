import streamlit as st
from PIL import Image, ImageDraw, ImageFilter
import io
from rembg import remove, new_session

st.set_page_config(page_title="Studio Foto Vinted", page_icon="📸", layout="centered")

st.title("📸 Studio Foto per Vinted")

bg_options = ["Studio Luminoso", "Grigio Neutro", "Nero Naturale"]

@st.cache_resource
def load_stable_model():
    return new_session("u2net")

def create_depth_background(size, style):
    width, height = size
    bg = Image.new("RGB", size, (255, 255, 255))
    draw = ImageDraw.Draw(bg)
    
    # Tonalità molto più tenui e naturali, meno "sparate"
    if style == "Studio Luminoso":
        c1, c2 = (245, 246, 248), (215, 218, 222)  # Bianco panna / grigio carta da zucchero leggerissimo
    elif style == "Grigio Neutro":
        c1, c2 = (205, 208, 212), (160, 164, 170)  # Grigio caldo e morbido
    else: # Nero Naturale (grigio scuro antracite, non nero buio)
        c1, c2 = (75, 78, 85), (45, 48, 52)

    for i in range(width // 2):
        ratio = i / (width // 2)
        r = int(c1[0] + (c2[0] - c1[0]) * ratio)
        g = int(c1[1] + (c2[1] - c1[1]) * ratio)
        b = int(c1[2] + (c2[2] - c1[2]) * ratio)
        draw.ellipse([i, i, width-i, height-i], outline=(r, g, b))
    return bg

uploaded_file = st.file_uploader("1. Carica foto", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Foto Originale", use_container_width=True)
    
    bg_style = st.selectbox("2. Scegli lo sfondo:", bg_options)
    
    if st.button("✨ Elabora Foto", type="primary", use_container_width=True):
        with st.spinner("Elaborazione in corso..."):
            image.thumbnail((1500, 1500))
            session = load_stable_model()
            output_image = remove(image, session=session)
            
            background = create_depth_background((1200, 1200), bg_style)
            
            # Ombra più leggera e naturale sotto il vestito
            shadow = Image.new("RGBA", (1200, 1200), (0, 0, 0, 0))
            shadow_draw = ImageDraw.Draw(shadow)
            shadow_draw.ellipse([350, 920, 850, 1130], fill=(0, 0, 0, 40)) # Ombra più trasparente
            shadow = shadow.filter(ImageFilter.GaussianBlur(35))
            
            output_image.thumbnail((900, 900), Image.Resampling.LANCZOS)
            paste_x, paste_y = (1200 - output_image.width) // 2, (1200 - output_image.height) // 2
            
            background.paste(shadow, (0, 0), shadow)
            background.paste(output_image, (paste_x, paste_y - 40), output_image)
            
            buffered = io.BytesIO()
            background.save(buffered, format="JPEG", quality=95)
            
            st.image(background, caption="Risultato Naturale", use_container_width=True)
            st.download_button("📥 Scarica Foto", buffered.getvalue(), "foto_vinted.jpg", "image/jpeg", use_container_width=True)

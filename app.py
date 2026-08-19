import streamlit as st
from PIL import Image, ImageDraw
import io
from rembg import remove, new_session

st.set_page_config(page_title="Studio Foto Vinted", page_icon="📸", layout="centered")

st.title("📸 Studio Foto per Vinted")

bg_options = ["Bianco Professionale", "Grigio Neutro", "Nero Naturale"]

@st.cache_resource
def load_stable_model():
    return new_session("u2net")

def create_natural_background(size, style):
    width, height = size
    bg = Image.new("RGB", size)
    draw = ImageDraw.Draw(bg)
    
    # Tonalità morbide e opache (sfumatura verticale realistica)
    if style == "Bianco Professionale":
        color_top = (248, 249, 250)
        color_bottom = (218, 222, 226)
    elif style == "Grigio Neutro":
        color_top = (210, 213, 218)
        color_bottom = (155, 159, 165)
    else: # Nero Naturale (Antracite opaco)
        color_top = (70, 73, 80)
        color_bottom = (35, 38, 42)

    # Sfumatura verticale riga per riga (stile parete di studio)
    for y in range(height):
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * (y / height))
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * (y / height))
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
        
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
            
            # 1. Crea lo sfondo con sfumatura naturale verticale
            background = create_natural_background((1200, 1200), bg_style)
            
            # 2. Ridimensiona e posiziona perfettamente al centro
            output_image.thumbnail((900, 900), Image.Resampling.LANCZOS)
            paste_x = (1200 - output_image.width) // 2
            paste_y = (1200 - output_image.height) // 2
            
            background.paste(output_image, (paste_x, paste_y), output_image)
            
            buffered = io.BytesIO()
            background.save(buffered, format="JPEG", quality=95)
            
            st.image(background, caption="Risultato Pulito e Centrato", use_container_width=True)
            st.download_button("📥 Scarica Foto", buffered.getvalue(), "foto_vinted.jpg", "image/jpeg", use_container_width=True)

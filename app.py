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
    
    if style == "Bianco Professionale":
        color_top = (248, 249, 250)
        color_bottom = (218, 222, 226)
    elif style == "Grigio Neutro":
        color_top = (210, 213, 218)
        color_bottom = (155, 159, 165)
    else: 
        color_top = (70, 73, 80)
        color_bottom = (35, 38, 42)

    for y in range(height):
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * (y / height))
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * (y / height))
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
        
    return bg

uploaded_files = st.file_uploader("1. Carica foto (massimo 5 alla volta)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    if len(uploaded_files) > 5:
        st.warning("⚠️ Hai caricato più di 5 foto. Verranno elaborate solo le prime 5.")
        uploaded_files = uploaded_files[:5]
        
    bg_style = st.selectbox("2. Scegli lo sfondo per tutte le foto:", bg_options)
    
    if st.button("✨ Elabora Tutte le Foto", type="primary", use_container_width=True):
        with st.spinner("Elaborazione in corso..."):
            session = load_stable_model()
            
            for i, uploaded_file in enumerate(uploaded_files):
                image = Image.open(uploaded_file)
                image.thumbnail((1500, 1500))
                
                output_image = remove(image, session=session)
                
                background = create_natural_background((1200, 1200), bg_style)
                output_image.thumbnail((950, 950), Image.Resampling.BICUBIC)
                
                paste_x = (1200 - output_image.width) // 2
                paste_y = (1200 - output_image.height) // 2
                
                background.paste(output_image, (paste_x, paste_y), output_image)
                
                buffered = io.BytesIO()
                background.save(buffered, format="JPEG", quality=98)
                
                st.markdown(f"--- Foto {i+1} ---")
                st.image(background, caption=f"Risultato Foto {i+1}", use_container_width=True)
                st.download_button(
                    f"📥 Scarica Foto {i+1}", 
                    buffered.getvalue(), 
                    f"vinted_foto_{i+1}.jpg", 
                    "image/jpeg", 
                    key=f"download_{i}",
                    use_container_width=True
                )

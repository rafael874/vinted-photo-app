import os
import streamlit as st
from PIL import Image
import io
from rembg import remove, new_session

st.set_page_config(page_title="Studio Foto Vinted", page_icon="📸", layout="centered")

st.title("📸 Studio Foto per Vinted")
st.write("Carica la foto, scegli lo sfondo e scaricala pronta per la vendita!")

# Mapping colori
color_map = {
    "Bianco": (255, 255, 255),
    "Nero": (0, 0, 0),
    "Grigio Chiaro": (220, 220, 220),
    "Grigio Scuro": (100, 100, 100),
    "Trasparente": None
}

@st.cache_resource
def load_better_model():
    return new_session("u2net")

# 1. Prima cosa: Caricamento foto in evidenza
uploaded_file = st.file_uploader("1. Carica o scatta la foto", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Foto Originale", width='stretch')
    
    # 2. Seconda cosa: Scelta dello sfondo subito sotto
    st.markdown("---")
    bg_color_name = st.selectbox("2. Scegli il colore dello sfondo:", list(color_map.keys()))
    bg_color = color_map[bg_color_name]
    
    # 3. Terza cosa: Pulsante grande centrale
    st.markdown("---")
    if st.button("✨ Elabora e Ottimizza", type="primary", width='stretch'):
        with st.spinner("Elaborazione in corso..."):
            session = load_better_model()
            output_image = remove(image, session=session)
            
            target_size = (1200, 1200)
            
            if bg_color is None:
                final_image = output_image.resize((1000, 1000))
                file_ext = "PNG"
                mime_type = "image/png"
            else:
                background = Image.new("RGB", target_size, bg_color)
                output_image.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
                paste_x = (target_size[0] - output_image.width) // 2
                paste_y = (target_size[1] - output_image.height) // 2
                background.paste(output_image, (paste_x, paste_y), output_image)
                final_image = background
                file_ext = "JPEG"
                mime_type = "image/jpeg"
            
            buffered = io.BytesIO()
            final_image.save(buffered, format=file_ext, quality=95)
            img_bytes = buffered.getvalue()
            
            st.success("Fatto!")
            st.image(final_image, caption="Risultato Finale", width='stretch')
            
            st.download_button(
                label=f"📥 Scarica Foto ({bg_color_name})",
                data=img_bytes,
                file_name=f"vinted_foto.{file_ext.lower()}",
                mime=mime_type,
                width='stretch'
            )

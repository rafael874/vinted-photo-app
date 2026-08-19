import os
import streamlit as st
from PIL import Image
import io
from rembg import remove, new_session

st.set_page_config(page_title="Studio Foto Vinted", page_icon="📸", layout="centered")

st.title("📸 Studio Foto per Vinted & Co.")

# Mapping colori
color_map = {
    "Bianco": (255, 255, 255),
    "Nero": (0, 0, 0),
    "Grigio Chiaro": (220, 220, 220),
    "Grigio Scuro": (100, 100, 100),
    "Trasparente": None
}

# Sidebar per le impostazioni
with st.sidebar:
    st.header("Impostazioni")
    bg_color_name = st.selectbox("Scegli lo sfondo", list(color_map.keys()))
    bg_color = color_map[bg_color_name]

@st.cache_resource
def load_better_model():
    # Usiamo u2net, più preciso del precedente u2netp
    return new_session("u2net")

uploaded_file = st.file_uploader("Carica la foto del tuo prodotto", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Foto Originale", width=300)
    
    if st.button("Elabora Foto", type="primary"):
        with st.spinner("Ritaglio in corso..."):
            session = load_better_model()
            output_image = remove(image, session=session)
            
            # Creazione sfondo
            target_size = (1200, 1200)
            
            if bg_color is None:
                # Caso trasparente
                final_image = output_image.resize((1000, 1000))
                file_ext = "PNG"
                mime_type = "image/png"
            else:
                # Caso sfondo colorato
                background = Image.new("RGB", target_size, bg_color)
                output_image.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
                paste_x = (target_size[0] - output_image.width) // 2
                paste_y = (target_size[1] - output_image.height) // 2
                background.paste(output_image, (paste_x, paste_y), output_image)
                final_image = background
                file_ext = "JPEG"
                mime_type = "image/jpeg"
            
            # Salvataggio
            buffered = io.BytesIO()
            final_image.save(buffered, format=file_ext, quality=95)
            img_bytes = buffered.getvalue()
            
            st.success("Foto pronta!")
            st.image(final_image, caption="Risultato Finale", width=400)
            
            st.download_button(
                label=f"Scarica Foto ({bg_color_name})",
                data=img_bytes,
                file_name=f"vinted_foto.{file_ext.lower()}",
                mime=mime_type
            )

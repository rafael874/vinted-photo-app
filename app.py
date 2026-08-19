import streamlit as st
from PIL import Image
import io
from rembg import remove, new_session

st.set_page_config(page_title="Studio Foto Vinted", page_icon="📸", layout="centered")

st.title("📸 Studio Foto per Vinted & Co.")
st.write("Rimuovi lo sfondo e ottimizza le tue foto prodotto in un secondo (standard 1200x1200px con sfondo bianco).")

# Forziamo l'uso del modello u2netp (pesa solo pochi megabyte)
@st.cache_resource
def load_light_model():
    return new_session("u2netp")

uploaded_file = st.file_uploader("Carica la foto del tuo prodotto", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    st.subheader("Foto Originale")
    st.image(image, width='content')
    
    if st.button("Elabora e Ottimizza Foto", type="primary"):
        with st.spinner("Elaborazione in corso con modello leggero..."):
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
                
            # Chiamata sicura con sessione leggera
            session = load_light_model()
            output_image = remove(image, session=session)
            
            target_size = (1200, 1200)
            background = Image.new("RGB", target_size, (255, 255, 255))
            
            output_image.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
            
            paste_x = (target_size[0] - output_image.width) // 2
            paste_y = (target_size[1] - output_image.height) // 2
            
            background.paste(output_image, (paste_x, paste_y), output_image)
            
            buffered = io.BytesIO()
            background.save(buffered, format="JPEG", quality=95)
            img_bytes = buffered.getvalue()
            
            st.subheader("Risultato Pronto per la Vendita!")
            st.image(background, width='content')
            
            st.download_button(
                label="Scarica Foto Ottimizzata (1200x1200)",
                data=img_bytes,
                file_name="vinted_pro_foto.jpg",
                mime="image/jpeg"
            )

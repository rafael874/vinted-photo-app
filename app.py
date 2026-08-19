import streamlit as st
from PIL import Image
import io
from rembg import remove, new_session

st.set_page_config(page_title="Studio Foto Vinted", page_icon="📸", layout="centered")

st.title("📸 Studio Foto per Vinted & Co.")
st.write("Rimuovi lo sfondo e ottimizza le tue foto prodotto in un secondo (standard 1200x1200px con sfondo bianco).")

# Usiamo una sessione leggera per evitare sovraccarichi di memoria sul server gratuito
@st.cache_resource
def get_rembg_session():
    # Usiamo 'u2netp', una versione ultraleggera e veloce ideale per i piani gratuiti
    return new_session("u2netp")

uploaded_file = st.file_uploader("Carica la foto del tuo prodotto", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    st.subheader("Foto Originale")
    st.image(image, width='content')
    
    if st.button("Elabora e Ottimizza Foto", type="primary"):
        with st.spinner("Elaborazione in corso..."):
            # Conversione in RGB se necessario
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
                
            # Rimozione sfondo con la sessione leggera
            session = get_rembg_session()
            output_image = remove(image, session=session)
            
            # Creazione sfondo bianco 1200x1200px
            target_size = (1200, 1200)
            background = Image.new("RGB", target_size, (255, 255, 255))
            
            # Ridimensionamento proporzionale del prodotto per farlo entrare nel quadrato
            output_image.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
            
            # Centratura dell'immagine sullo sfondo bianco
            paste_x = (target_size[0] - output_image.width) // 2
            paste_y = (target_size[1] - output_image.height) // 2
            
            background.paste(output_image, (paste_x, paste_y), output_image)
            
            # Salvataggio in formato bytes per il download
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

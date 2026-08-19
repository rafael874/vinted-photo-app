import streamlit as st
import streamlit.components.v1 as components
from rembg import remove
from PIL import Image
import io

# Configurazione della pagina
st.set_page_config(page_title="Vinted Studio Photo Editor", page_icon="📸", layout="centered")

# --- 1. GOOGLE ANALYTICS ---
GA_TRACKING_ID = "G-F84MYBLZSG"
ga_js = f"""
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_TRACKING_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || '';
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_TRACKING_ID}');
</script>
"""
components.html(ga_js, height=0)

# --- 2. TITOLO E INTERFACCIA ---
st.title("📸 Vinted Studio Photo Editor")
st.write("Carica una foto per rimuovere lo sfondo automaticamente.")

uploaded_file = st.file_uploader("Scegli un'immagine", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Mostra l'immagine originale
    image = Image.open(uploaded_file)
    st.image(image, caption="Foto Originale", use_container_width=True)
    
    with st.spinner("Rimozione sfondo in corso..."):
        # Logica di rimozione sfondo
        input_image = image.convert("RGBA")
        output_image = remove(input_image)
        
        # Mostra il risultato
        st.image(output_image, caption="Foto senza sfondo", use_container_width=True)
        
        # Bottone di Download
        buf = io.BytesIO()
        output_image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="⬇️ Scarica foto pulita",
            data=byte_im,
            file_name="foto_vinted.png",
            mime="image/png",
            use_container_width=True
        )

    # --- 3. SEZIONE DONAZIONE IN EVIDENZA (Appare dopo l'elaborazione) ---
    st.markdown("---")
    st.subheader("☕ Ti è stato utile?")
    st.write("Se l'app ti ha aiutato a vendere su Vinted, offrimi un caffè per sostenere i costi del server!")
    st.link_button(
        "☕ Offrimi un caffè (PayPal)",
        "https://www.paypal.me/ContoAziendalePaypal",
        use_container_width=True,
    )

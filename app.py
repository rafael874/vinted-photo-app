import io
from PIL import Image
from rembg import remove
import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="Studio Foto Vinted", page_icon="📸", layout="centered"
)

st.title("📸 Studio Foto per Vinted & Co.")
st.write(
    "Carica la foto del tuo capo: l'app rimuoverà lo sfondo e la centrerà in un formato quadrato perfetto (1200x1200px) con sfondo bianco."
)

# Upload dell'immagine
uploaded_file = st.file_uploader(
    "Scegli un'immagine...", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    # Mostra l'immagine originale
    image = Image.open(uploaded_file)
    st.image(image, caption="Foto Originale", use_container_width=True)

    if st.button("Elabora e Ottimizza Foto", type="primary"):
        with st.spinner("Rimozione dello sfondo e ottimizzazione in corso..."):
            # Conversione in RGBA per gestire la trasparenza
            if image.mode in ("RGBA", "LA") or (
                image.mode == "P" and "transparency" in image.info
            ):
                image = image.convert("RGBA")
            else:
                image = image.convert("RGB").convert("RGBA")

            # 1. Rimuovi lo sfondo usando rembg
            output_image = remove(image)

            # 2. Crea uno sfondo bianco quadrato 1200x1200px
            target_size = (1200, 1200)
            background = Image.new("RGBA", target_size, (255, 255, 255, 255))

            # Ridimensiona l'immagine mantenendo le proporzioni
            output_image.thumbnail((1050, 1050), Image.Resampling.LANCZOS)

            # Calcola la posizione per centrarla
            offset_x = (target_size[0] - output_image.width) // 2
            offset_y = (target_size[1] - output_image.height) // 2

            # Incolla il capo sullo sfondo bianco
            background.paste(output_image, (offset_x, offset_y), output_image)

            # Converti in RGB per il salvataggio in JPG
            final_image = background.convert("RGB")

            # Salva l'immagine in un buffer
            buf = io.BytesIO()
            final_image.save(buf, format="JPEG", quality=95)
            byte_im = buf.getvalue()

        st.success("Fatto! La tua foto è pronta.")
        st.image(final_image, caption="Foto Ottimizzata e Centrata", use_container_width=True)

        # Pulsante per il download
        st.download_button(
            label="📥 Scarica Foto per Vinted",
            data=byte_im,
            file_name="foto_vinted_ottimizzata.jpg",
            mime="image/jpeg",
        )

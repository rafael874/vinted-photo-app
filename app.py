import io
from PIL import Image
import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="Vinted Studio Photo Editor", page_icon="📸", layout="centered"
)

# --- INTERFACCIA PRINCIPALE ---
st.title("📸 Vinted Studio Photo Editor")
st.write(
    "Rimuovi lo sfondo e crea foto perfette per i tuoi annunci su Vinted in"
    " pochi secondi."
)

uploaded_file = st.file_uploader(
    "Scegli un'immagine", type=["jpg", "jpeg", "png"]
)

# SEZIONE SCELTA SFONDO
bg_choice = st.selectbox(
    "Seleziona il colore dello sfondo:",
    [
        "Trasparente (PNG)",
        "Bianco Puro",
        "Grigio Neutro",
        "Beige / Carta da zucchero",
    ],
)

if uploaded_file is not None:
  # Mostra l'immagine originale
  image = Image.open(uploaded_file)
  st.image(image, caption="Foto Originale")

  if st.button("Rimuovi Sfondo"):
    with st.spinner(
        "Elaborazione in corso... (la prima volta potrebbe metterci qualche"
        " secondo)"
    ):
      try:
        from rembg import new_session, remove

        input_image = image.convert("RGBA")
        session = new_session("u2netp")
        output_image = remove(input_image, session=session)

        # --- CENTRATURA DELL'OGGETTO ---
        # Creiamo una tela vuota della stessa dimensione dell'originale
        # e incolliamo il soggetto tagliato esattamente al centro
        background_size = input_image.size
        
        # Scegliamo il colore dello sfondo in base alla scelta dell'utente
        if bg_choice == "Bianco Puro":
          bg_color = (255, 255, 255, 255)
        elif bg_choice == "Grigio Neutro":
          bg_color = (240, 240, 240, 255)
        elif bg_choice == "Beige / Carta da zucchero":
          bg_color = (245, 242, 238, 255)
        else:
          bg_color = (0, 0, 0, 0) # Trasparente

        # Creiamo il canvas dello sfondo
        final_background = Image.new("RGBA", background_size, bg_color)
        
        # Calcoliamo le coordinate per centrare l'oggetto
        paste_x = (background_size[0] - output_image.size[0]) // 2
        paste_y = (background_size[1] - output_image.size[1]) // 2
        
        # Incolliamo l'oggetto al centro
        final_background.paste(output_image, (paste_x, paste_y), output_image)

        # Finalizzazione del formato immagine
        if bg_choice == "Trasparente (PNG)":
          final_image = final_background
          file_format, file_extension, mime_type = "PNG", "png", "image/png"
        else:
          final_image = final_background.convert("RGB")
          file_format, file_extension, mime_type = "JPEG", "jpg", "image/jpeg"

        # Mostra il risultato
        st.image(final_image, caption=f"Foto elaborata e centrata ({bg_choice})")

        # Pulsante di Download
        buf = io.BytesIO()
        final_image.save(buf, format=file_format)
        st.download_button(
            label=f"⬇️ Scarica foto ({file_extension.upper()})",
            data=buf.getvalue(),
            file_name=f"vinted_studio.{file_extension}",
            mime=mime_type,
        )
      except Exception as e:
        st.error(f"Errore durante l'elaborazione dell'immagine: {e}")

# --- SEZIONE SUPPORTO ---
st.markdown("---")
st.subheader("☕ Ti è stato utile questo strumento?")
st.write(
    "Puoi offrire un caffè per sostenere i costi o contattarmi per"
    " bug/suggerimenti!"
)

col1, col2 = st.columns(2)
with col1:
  st.link_button(
      "☕ Offrimi un caffè (PayPal)",
      "https://www.paypal.me/ContoAziendalePaypal",
  )
with col2:
  st.link_button("✉️ Contattami", "mailto:tuaemail@example.com")

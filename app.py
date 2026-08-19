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
        "Caricamento motore IA ed elaborazione in corso (potrebbe volerci un"
        " attimo)..."
    ):
      # Importiamo rembg SOLO qui dentro, in modo che non si carichi all'avvio
      # evitando il crash immediato dell'applicazione.
      from rembg import new_session, remove

      input_image = image.convert("RGBA")
      session = new_session("u2netp")
      output_image = remove(input_image, session=session)

      # Gestione dei vari sfondi
      if bg_choice == "Bianco Puro":
        background = Image.new("RGBA", output_image.size, (255, 255, 255, 255))
        background.paste(output_image, (0, 0), output_image)
        final_image = background.convert("RGB")
        file_format, file_extension, mime_type = "JPEG", "jpg", "image/jpeg"
      elif bg_choice == "Grigio Neutro":
        background = Image.new("RGBA", output_image.size, (240, 240, 240, 255))
        background.paste(output_image, (0, 0), output_image)
        final_image = background.convert("RGB")
        file_format, file_extension, mime_type = "JPEG", "jpg", "image/jpeg"
      elif bg_choice == "Beige / Carta da zucchero":
        background = Image.new("RGBA", output_image.size, (245, 242, 238, 255))
        background.paste(output_image, (0, 0), output_image)
        final_image = background.convert("RGB")
        file_format, file_extension, mime_type = "JPEG", "jpg", "image/jpeg"
      else:  # Trasparente
        final_image = output_image
        file_format, file_extension, mime_type = "PNG", "png", "image/png"

      # Mostra il risultato
      st.image(final_image, caption=f"Foto elaborata ({bg_choice})")

      # Pulsante di Download
      buf = io.BytesIO()
      final_image.save(buf, format=file_format)
      st.download_button(
          label=f"⬇️ Scarica foto ({file_extension.upper()})",
          data=buf.getvalue(),
          file_name=f"vinted_studio.{file_extension}",
          mime=mime_type,
      )

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

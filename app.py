import io
from PIL import Image
from rembg import remove
import streamlit as st
import streamlit.components.v1 as components

# Configurazione della pagina
st.set_page_config(
    page_title="Vinted Studio Photo Editor", page_icon="📸", layout="centered"
)

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

# --- 2. INTERFACCIA PRINCIPALE ---
st.title("📸 Vinted Studio Photo Editor")
st.write(
    "Rimuovi lo sfondo e crea foto perfette per i tuoi annunci su Vinted in"
    " pochi secondi."
)

# Sidebar per le opzioni di personalizzazione dello sfondo
with st.sidebar:
  st.title("🎨 Personalizzazione")
  st.write("Scegli lo sfondo per la foto del tuo capo.")

  bg_choice = st.selectbox(
      "Colore dello sfondo",
      ["Trasparente (PNG)", "Bianco Puro", "Grigio Neutro", "Beige / Carta da zucchero"],
  )

uploaded_file = st.file_uploader(
    "Scegli un'immagine", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
  # Mostra l'immagine originale
  image = Image.open(uploaded_file)
  st.image(image, caption="Foto Originale", use_container_width=True)

  with st.spinner("Elaborazione e rimozione sfondo in corso..."):
    # Rimozione dello sfondo con rembg
    input_image = image.convert("RGBA")
    output_image = remove(input_image)

    # Gestione dei vari sfondi selezionabili
    if bg_choice == "Bianco Puro":
      background = Image.new("RGBA", output_image.size, (255, 255, 255, 255))
      background.paste(output_image, (0, 0), output_image)
      final_image = background.convert("RGB")
      file_format = "JPEG"
      file_extension = "jpg"
      mime_type = "image/jpeg"
    elif bg_choice == "Grigio Neutro":
      background = Image.new("RGBA", output_image.size, (240, 240, 240, 255))
      background.paste(output_image, (0, 0), output_image)
      final_image = background.convert("RGB")
      file_format = "JPEG"
      file_extension = "jpg"
      mime_type = "image/jpeg"
    elif bg_choice == "Beige / Carta da zucchero":
      background = Image.new("RGBA", output_image.size, (245, 242, 238, 255))
      background.paste(output_image, (0, 0), output_image)
      final_image = background.convert("RGB")
      file_format = "JPEG"
      file_extension = "jpg"
      mime_type = "image/jpeg"
    else:  # Trasparente
      final_image = output_image
      file_format = "PNG"
      file_extension = "png"
      mime_type = "image/png"

    # Mostra il risultato finale
    st.image(
        final_image,
        caption=f"Foto elaborata ({bg_choice})",
        use_container_width=True,
    )

    # Pulsante di Download
    buf = io.BytesIO()
    final_image.save(buf, format=file_format)
    byte_im = buf.getvalue()

    st.download_button(
        label=f"⬇️ Scarica foto ({file_extension.upper()})",
        data=byte_im,
        file_name=f"vinted_studio.{file_extension}",
        mime=mime_type,
        use_container_width=True,
    )

  # --- 3. SEZIONE SUPPORTO E CONTATTO (In evidenza) ---
  st.markdown("---")
  st.subheader("☕ Ti è stato utile questo strumento?")
  st.write(
      "Se l'app ti aiuta a velocizzare le vendite su Vinted, puoi offrire un"
      " caffè per sostenere i costi del server o contattarmi per suggerimenti!"
  )

  # Pulsante Donazione PayPal
  st.link_button(
      "☕ Offrimi un caffè (PayPal)",
      "https://www.paypal.me/ContoAziendalePaypal",
      use_container_width=True,
  )

  # Pulsante di Contatto (es. Email o Telegram - sostituisci con il tuo contatto)
  st.link_button(
      "✉️ Contattami / Segnala un bug",
      "mailto:tuaemail@example.com",  # Oppure metti il link al tuo Telegram es: "https://t.me/tuonome"
      use_container_width=True,
  )

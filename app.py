import streamlit as st
import streamlit.components.v1 as components

# Configurazione della pagina (deve essere sempre la prima chiamata Streamlit)
st.set_page_config(
    page_title="Vinted Studio Photo Editor",
    page_icon="📸",
    layout="centered",
)

# --- 1. CONFIGURAZIONE GOOGLE ANALYTICS ---
GA_TRACKING_ID = "G-F84MYBLZSG"

ga_js = f"""
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_TRACKING_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || '';
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_TRACKING_ID}');
</script>
"""

# Iniettiamo il codice di tracciamento (altezza 0 così non occupa spazio visivo)
components.html(ga_js, height=0)


# --- 2. BARRA LATERALE CON SEZIONE DONAZIONE ---
with st.sidebar:
  st.title("⚙️ Opzioni")
  st.write("Carica la foto del tuo capo per Vinted e rimuovi lo sfondo.")

  st.markdown("---")

  # Sezione Donazione / Supporto
  st.subheader("☕ Supporta il progetto")
  st.write(
      "Se questa app ti fa risparmiare tempo e ti aiuta a vendere di più su"
      " Vinted, offrimi un caffè per i costi del server!"
  )

  # Sostituisci il link qui sotto con il tuo link di Buy Me a Coffee, Ko-fi o PayPal
  st.link_button(
      "☕ Offrimi un caffè",
      "https://www.buymeacoffee.com/tuonome",
      use_container_width=True,
  )


# --- 3. CORPO PRINCIPALE DELL'APP ---
st.title("📸 Vinted Studio Photo Editor")
st.write("Benvenuto! Carica qui sotto l'immagine del tuo articolo.")

# Esempio di elemento di upload (puoi integrarlo con la tua logica di rembg / Pillow esistente)
uploaded_file = st.file_uploader(
    "Scegli un'immagine (JPG o PNG)", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
  st.success("Immagine caricata con successo!")
  # Qui sotto inserisci la logica con rembg e Pillow che hai già preparato

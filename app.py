import streamlit as st
import streamlit.components.v1 as components

# Configurazione della pagina
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
components.html(ga_js, height=0)


# --- 2. BARRA LATERALE (Solo per opzioni tecniche se servono) ---
with st.sidebar:
  st.title("⚙️ Info")
  st.write("App creata per velocizzare le vendite su Vinted.")


# --- 3. CORPO PRINCIPALE DELL'APP ---
st.title("📸 Vinted Studio Photo Editor")
st.write(
    "Benvenuto! Carica qui sotto l'immagine del tuo articolo per rimuovere lo"
    " sfondo."
)

# Esempio di upload file
uploaded_file = st.file_uploader(
    "Scegli un'immagine (JPG o PNG)", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
  st.success("Immagine caricata correttamente!")

  # --- QUI VA LA TUA LOGICA DI ELABORAZIONE (rembg / Pillow) ---
  # E finta per l'esempio, ma qui sotto mostreresti l'immagine pronta

  st.info(
      "✨ La tua foto è pronta! (Inserisci qui sotto il tuo blocco di"
      " download)"
  )

  # --- SEZIONE DONAZIONE IN EVIDENZA NEL CORPO PRINCIPALE ---
  st.markdown("---")
  st.subheader("☕ Ti è stato utile questo strumento?")
  st.write(
      "Se l'app ti ha fatto risparmiare tempo e ti aiuta a vendere su Vinted,"
      " considera l'idea di offrire un caffè per sostenere i costi di"
      " gestione!"
  )

  st.link_button(
      "☕ Offrimi un caffè (PayPal)",
      "https://www.paypal.me/ContoAziendalePaypal",
      use_container_width=True,
  )

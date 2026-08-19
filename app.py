import streamlit as st
import streamlit.components.v1 as components

# Configurazione della pagina (deve essere sempre la prima istruzione Streamlit)
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

# Iniettiamo il codice di tracciamento (altezza 0 così non è visibile nella pagina)
components.html(ga_js, height=0)


# --- 2. BARRA LATERALE (SIDEBAR) ---
with st.sidebar:
  st.title("⚙️ Opzioni")
  st.write("Gestisci le foto dei tuoi capi per Vinted.")

  st.markdown("---")

  # Sezione Donazione / Supporto con il tuo link PayPal corretto
  st.subheader("☕ Supporta il progetto")
  st.write(
      "Se questa app ti aiuta a vendere più velocemente su Vinted, offrimi un"
      " caffè per sostenere i costi del server!"
  )

  st.link_button(
      "☕ Offrimi un caffè",
      "https://www.paypal.me/ContoAziendalePaypal",
      use_container_width=True,
  )


# --- 3. CORPO PRINCIPALE DELL'APP ---
st.title("📸 Vinted Studio Photo Editor")
st.write(
    "Benvenuto! Carica qui sotto l'immagine del tuo articolo per rimuovere lo"
    " sfondo."
)

# Esempio di upload file (puoi collegarlo alla tua logica con rembg / Pillow)
uploaded_file = st.file_uploader(
    "Scegli un'immagine (JPG o PNG)", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
  st.success("Immagine caricata correttamente!")
  # Qui inserisci il resto della tua logica per elaborare l'immagine con rembg

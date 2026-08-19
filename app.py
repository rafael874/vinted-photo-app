import streamlit as st
from PIL import Image, ImageDraw, ImageOps
import io
from rembg import remove, new_session

# Configurazione della pagina ottimizzata per dispositivi mobili
st.set_page_config(page_title="Studio Foto Vinted", page_icon="📸", layout="centered")

st.title("📸 Studio Foto per Vinted")
st.markdown("Rendi i tuoi capi professionali in un click. Carica le tue foto qui sotto.")

bg_options = ["Bianco Professionale", "Grigio Neutro", "Nero Naturale"]

@st.cache_resource
def load_stable_model():
    return new_session("u2net")

def create_natural_background(size, style):
    width, height = size
    bg = Image.new("RGB", size)
    draw = ImageDraw.Draw(bg)
    
    if style == "Bianco Professionale":
        color_top, color_bottom = (248, 249, 250), (218, 222, 226)
    elif style == "Grigio Neutro":
        color_top, color_bottom = (210, 213, 218), (155, 159, 165)
    else: # Nero Naturale
        color_top, color_bottom = (70, 73, 80), (35, 38, 42)

    for y in range(height):
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * (y / height))
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * (y / height))
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return bg

# Selettore file ottimizzato per aprire la galleria del telefono
uploaded_files = st.file_uploader(
    "1. Seleziona fino a 5 foto dal tuo rullino:", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True,
    help="Tocca qui per aprire la galleria del telefono e scegliere le foto."
)

if uploaded_files:
    if len(uploaded_files) > 5:
        st.warning("⚠️ Puoi caricare al massimo 5 foto alla volta.")
        uploaded_files = uploaded_files[:5]
        
    bg_style = st.selectbox("2. Scegli lo sfondo:", bg_options)
    
    if st.button("✨ Avvia Elaborazione", type="primary", use_container_width=True):
        progress_bar = st.progress(0)
        session = load_stable_model()
        
        for i, uploaded_file in enumerate(uploaded_files):
            try:
                # Caricamento e correzione automatica rotazione telefono
                image = Image.open(uploaded_file)
                image = ImageOps.exif_transpose(image)
                image.thumbnail((1500, 1500))
                
                # Rimozione sfondo nitida
                output_image = remove(image, session=session)
                
                # Creazione sfondo e posizionamento centrato
                background = create_natural_background((1200, 1200), bg_style)
                output_image.thumbnail((950, 950), Image.Resampling.BICUBIC)
                
                paste_x = (1200 - output_image.width) // 2
                paste_y = (1200 - output_image.height) // 2
                background.paste(output_image, (paste_x, paste_y), output_image)
                
                # Salvataggio in alta qualità
                buffered = io.BytesIO()
                background.save(buffered, format="JPEG", quality=95)
                
                # Anteprima e download puliti
                st.markdown(f"**Foto {i+1} completata**")
                st.image(background, use_container_width=True)
                st.download_button(
                    f"📥 Scarica Foto {i+1}", 
                    buffered.getvalue(), 
                    f"vinted_{i+1}.jpg", 
                    "image/jpeg", 
                    key=f"d_{i}", 
                    use_container_width=True
                )
                st.markdown("---")
                
            except Exception as e:
                st.error(f"Errore durante l'elaborazione della foto {i+1}: {e}")
            
            # Aggiornamento barra di avanzamento
            progress_bar.progress((i + 1) / len(uploaded_files))
            
        st.success("🎉 Tutte le foto sono pronte per essere caricate su Vinted!")

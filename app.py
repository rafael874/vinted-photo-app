if st.button("Rimuovi Sfondo"):
    with st.spinner("Elaborazione in corso... (potrebbe metterci qualche secondo la prima volta)"):
      try:
        from rembg import new_session, remove
        
        input_image = image.convert("RGBA")
        # Inizializziamo la sessione con gestione errori
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
      except Exception as e:
        st.error(f"Errore durante l'elaborazione dell'immagine: {e}")

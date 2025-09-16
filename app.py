import streamlit as st
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip
import os
import uuid

def main():
    st.set_page_config(page_title="Gerador de Vídeos com IA", layout="centered")
    st.title("🎬 IA Criadora de Vídeos")
    st.write("Digite seu texto, escolha a duração e gere seu vídeo automaticamente!")

    texto = st.text_area("📝 Texto do vídeo", placeholder="Ex: Crie um vídeo motivacional sobre superação...")
    duracao = st.slider("⏱️ Duração do vídeo (em segundos)", min_value=5, max_value=120, value=30, step=1)
    imagem_file = st.file_uploader("📸 Escolha uma imagem de fundo (opcional)", type=["jpg", "jpeg", "png"])

    if st.button("🚀 Gerar vídeo"):
        if not texto.strip():
            st.error("Por favor, insira um texto para gerar o vídeo.")
            return

        st.info("Gerando narração...")
        audio_id = str(uuid.uuid4())
        audio_path = f"temp_{audio_id}.mp3"

        tts = gTTS(text=texto, lang='pt-br')
        tts.save(audio_path)

        if imagem_file is not None:
            imagem_path = f"temp_{audio_id}.jpg"
            with open(imagem_path, "wb") as f:
                f.write(imagem_file.read())
        else:
            imagem_path = "fundo.jpg"

        audio_clip = AudioFileClip(audio_path)

        if audio_clip.duration > duracao:
            audio_clip = audio_clip.subclip(0, duracao)
            final_duration = duracao
        else:
            final_duration = audio_clip.duration

        imagem_clip = ImageClip(imagem_path).set_duration(final_duration).set_audio(audio_clip)
        imagem_clip = imagem_clip.resize(height=720)

        video_path = f"temp_{audio_id}_video.mp4"
        imagem_clip.write_videofile(video_path, fps=24, codec="libx264", audio_codec="aac", verbose=False, logger=None)

        st.success("✅ Vídeo gerado com sucesso!")
        st.video(video_path)

        with open(video_path, "rb") as file:
            st.download_button("⬇️ Baixar vídeo", file, file_name="video_gerado.mp4", mime="video/mp4")

        try:
            os.remove(audio_path)
            if imagem_file is not None:
                os.remove(imagem_path)
            os.remove(video_path)
        except Exception as e:
            st.warning(f"Não foi possível remover alguns arquivos temporários: {e}")

if __name__ == "__main__":
    main()

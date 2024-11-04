import pygame
import threading
from gtts import gTTS
from io import BytesIO

class AudioPlayer:
    """gTTSを使用して説明を音声で読み上げるクラス"""

    def play_audio(self, description):
        """指定された説明を音声でMP3形式で再生"""
        try:
            # MP3形式で音声データを生成
            tts = gTTS(description, lang="ja")
            audio_stream = BytesIO()
            tts.write_to_fp(audio_stream)
            audio_stream.seek(0)
            
            # MP3データをpygameで再生
            pygame.mixer.init()
            pygame.mixer.music.load(audio_stream, "mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue
        except Exception as e:
            print(f"音声出力エラー: {e}")

    def speak_description(self, description):
        """音声再生を別スレッドで実行"""
        threading.Thread(target=self.play_audio, args=(description,)).start()

    def stop_audio(self):
        """再生中の音声を停止"""
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

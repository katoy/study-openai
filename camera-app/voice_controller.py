import speech_recognition as sr

class VoiceController:
    """音声入力に基づきアクションを制御するクラス"""
    def __init__(self, device_index=0):  # 使用するデバイスインデックスを指定
        self.recognizer = sr.Recognizer()
        try:
            self.microphone = sr.Microphone(device_index=device_index)
        except IOError:
            print("指定したデバイスインデックスでマイクが見つかりませんでした。音声コマンドを無効化します。")
            self.microphone = None

    def listen_for_command(self):
        """音声コマンドを待機して認識。マイクが認識できなければ無効化"""
        if self.microphone is None:
            print("音声コマンドは無効です。")
            return None

        try:
            with self.microphone as source:
                print("音声コマンドを待機中...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)

            try:
                command = self.recognizer.recognize_google(audio, language="ja-JP")
                print(f"認識した音声コマンド: {command}")
                return command
            except sr.UnknownValueError:
                print("音声を認識できませんでした。")
            except sr.RequestError as e:
                print(f"音声認識エラー: {e}")
        except AssertionError as e:
            print(f"音声入力デバイスに関するエラー: {e}")
        except AttributeError as e:
            print("音声入力デバイスの初期化に失敗しました。マイクが接続されているか確認してください。")
        return None

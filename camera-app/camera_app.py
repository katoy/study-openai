"""
このプログラムは、Raspberry Pi 上でカメラ映像から物体を検出し、検出結果に基づいた説明を生成し、
音声で読み上げる機能を提供します。また、キーボードおよび音声による操作が可能です。

主な機能:
1. カメラ映像から物体検出: YOLO モデルを使用して、カメラ映像から物体を検出し、各物体に枠とラベルを描画します。
2. 検出結果の説明生成: OpenAI API を用いて、検出された物体についての説明文を生成します。
3. 音声出力: gTTS (Google Text-to-Speech) を使い、生成された説明を音声で読み上げます。
4. 操作方法:
   - キーボード:
     - SPACEキー: 検出された物体に関する説明を生成し、音声で読み上げます。
     - ESCキー: 音声の読み上げを停止します。
     - Qキー: 音声出力を中断し、プログラムを終了します。
   - 音声操作:
     - 「説明して」: 検出された物体に関する説明を生成し、音声で読み上げます。
     - 「停止して」: 音声の読み上げを停止します。
     - 「終了して」: 音声出力を中断し、プログラムを終了します。
"""

import cv2
from object_detector import ObjectDetector
from description_generator import DescriptionGenerator
from audio_player import AudioPlayer
from voice_controller import VoiceController

class CameraApp:
    """カメラ映像から物体を検出し、説明文を生成して読み上げるメインアプリケーションクラス"""

    def __init__(self):
        self.detector = ObjectDetector()
        self.generator = DescriptionGenerator()
        self.audio_player = AudioPlayer()
        self.voice_controller = VoiceController()
        self.cap = cv2.VideoCapture(0)
        # 音声コマンドが有効かどうかをフラグで管理
        self.voice_command_enabled = self.voice_controller.microphone is not None
        if not self.voice_command_enabled:
            print("音声コマンドは無効です。マイクが認識されていません。")

    def process_voice_command(self, command):
        """音声コマンドに基づき操作を実行"""
        if command == "説明して":
            self.process_description_request()
        elif command == "停止して":
            print("音声を停止します...")
            self.audio_player.stop_audio()
        elif command == "終了して":
            print("音声出力を中断してプログラムを終了します...")
            self.audio_player.stop_audio()
            self.cleanup()

    def process_description_request(self):
        """説明を生成し、音声で読み上げる処理"""
        ret, frame = self.cap.read()
        if not ret:
            print("フレームをキャプチャできませんでした。")
            return

        detections = self.detector.detect_objects(frame)
        if detections:
            description = self.generator.generate_description(detections)
            print("AIからの説明:", description)  # ターミナルに説明を表示
            self.audio_player.speak_description(description)
        else:
            print("オブジェクトが検出されませんでした。")

    def cleanup(self):
        """リソースを解放してプログラムを終了"""
        self.cap.release()
        self.audio_player.stop_audio()  # プログラム終了前に音声を停止
        cv2.destroyAllWindows()

    def run(self):
        """メインループ"""
        if not self.cap.isOpened():
            print("カメラにアクセスできません。カメラデバイス番号を確認してください。")
            return

        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("フレームをキャプチャできませんでした。")
                    break

                detections = self.detector.detect_objects(frame)
                self.detector.draw_boxes(frame, detections)
                cv2.imshow("USB Camera - YOLO Object Detection", frame)

                # キーボード操作の処理
                key = cv2.waitKey(10) & 0xFF
                if key == ord(' '):  # SPACEキー
                    print("SPACEキーが押されました。説明を生成します...")
                    self.process_description_request()
                elif key == 27:  # ESCキー
                    print("ESCキーが押されました。音声を停止します...")
                    self.audio_player.stop_audio()
                elif key == ord('q'):  # Qキー
                    print("Qキーが押されました。音声出力を中断し、プログラムを終了します...")
                    self.audio_player.stop_audio()
                    self.cleanup()
                    break

                # 音声コマンドが有効な場合のみ音声コマンドを処理
                if self.voice_command_enabled:
                    command = self.voice_controller.listen_for_command()
                    if command:
                        self.process_voice_command(command)

        finally:
            self.cleanup()

if __name__ == "__main__":
    app = CameraApp()
    app.run()

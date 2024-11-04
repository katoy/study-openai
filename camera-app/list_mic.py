import speech_recognition as sr

# 利用可能なマイクのリストを表示
for i, mic_name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"Microphone with index {i}: {mic_name}")

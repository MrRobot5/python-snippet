
"""
demo: 不断监听麦克风输入，并在检测到关键字"open"时打开默认浏览器

使用 speech_recognition 库来识别语音，并使用webbrowser库来打开浏览器。

离线语音识别
speech_recognition 库可以配合某些支持离线工作的引擎使用，如 CMU Sphinx（也称为 PocketSphinx）。
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pocketsphinx

pip install SpeechRecognition
pip install PyAudio
pip install vosk
pip install pocketsphinx

@since 2024年1月18日 18:18:26
"""
import json
from vosk import Model, KaldiRecognizer

import speech_recognition as sr
import webbrowser

# 初始化识别器
recognizer = sr.Recognizer()
model = Model(model_path="C:/Users/yangpan3/Downloads/vosk-model-small-cn-0.22")
rec = KaldiRecognizer(model, 44000)
rec.SetWords(True)
rec.SetPartialWords(True)

# 使用默认麦克风作为音频源
with sr.Microphone() as source:
    print("Listening for the keyword 'open'...")

    # 不断监听麦克风输入
    while True:
        try:
            # 调整识别器的噪声水平
            recognizer.adjust_for_ambient_noise(source, duration=1)

            print("listen...")
            # 监听一段时间（你可以根据需要调整duration的值）
            audio = recognizer.listen(source, timeout=5)
            print("listen done")
            audio_data = audio.get_wav_data()
            if rec.AcceptWaveform(audio_data):
                res = json.loads(rec.Result())
                print(res["text"])

        except Exception as e:
            # 其他错误
            print("An error occurred: {0}".format(e))

import pandas as pd
import azure.cognitiveservices.speech as speechsdk
import os

# Excelファイルの読み込み
file_path = 'python_sentence.xlsx'
df = pd.read_excel(file_path)

# 'sentence' 列から英文を取得
sentences = df['Sentence'].tolist()

# Azure Speechの設定
speech_key = "02672ae4422b4395bfe66e1868760f88"
service_region = "eastus"

def text_to_speech(text, index):
    #出力先フォルダを指定したつもりだけど実際はこのpython_ttsに保存されてしまう。まあいいか。
    #output_dir = os.path.expanduser("~/Desktop/python_tts_outputs")
    #os.makedirs(output_dir, exist_ok=True)
    output_dir = 'output_files'
    os.makedirs(output_dir, exist_ok=True)
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_voice_name = "en-US-ChristopherNeural"
    audio_config = speechsdk.audio.AudioOutputConfig(filename=f"{index+1}_sentence.mp3")

    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized for text [{index}]: {text}")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print(f"Error details: {cancellation_details.error_details}")

# 各英文を音声合成してMP3ファイルに保存
for index, sentence in enumerate(sentences):
    text_to_speech(sentence, index)

print("音声合成が完了しました。")

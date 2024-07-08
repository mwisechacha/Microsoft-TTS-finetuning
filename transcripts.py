import pandas as pd
import os
import requests
from moviepy.editor import VideoFileClip
import assemblyai as aai
import numpy as np




def transcribe_audio(file_path, assemblyai_api_key):

    file_path = os.path.join(os.getcwd(),file_path)
      

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_path)

    if transcript.status == aai.TranscriptStatus.error:
        print(transcript.error)
    else:
        return transcript.text


x = ["None","NaN","nan","N/A","n/a","na","NA","-",""]



def insert_wav_path_and_transcribe(excel_path, wav_files, assemblyai_api_key):
    df = pd.read_excel(excel_path)
    for i in range(len(df)):

        wav = df.iloc[i]

        try:
            #check if the record has not  been transcribed
            if isinstance(wav['text'],str):
                if wav['text'] in x:
                    # Verify file path
                    file_path = wav[".wav location"]
                    print(f"Chcking file path: {file_path}")
                    if os.path.exists(file_path):
                        print("File exists. Transcribing")
                        transcription = transcribe_audio(wav[".wav location"], assemblyai_api_key)
                        df.at[i, 'text'] = transcription if transcription else wav['text']
                    else:
                        print(f"File does not exist: {file_path}")
                else:
                    print("Already transcribed")
            if isinstance(wav['text'], float):
                if np.isnan(wav['text']):
                    # verify file path
                    file_path = wav[".wav location"]
                    print(f"Checking file path: {file_path}")
                    if os.path.exists(file_path):
                        print("File exists. Transcribing")
                        transcription = transcribe_audio(file_path, assemblyai_api_key)
                        df.at[i, 'text'] = transcription if transcription else wav['text']
                    else:
                        print(f"File does not exist: {file_path}")
        
        except Exception as e:
            print(e)
            continue

    df.to_csv("./dataset.csv", index=False)

assemblyai_api_key = "afeff34b67824cb9907783dc5d90f82e" 
wav_files = 'Voices'
insert_wav_path_and_transcribe('./Video_dataset.xlsx', wav_files, assemblyai_api_key)
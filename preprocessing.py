# converting mp4 videos to .wav format using moviepy library
from moviepy.editor import VideoFileClip
import pandas as pd
import speech_recognition as sr
import os

# def mp3_to_wav(video_path, output_path):
#     # extract directory path
#     wav_dir = os.path.dirname(output_path)

#     # create directory if it does not exist
#     if not os.path.exists(wav_dir):
#         os.makedirs(wav_dir)

#     video = VideoFileClip(video_path)
#     video.audio.write_audiofile(output_path)
#     return output_path

# convert all mp4 files in the directory to wav files and insert them in an excel file
def mp4_to_wav(input_dir, output_dir):
    # extract all files in the directory
    files = os.listdir(input_dir)
    # create a list to store the paths of the wav files
    wav_files = []
    for file in files:
        if file.endswith('.mp4'):
            name = file.split('.')[0]
            output_path = os.path.join(output_dir, name + '.wav')
            input_path = os.path.join(input_dir, file)

            # convert the mp4 file to wav file
            video = VideoFileClip(input_path)
            video.audio.write_audiofile(output_path)
            wav_files.append(output_path)

    return wav_files

wav_files = mp4_to_wav('Video', 'Voices')

# a function to place the .wav path in an existing excel file
def insert_wav_path(excel_path, wav_files):
    df = pd.read_excel(excel_path)

    # for wav_path in wav_files:
    #     wav_id = os.path.splitext(os.path.basename(wav_path))[0]

    #     row_index = df[df['File'] == wav_id].index
    #     if not row_index.empty:
    #         df.loc[row_index, '.wav location'] = wav_path
    #     else:
    #         df = df.append({'File': wav_id, '.wav location': wav_path}, ignore_index=True)

    for wav_path in wav_files:
        wav_id = os.path.splitext(os.path.basename(wav_path))[0]

        if wav_id in df['File'].values:
            row_index = df[df['File'] == wav_id].index
            df.loc[row_index, '.wav location'] = wav_path
        else:
            # Create a new DataFrame for the row to append
            new_row = pd.DataFrame({'File': [wav_id], '.wav location': [wav_path]})
            # Use pd.concat to append the new row
            df = pd.concat([df, new_row], ignore_index=True)

    df.to_excel(excel_path, index=False)

insert_wav_path('Video_dataset.xlsx', wav_files)


def generate_transcript(excel_path):
    df = pd.read_excel(excel_path)
    r = sr.Recognizer()
    for index, row in df.iterrows():
        if pd.isnull(row['text']):
            audio_path = row['.wav location']
            with sr.AudioFile(audio_path) as source:
                audio = r.record(source)
                try:
                    text = r.recognize_google(audio)
                    df.loc[index, 'text'] = text
                except sr.UnknownValueError:
                    print('Google Speech Recognition could not understand the audio')
                except sr.RequestError as e:
                    print('Could not request results from Google Speech Recognition service; {0}'.format(e))
    df.to_excel(excel_path, index=False)

generate_transcript('transcripts.xlsx')
# converting mp4 videos to .wav format using moviepy library
from moviepy.editor import VideoFileClip
import pandas as pd
import os
import assemblyai as aai
import requests


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


def insert_wav_path(excel_path, wav_files):
    df = pd.read_excel(excel_path)
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


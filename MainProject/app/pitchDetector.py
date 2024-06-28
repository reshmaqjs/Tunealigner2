import wave
import numpy as np
from scipy.fft import fft
import librosa

def detect_pitch(segment):
    # Calculate the Fast Fourier Transform (FFT)
    spectrum = fft(segment)

    # Calculate the frequency axis
    frame_rate = 44100  # Sample rate (can be adjusted accordingly)
    frequencies = np.fft.fftfreq(len(spectrum), d=1/frame_rate)

    # Find the index of the peak frequency
    peak_index = np.argmax(np.abs(spectrum))

    # Get the corresponding frequency (pitch)
    pitch = np.abs(frequencies[peak_index])

    return pitch 

def segment_audio_and_detect_pitch(y,sr):
    
    # Detect onsets
    onsets = librosa.onset.onset_detect(y=y, sr=sr)
    onset_times = librosa.frames_to_time(onsets, sr=sr)
    sampleSize=len(y)
    duration=librosa.get_duration(y=y, sr=sr)
    actual_onset_Times=[]
    # Segment audio at onsets and calculate pitch for each segment
    onsets=[]
    for i in onset_times:
        frame=int(sampleSize*i/duration)
        onsets.append(frame)
        
    segment_pitches = []
    k=0
    for i in range(len(onsets)):
        if (onset_times[i] > onset_times[k]+0.25) or i==0:         
            start_sample = 0 if i == 0 else onsets[i]
            end_sample = int((len(y)+onsets[i])/2) if i == len(onsets) - 1 else onsets[i+1]
            segment = y[start_sample:end_sample]
            pitch = detect_pitch(segment)
            segment_pitches.append(int(pitch))
            actual_onset_Times.append(onset_times[i])
            k=i
         
    return actual_onset_Times, segment_pitches,duration
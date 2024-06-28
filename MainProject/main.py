from flask import Flask, render_template, request,  session, send_from_directory, url_for, Response
from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField
from werkzeug.utils import secure_filename
import shutil
import os
import pyaudio
import uuid
import threading
import subprocess
from wtforms.validators import InputRequired
from flask_wtf.file import FileAllowed
import wave
import numpy as np
from scipy.fft import fft
import librosa
from app.getNoteTimeSequence import Make_Note_Time_Sequence
from app.pitchDetector import segment_audio_and_detect_pitch 
from app.SequenceAligner import AlignBest
app =Flask(__name__)
app.config['SECRET_KEY']='supersecretkey'
app.config['UPLOAD_FOLDER']='static/files'

# Configuration for audio recording
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
OUTPUT_DIR = 'recordings'
OUTPUT_DIR2 = 'templates/audios'

# Create output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Initialize PyAudio
audio = pyaudio.PyAudio()


# Global variable to track recording state
refrecflag=""
testrecflag=""
recording = False
stream = None
frames = []

def start_recording(filename):
    global recording, stream, frames
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    frames = []

    print("Recording...")

    while recording:
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    savereftoaudio()
    savetesttoaudio()
@app.route('/recordtest') #, methods=['POST']
def recordtest():
    global recording
    filename = os.path.join(OUTPUT_DIR, 'test.wav')
    recording = True
    threading.Thread(target=start_recording, args=(filename,)).start()
    return filename
@app.route('/recordref') #, methods=['POST']
def recordref():
    global recording
    filename = os.path.join(OUTPUT_DIR, 'ref.wav')
    recording = True
    threading.Thread(target=start_recording, args=(filename,)).start()
    return filename


@app.route('/stop')
def stop():
    global recording
    recording = False
    return 'Recording stopped.'

@app.route('/savereftoaudio')
def savereftoaudio():
    try:
        # Copy the file 
        a1="./recordings/ref.wav"
        b1="./static/files/ref.wav"
        c1="./static/files/ref.mp3"
        a2="./static/files/refr1.wav"
        b2="./static/files/ref2.wav"
        c2= "./static/files/ref3.mp3"
        shutil.copyfile(a1,a2)
        shutil.copyfile(b1,b2)
        shutil.copyfile(c1,c2)
        print("trying")
        print("File copied successfully.")
    except Exception as e:
        print("Error:", e)
    return 'saved'

@app.route('/savetesttoaudio')
def savetesttoaudio():
    try:
        # Copy the file
        a1="./recordings/test.wav"
        b1="./static/files/test.wav"
        c1="./static/files/test.mp3"
        a2="./static/files/testr1.wav"
        b2="./static/files/test2.wav"
        c2= "./static/files/test3.mp3"
        shutil.copyfile(a1,a2)
        shutil.copyfile(b1,b2)
        shutil.copyfile(c1,c2)
        print("trying")
        print("File copied successfully.")
    except Exception as e:
        print("Error:", e)
    return 'saved'
    

class UploadFileForm(FlaskForm):
    file1=FileField("File",validators=[FileAllowed(['wav', 'mp3'],'Only WAV or MP3 files allowed.')],id="fil1")
    file2=FileField("File",validators=[FileAllowed(['wav', 'mp3'],'Only WAV or MP3 files allowed.')],id="fil2")
    submit_process = SubmitField("Process Files")
    submit=SubmitField("Evaluate",id="submit")

def mp3_to_wav(mp3_path):
    wav_path = os.path.splitext(mp3_path)[0] + '.wav'
    subprocess.call(['ffmpeg', '-i', mp3_path, wav_path])
    return wav_path


@app.route('/',methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])

def home():
    refFlag=0
    testFlag=0
    form=UploadFileForm()
    if request.method == 'POST':
        if 'submit' in request.form and request.form['submit'] == 'Evaluate':
           # if form.validate_on_submit():
           global refrecflag
           refrecflag = request.form.get('refname')
           refsrc="./static/files/refr1.wav"
           global testrecflag
           testrecflag = request.form.get('testname')
           testsrc="./static/files/testr1.wav"
           print( refrecflag," ",testrecflag)
           file1=form.file1.data
           if(file1.filename!=""):
               filename1 = secure_filename(file1.filename)
               if filename1.endswith('.mp3'):
                   filename1='ref.mp3'
                   refsrc="./static/files/ref3.mp3"
                   refFlag=1
               else:
                   filename1='ref.wav'
                   refsrc="./static/files/ref2.wav"
               file1.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(filename1)))
           file2=form.file2.data
           if(file2.filename!=""):
               filename2 = secure_filename(file2.filename)
               if filename2.endswith('.mp3'):
                   filename2='test.mp3'
                   testsrc="./static/files/test3.mp3"
                   testFlag=1
               else:
                   filename2='test.wav'
                   testsrc="./static/files/test2.wav"
               file2.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(filename2)))
           print(refFlag,",",testFlag)
           refseq,testseq,AlignedRefSeq,AlignedTestSeq,percentscore,timesref,timestest=evaluate(refFlag,testFlag)
           refalignNotes,testalinNotes=Findnotes(AlignedRefSeq,AlignedTestSeq)
           data = {'refsrc':refsrc,'testsrc':testsrc,'refseq': refseq, 'testseq': testseq,'AlignedRefSeq':AlignedRefSeq,'AlignedTestSeq':AlignedTestSeq,'refalignNotes':refalignNotes,'testalinNotes':testalinNotes,'percentscore':percentscore,'timesref':timesref,'timestest':timestest}
        #    return render_template('second.html',data=data)  
           savereftoaudio()
           savetesttoaudio()
           return render_template('second.html',data=data)
    data = {'refseq': "", 'testseq': "",'AlignedRefSeq':"",'AlignedTestSeq':"",'refalignNotes':"",'testalinNotes':"",'percentscore':""}  
    return render_template('index.html',form=form)
     
def Findnotes(aref,atest):
    a_refnote = [i[0]+str(i[1]) for i in aref]
    a_testnote= [ i[0]+str(i[1]) for i in atest]
    return a_refnote,a_testnote
def evaluate(rf,tf):
    print( refrecflag," ",testrecflag)
    audio_file_path_ref="ref.wav"
    audio_file_path_test="test.wav"
    if(rf==1):
        audio_file_path_ref='ref.mp3'
    if(tf==1):
        audio_file_path_test='test.mp3'
    
    # Load the audio file
    static_folder = os.path.join(os.path.dirname(__file__), 'static/files')
    file_path1 = os.path.join(static_folder, audio_file_path_ref)
    file_path2 = os.path.join(static_folder, audio_file_path_test)
#if latest is record then change audio_file_path_ref="ref.wav" and audio_file_path_test="test.wav"
    if (refrecflag == "record"):
        static_folder = os.path.join(os.path.dirname(__file__), 'recordings')
        file_path1 = os.path.join(static_folder,'ref.wav')
    if (testrecflag == "record"):
        static_folder = os.path.join(os.path.dirname(__file__), 'recordings')
        file_path2 = os.path.join(static_folder,'test.wav')
        print(file_path2)

    y1, sr1 = librosa.load(file_path1, sr=None)
    y2, sr2 = librosa.load(file_path2, sr=None)
    # y1 = librosa.effects.preemphasis(y1)
    # y1 = librosa.effects.preemphasis(y1)
    onsettime_ref,segment_pitches_ref,duration_ref = segment_audio_and_detect_pitch(y1,sr1)
    onsettime_test,segment_pitches_test,duration_test = segment_audio_and_detect_pitch(y2,sr2)

    print("\nOnset time sequence:", onsettime_ref)
    print("\nSegment pitch sequence:", segment_pitches_ref)

    print("\nOnset time sequence:", onsettime_test)
    print("\nSegment pitch sequence:", segment_pitches_test)
    note_time_sequence_ref=Make_Note_Time_Sequence(segment_pitches_ref,onsettime_ref,duration_ref)
    note_time_sequence_test=Make_Note_Time_Sequence(segment_pitches_test,onsettime_test,duration_test)
    print(" ")
    print(" ")
    print("\nnote_time_sequence_ref   ",note_time_sequence_ref)
    print("\nnote_time_sequence_test   ",note_time_sequence_test)
    print(" ")
    print(" ")
    ref_align_seq,test_align_seq,percentOfMatch=AlignBest(note_time_sequence_ref,note_time_sequence_test)
    return note_time_sequence_ref,note_time_sequence_test,ref_align_seq,test_align_seq,percentOfMatch,onsettime_ref,onsettime_test

if __name__=='__main__':
    app.run(
        host='127.0.0.1',
        port=5001,
        debug=True
    )
from math import log2
def FindNote(pitch_value):
    pitchVal=pitch_value
    note_names={
        0:'S',
        1:'R',
        2:'r',
        3:'G',
        4:'g',
        5:'M',
        6:'m',
        7:'P',
        8:'D',
        9:'d',
        10:'N',
        11:'n'
    }
    if(pitchVal==0):
        return "00"
    note_number=round(12*(log2(pitchVal)-log2(261))) % 12
    octave= 4 + (round(12*(log2(pitchVal)-log2(261))) // 12)
    return note_names[note_number]+str(octave)

def Make_Note_Time_Sequence(pitch_seq,time_seq,endTime):

    pitchSequence=pitch_seq
    timeSequence=time_seq
    aud_duration=endTime
    noteSeq=[]
    for i in pitchSequence:
        note=FindNote(i)
        noteSeq.append(note)
    not_time_seq=[]
    for i in range(len(noteSeq)):
        #dict={}
        li=[]
        if i==len(noteSeq)-1 :
            # dict={"note":noteSeq[i],"duration":aud_duration-timeSequence[i]}
            li=[noteSeq[i],aud_duration-timeSequence[i]]
        else:
            # dict={"note":noteSeq[i],"duration":timeSequence[i+1]-timeSequence[i]}
            li=[noteSeq[i],timeSequence[i+1]-timeSequence[i]]
        not_time_seq.append(li)

    return not_time_seq


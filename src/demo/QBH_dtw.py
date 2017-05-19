import os
import subprocess
import string

def wav2note(wavFilePath,wavFileName,txtFileName):
    """
    Extract note information from audio(.wav) file.
	The note information is outputed into txt file.
	Pitch extraction using autocorrelation method. Using Praat software.

    wavFilePath: Path of the audio file, e.g. 'audio/path/audio.wav'
    wavFileName: name of the audio file, e.g. 'audio.wav'
    txtFileName: Path of the output file, e.g. 'output/path/result.txt'
    """
    
    wavFileId = wavFileName[0:-4]
    PraatPath = '/Applications/Praat.app/Contents/MacOS/Praat'
    PraatScriptPath = '~/bishe/src/pitch_tracking_terminal_note.praat'

    subprocess.call([PraatPath,'--run',PraatScriptPath,wavFilePath, wavFileId, txtFileName])
    
    return;

def wav2pitch(wavFilePath,wavFileName,txtFileName):
    """
    Extract pitch information from audio(.wav) file.
    The note information is outputed into txt file.
    Pitch extraction using autocorrelation method. Using Praat software.

    wavFilePath: Path of the audio file, e.g. 'audio/path/audio.wav'
    wavFileName: name of the audio file, e.g. 'audio.wav'
    txtFileName: Path of the output file, e.g. 'output/path/result.txt'
    """
    
    wavFileId = wavFileName[0:-4]
    PraatPath = '/Applications/Praat.app/Contents/MacOS/Praat'
    PraatScriptPath = '~/bishe/src/pitch_tracking_terminal_pitch.praat'

    subprocess.call([PraatPath,'--run',PraatScriptPath,wavFilePath, wavFileId, txtFileName])
    
    return;

def readFile(txtFilePath):
    """
    Read from file and return a list.

    File format: numbers are seperated by line seperator
    """
    noteList = []

    f = open(txtFilePath,"r")
    while(True):
        line = f.readline()
        if line:
            line = line.strip('\n')
            noteList.append(line)
        else:
            break

    return noteList

def string2number(noteList):
    """
    Turn a string list into number list.

    The 'readFile' method gets a list containing string
    element. To further process the numbers, this 
    string2number method convert the strings into numbers.
    The '--undefined--' element in the noteList will be 
    converted into 0.
    
    noteList: a string list containing integers in string 
              format and '--undefined--'

    return a numberList containning positive integers and 0.

    """
    N = len(noteList)

    numberList = noteList

    for ii in xrange(N):
        if(noteList[ii] == "--undefined--"):
            numberList[ii] = 0
        else:
            numberList[ii] = string.atoi(noteList[ii])

    return numberList

def smooth(noteList):
    """ 
    To modify the unstable pitch of human humming
    
    Human can not produce a long and accurate pitch in 
    a certain time. The signal is not smooth. To make the
    signal smooth, we set a threshold time. If the signal
    did not last on one note for a 10ms, then remove
    it.

    noteList: a numeric list. Number '0' means nan

    return: smoothList

    """

    smoothList = noteList

    N = len(noteList)

    ii = 0
    while(ii<N):
        tempNote = smoothList[ii]

        for jj in range(1,N+1):
            if(ii+jj>(N-1)):
                break
            if(tempNote != smoothList[ii+jj]):
                break

        if(jj < 10):
            for kk in range(ii,ii+jj):
                smoothList[kk] = 0

        ii = ii + jj

        if(ii > N):
            break

    return smoothList

def inter4list(noteList):
    """
    
    Using nearest neighbor interpolation to deal with 
    the zeros in the sequence.

    noteList_withnan: a list containing positive and zeros
    
    return: return a list that contains no zero.(The old
    zero number will be replaced y interpolation)

    """

    # find valid(non-zero) position in humming sequence    

    N = len(noteList)
    validPos = []

    for ii in xrange(N):
        if(noteList[ii] == 0):
            continue
        validPos.append(ii)

    # find gap position in validPos
    N = len(validPos)
    gapPos_start = []
    for ii in xrange(N-1):
        if(validPos[ii+1] - validPos[ii] > 1):
            gapPos_start.append(validPos[ii])

    gapPos_end = []
    for ii in xrange(1,N):
        if(validPos[ii] - validPos[ii-1] > 1):
            gapPos_end.append(validPos[ii])

    # interpolation between these "0", 
    # using nearest nerghbor method
    N = len(gapPos_end)

    interpolationList = noteList

    for ii in xrange(N):
        interpolationList = near_interpolation(noteList, gapPos_start[ii],gapPos_end[ii])
    return interpolationList[validPos[0]:validPos[-1]]

def near_interpolation(seq, s, e):
    """
    function used in inter4list, an implementation for nearest neighbor
    interpolation method.

    seq: a list consist of integers
    s: start index of a subsequence that needs interpolated
    e: end index of a subsequence that needs interpolated

    return a interpolated sequence
    """
    seq_Inter = seq

    for ii in xrange(s,e+1):
        if(ii>(s+e)/2):
            seq_Inter[ii] = seq[e]
        else:
            seq_Inter[ii] = seq[s]
    
    return seq_Inter




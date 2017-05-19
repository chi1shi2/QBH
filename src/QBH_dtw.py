import os
import subprocess
import string
import mlpy
import numpy as np

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
    
    return

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
    
    return

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

    for ii in range(N):
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
        interpolationList = near_interpolation(interpolationList, gapPos_start[ii],gapPos_end[ii])

    # remove the zero element in interpolation list
    for each in interpolationList:
        if (each == 0):
            interpolationList.remove(0)
    return interpolationList

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

    for ii in range(s,e+1):
        if(ii>(s+e)/2):
            seq_Inter[ii] = seq[e]
        else:
            seq_Inter[ii] = seq[s]
    
    return seq_Inter

def getDtwScore_seq(template, evaluate):
    """
    return the score of dtw between template sequence and 
    sequence need to be evaluated

    input are sequences
    """
    res = mlpy.dtw_subsequence(evaluate, template)

    return res[0]

def getDtwScore_file(templateFile, evaluateFile):
    """
    return the score of dtw between template sequence and 
    sequence need to be evaluated

    input are files: 
    e.g. getDtwScore_file('input/path/a.txt','eva/path/b.txt')

    """

    # Get template list
    templateList = readFile(templateFile)
    templateList = string2number(templateList)

    # Get evaluate list
    noteList = readFile(evaluateFile)
    numberList = string2number(noteList)
    evaluateList = numberList

    return getDtwScore_seq(templateList,evaluateList)

def getSongString(number):
    """
    Give a number between 1-99, return the number as a five-digit string.
    e.g. 2 --> "00002"    14 --> "00014"
    """

    if ((number < 0) or (number > 99)):
        raise ValueError('input of getSongString must between 0 and 99!')
    if (number < 10):
        string = "0000" + str(number)
    elif (number > 9):
        string = "000" + str(number)

    return string

def txt_getDtwScoreList( H_noteSeq, T_noteSeqList ):
    """
    input a humming noteFile and output the dtw score list for all songs
    """

    # Get song list
    N = len(T_noteSeqList)
    songList = range(1, N + 1)

    # Get dtw score for each song
    scoreList = []
    N = len(T_noteSeqList)
    for ii in xrange(N):
        score = getDtwScore_seq(T_noteSeqList[ii],H_noteSeq)
        scoreList.append(score)

    return [scoreList,songList]

def getSeqList(pathDir):
    """
    Read the directory consist of .txt file
    The number in txt file: each line stores a number
    The function will return a list, each element is a list consisted of number stored in different txt file.

    :param pathDir: the directory that stores txt files
    :return: a list consists of note list
    """
    noteDir = pathDir

    noteFileList = os.listdir(noteDir)
    if '.DS_Store' in noteFileList:
        noteFileList.remove('.DS_Store')

    T_noteList = []  # T stands for 'template'
    for fileName in noteFileList:
        eachNoteDir = noteDir + fileName
        tempList = readFile(eachNoteDir)
        tempList = string2number(tempList)
        T_noteList.append(tempList)

    return T_noteList

#  ------ Evaluation Function Family ------
def getMostMatchedSong(scoreList,songList):

    sortedScore = sorted(scoreList)
    maxIndex = scoreList.index(sortedScore[0])
    return songList[maxIndex]

def getTop3MatchedSong(scoreList,songList):

    top3Song = []
    sortedScore = sorted(scoreList)

    # Get most matched song
    tempIndex = scoreList.index(sortedScore[0])
    top3Song.append(songList[tempIndex])

    # Get second matched song
    tempIndex = scoreList.index(sortedScore[1])
    top3Song.append(songList[tempIndex])

    # Get thired matched song
    tempIndex = scoreList.index(sortedScore[2])
    top3Song.append(songList[tempIndex])

    return top3Song

def getTop5MatchedSong(scoreList, songList):
    top3Song = []
    sortedScore = sorted(scoreList)

    # Get most matched song
    tempIndex = scoreList.index(sortedScore[0])
    top3Song.append(songList[tempIndex])

    # Get second matched song
    tempIndex = scoreList.index(sortedScore[1])
    top3Song.append(songList[tempIndex])

    # Get thired matched song
    tempIndex = scoreList.index(sortedScore[2])
    top3Song.append(songList[tempIndex])

    # Get 4th matched song
    tempIndex = scoreList.index(sortedScore[3])
    top3Song.append(songList[tempIndex])

    # Get 5th matched song
    tempIndex = scoreList.index(sortedScore[4])
    top3Song.append(songList[tempIndex])

    return top3Song

def getTxtEvaluated(H_noteFile, T_noteDir, songId, info):
    """
    for input txt humming note file, find whether it is in the most matched song and top3 top5 matched songs

    :param wavFile: wavFile that needs evaluated. e.g. './00029.txt'
    :param T_noteDir: Path of stored template note files
    :param songId: the song id of input humming song note
    :param info: if set True, then the function will print the most matched song and top3 top5 matched songs
    :return: no return value
    """
    # process the H_noteSeq
    H_noteSeq = readFile(H_noteFile)
    H_noteSeq = string2number(H_noteSeq)
    H_noteSeq = smooth(H_noteSeq)
    H_noteSeq = inter4list(H_noteSeq)

    # Get T_noteSeqList
    T_noteSeqList = getSeqList(T_noteDir)
    [scoreList, songList] = txt_getDtwScoreList( H_noteSeq, T_noteSeqList)

    # Get evaluated result
    top1 = getMostMatchedSong(scoreList, songList)
    top3 = getTop3MatchedSong(scoreList, songList)
    top5 = getTop5MatchedSong(scoreList, songList)

    res = [0,0,0]
    if top1 == songId:
        res[0] = 1
    if songId in top3:
        res[1] = 1
    if songId in top5:
        res[2] = 1

    # If info is True, then print the result
    if(info == True):
        print ("input song: " + str(songId))

        print ("mostMatched:")
        print top1

        print ("top3Matched:")
        print top3

        print ("top5Matched:")
        print top5

    return res

def getWavEvaluated(H_wavFile, T_noteDir):
    """

    :param H_wavFile: Humming wav file
    :param T_noteDir: Path of stored template note files
    :return:
    """

    return
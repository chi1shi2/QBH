import QBH_dtw as dtw
import os

total = 0
correct = [0,0,0]


#H_noteFile = '/Users/wangpeiguang/bishe/year2009/person00001/note/00001.txt'
T_noteDir = '/Users/wangpeiguang/bishe/noteFile/'

dataDir = '/Users/wangpeiguang/bishe/year2009/'
personList = os.listdir(dataDir)

if '.DS_Store' in personList:
    personList.remove('.DS_Store')

for eachPerson in personList:

    personDir = dataDir + eachPerson + '/note/'

    noteList = os.listdir(personDir)
    if '.DS_Store' in noteList:
        noteList.remove('.DS_Store')

    for eachNoteFile in noteList:
        H_noteFile = personDir + eachNoteFile
        songId = int(H_noteFile[-7:-4])
        result = dtw.getTxtEvaluated(H_noteFile,T_noteDir,songId,2)
        total = total + 1
        correct[0] = correct[0] + result[0]
        correct[1] = correct[1] + result[1]
        correct[2] = correct[2] + result[2]

print total
print correct

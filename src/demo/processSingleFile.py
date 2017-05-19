import QBH_dtw as dtw
import string

# Process a signle file
noteList = dtw.readFile('00029.txt')
numberList = dtw.string2number(noteList)
smoothList = dtw.smooth(numberList)
interList = dtw.inter4list(smoothList)

print(interList)


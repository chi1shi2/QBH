import string
import mlpy

# Read humming sequece
humming_seq = []

f = open("00029_humming.txt","r")
while 1:
	line = f.readline()
	if line:
		ts = string.atoi(line)
		humming_seq.append(ts)
	else:
		break

f.close()

# Read music note
music_seq = []

f = open("/Users/wangpeiguang/bishe/noteFile/00009.txt","r")
while 1:
	line = f.readline()
	if line:
		ts = string.atoi(line)
		music_seq.append(ts)
	else:
		break

f.close()

res = mlpy.dtw_subsequence(humming_seq, music_seq)

print(res[0])
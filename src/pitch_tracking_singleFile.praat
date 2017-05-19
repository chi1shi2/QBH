# This is the Script to list statistics of pitch
# Modified from Praat's Documents
# http://www.fon.hum.uva.nl/praat/manual/Script_for_listing_F0_statistics.html

selectObject: "Sound 00029"
To Pitch: 0.01,150,600 ; set the frame time to 0.01s, floor freq 150Hz, cell freq 600Hz

selectObject:"Pitch 00029"

startTime = Get start time
endTime = Get end time
frameTime = 0.01

deleteFile: "myfile.txt"

numberOfTimeSteps = (endTime - startTime) / frameTime
# writeInfoLine: " tmin tmax mean fmin fmax stdev"
for step to numberOfTimeSteps
    tmin = startTime + (step - 1) * frameTime
    tmax = tmin + frameTime
    mean = Get mean: tmin, tmax, "Hertz"
	note = 12 * log2(mean/440.0) + 69
    # appendInfoLine: fixed$ (tmin, 6), " ", fixed$ (tmax, 6), " ", fixed$ (mean, 2)
    appendFileLine: "myfile.txt",fixed$ (mean, 2)
endfor
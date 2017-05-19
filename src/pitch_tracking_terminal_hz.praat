
Read from file: fileName$

selectObject: "Sound " + fileId$
To Pitch: 0.01,150,600 

selectObject: "Pitch " + fileId$

startTime = Get start time
endTime = Get end time
frameTime = 0.01

deleteFile: txtfilePath$

numberOfTimeSteps = (endTime - startTime) / frameTime
# writeInfoLine: " tmin tmax mean fmin fmax stdev"
for step to numberOfTimeSteps
    tmin = startTime + (step - 1) * frameTime
    tmax = tmin + frameTime
    mean = Get mean: tmin, tmax, "Hertz"
	note = 12 * log2(mean/440.0) + 69
    # appendInfoLine: fixed$ (tmin, 6), " ", fixed$ (tmax, 6), " ", fixed$ (mean, 2)
    appendFileLine: txtfilePath$,fixed$(mean, 2)
endfor

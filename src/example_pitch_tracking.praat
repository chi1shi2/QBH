# Original script from Praat's Document

startTime = Get start time
endTime = Get end time
numberOfTimeSteps = (endTime - startTime) / 0.05
writeInfoLine: " tmin tmax mean fmin fmax stdev"
for step to numberOfTimeSteps
    tmin = startTime + (step - 1) * 0.05
    tmax = tmin + 0.05
    mean = Get mean: tmin, tmax, "Hertz"
    minimum = Get minimum: tmin, tmax, "Hertz", "Parabolic"
    maximum = Get maximum: tmin, tmax, "Hertz", "Parabolic"
    stdev = Get standard deviation: tmin, tmax, "Hertz"
    appendInfoLine: fixed$ (tmin, 6), " ", fixed$ (tmax, 6), " ", fixed$ (mean, 2),
    ... " ", fixed$ (minimum, 2), " ", fixed$ (maximum, 2), " ", fixed$ (stdev, 2)
endfor
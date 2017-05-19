%% plot MATALAB function
% after importing data song & humming

load('~/bishe/data/processing_humming_singleFile.mat')

%% plot the midi file and semitone

subplot(211);
plot(song);
title('MIDI file of 00029.midi');
ylabel('semitone');

subplot(212);
plot(humming);
title('Humming sequence extracted from pitch tracking method');
ylabel('semitone');

%% process the humming signal

figure(2)

humming_1 = humming;

N = length(humming_1);

ii = 1;
while(ii<N)
    tempNote = humming_1(ii);
    
    for jj = 1:N
        if(ii+jj>N)
            break;
        end
        if(tempNote ~= humming_1(ii + jj))
            break;
        end
    end
        
    if (jj < 10)
        for xx = ii:(ii+(jj-1))
            humming_1(xx) = NaN;
        end
    end
    
    ii = ii+jj;
    if(ii > N)
        break;
    end

end

% plot(humming_1);

subplot(311);
plot(song);
title('MIDI file of 00029.midi');
ylabel('semitone');

subplot(312);
plot(humming);
title('Humming Pitch Sequence (Before smoothing)');
ylabel('semitone');

subplot(313);
plot(humming_1);
title('Humming Pitch Sequence (After smoothing)');
ylabel('semitone');

%% find valid position in refined humming sequence
N = length(humming_1);

validPos = [];

for ii = 1:N
    if(isnan(humming_1(ii)))
        continue;
    end
    validPos = [validPos ii];
end

%% find gap position in validPos
N = length(validPos);

gapPos_start = [];
for ii = 1:(N-1)
    if(validPos(ii+1) - validPos(ii)>1)
        gapPos_start = [gapPos_start validPos(ii)];
    end
end

gapPos_end = [];
for ii = 2:N
    if(validPos(ii)-validPos(ii-1)>1)
        gapPos_end = [gapPos_end validPos(ii)];
    end
end

%% interpolation between these "nan", using Nearest Neighbour Interpolation
N = length(gapPos_end);

humming_Inter = humming_1;

for ii = 1:N
    humming_Inter = near_interpolation(humming_Inter,gapPos_start(ii),gapPos_end(ii));
end

subplot(211)
plot(humming_1)
title('????????????????')
xlabel('n')
ylabel('??')
subplot(212)
plot(humming_Inter)
title('??????????????')
xlabel('n')
ylabel('??')

%% Remove Nan
N = length(humming_Inter);

humming_processed = [];

for ii = 1:N
    if(isnan(humming_Inter(ii)))
        continue;
    else
        humming_processed= [humming_processed humming_Inter(ii)];
    end

end



%% Writing results into files
wf = fopen('00029.txt','w');

N = length(humming_processed);

for ii = 1:N
    fprintf(wf,num2str(humming_processed(ii)));
    fprintf(wf,'\n');
end

fclose(wf);



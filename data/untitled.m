%% plot MATALAB function
% after importing data song & humming

load('~/bishe/data/processing_humming_singleFile.mat')

subplot(211);
plot(song);
title('MIDI file of 00029.midi');
ylabel('semitone');

subplot(212);
plot(humming);
title('Humming sequence extracted from pitch tracking method');
ylabel('semitone');

%% process the humming signal
% ?????
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
subplot(211);
plot(song);
title('MIDI file of 00029.midi');
ylabel('semitone');

subplot(212);
plot(humming_1);
title('Humming sequence extracted from pitch tracking method');
ylabel('semitone');
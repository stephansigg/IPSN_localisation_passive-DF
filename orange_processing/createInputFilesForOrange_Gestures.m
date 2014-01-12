% create input files for orange


function [] = createInputFilesForOrange_Gestures(inputData)

%% Read contents of the directory-file
 
dataFile = fopen(inputData);
% Write the contents of the file into an array.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% New here: read in the output file and then later on extract the
%%% distinct blocks for which all the features will be calculated
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
data=textscan(dataFile,'%s%s%s%s');
fclose(dataFile);
%% Prepare outputfiles that contain all sample data
p=1; % this is the fraction defining how much of the data is written to training and how much is written to testing data set.

%% Write Features.txt
    EXFilenameFeaturesOverallOutAnn=strcat('Features_',num2str(p),'-annotated_[',inputData,'].tab');
    EXfileFeaturesOverallOutAnn = fopen(EXFilenameFeaturesOverallOutAnn,'w');
    EXFilenameFeaturesOverallOutNoAnn=strcat('Features_',num2str(1-p),'-NOTannotated_[',inputData,'].tab');
    EXfileFeaturesOverallOutNoAnn = fopen(EXFilenameFeaturesOverallOutNoAnn,'w');
%% Write header for annotated file:
    fprintf(EXfileFeaturesOverallOutAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n','mean','median','var','CM3','RMS','max','min','diff','count','dirChan','slope','slope2','mean2','diffMinMax','situation');
    fprintf(EXfileFeaturesOverallOutAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n','c','c','c','c','c','c','c','c','c','c','c','c','c','c','d');
    fprintf(EXfileFeaturesOverallOutAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','class');

%% Write header for non-annotated file:
    fprintf(EXfileFeaturesOverallOutNoAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n','mean','median','var','CM3','RMS','max','min','diff','count','dirChan','slope','slope2','mean2','diffMinMax','situation','groundtruth');
    fprintf(EXfileFeaturesOverallOutNoAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n','c','c','c','c','c','c','c','c','c','c','c','c','c','c','d','d');
    fprintf(EXfileFeaturesOverallOutNoAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','class');

    
%% now extract data from the file
[length breadth]=size(data{1,1});
% first, count the number of different recordings
counter=0;
for i=1:length 
    if (strcmp(data{1,1}{i,1}(1,1),'0'))
        counter=counter+1;
    end
end
%% Initialise container to hold the feature values
    meanValues = zeros(counter,1);
    varValues = zeros(counter,1);
    medianValues = zeros(counter,1);
    CM3Values = zeros(counter,1);
    RMSValues = zeros(counter,1);
    maxValues = zeros(counter,1);
    minValues = zeros(counter,1);
    diffValues = zeros(counter,1);
    slopeValues = zeros(counter,1);
    slopeValues2 = zeros(counter,1);
    meanValues2 = zeros(counter,1);
    diffMinMaxValues = zeros(counter,1);
    
    % #peaks with 10%<max
    countBetweenMaxValues = zeros(counter,1);
    % differenz aufeinanderfolgender Maxima
    directionChanges = zeros(counter,1);
    energyValues = zeros(counter,1);
    entropyValues = zeros(counter,1);
    averageFFTValues = zeros(counter,1);
    stdValues=zeros(counter,1);
    
% Now, for each recording, calculate all features
k=1;
for i=1:length
    if (strcmp(data{1,1}{i,1}(1,1),'0'))% found column right before the sampled data
        helperCounter=i;
        while (0==strcmp(data{1,1}{i,1}(1,1),'E'))
            %count legth of recording
            i=i+1;
        end
        dataArray=zeros(1,i-helperCounter-1);        
        % sample all data
        for dataArrayCounter=helperCounter+1:i-1
            dataArray(1,dataArrayCounter-helperCounter)=str2num(data{1,3}{dataArrayCounter,1}(1,:));
        end
        % hier nun die Berechnung der features
        meanValues(k,1)=mean(dataArray);
        varValues(k,1)=var(dataArray);
        medianValues(k,1)=median(dataArray);
        CM3Values(k,1)=moment(dataArray,3);
        RMSValues(k,1)=sqrt(varValues(k,1));%RMS=sqrt(var)
        maxValues(k,1)=max(dataArray);
        minValues(k,1)=min(dataArray);
        diffValues(k,1)=maxValues(k,1)-minValues(k,1);
        slopeHelper=zeros(2,i-helperCounter-1);
        for slopecounter=1:i-helperCounter-1
            slopeHelper(1,slopecounter)=slopecounter;
            slopeHelper(2,slopecounter)=dataArray(1,slopecounter);
        end
        slope=gradient(slopeHelper);
        slopeValues(k,1)= mean(slope(2,:));
        
        meanSlope1=mean(slope(2,1:floor((i-helperCounter-1)/2)));
        meanSlope2=mean(slope(2,floor((i-helperCounter-1)/2)+1:i-helperCounter-1));
        slopeValues2(k,1)= meanSlope1/meanSlope2;
        meanValues2(k,1)=mean(dataArray(1,1:floor((i-helperCounter-1)/2)))/mean(dataArray(1,floor((i-helperCounter-1)/2)+1:i-helperCounter-1));
        diffMinMaxValues(k,1)=maxValues(k,1)-minValues(k,1);
        count=0;
        previousMax=0;
        maxCounter=0;
        accumulatedMax=0;
        for counter=1:i-helperCounter-1
            if (dataArray(1,counter)>(0.9*maxValues(k,1)) || dataArray(1,counter) < (0.9*minValues(k,1)))
                count=count+1;
            end
            if (counter > 1 && counter < i-helperCounter-1) %shall not be applied for first and last value in the window
                if (dataArray(1,counter)>dataArray(1,counter-1)&&dataArray(1,counter)<dataArray(1,counter+1))%found new maximum
                    maxCounter=maxCounter+1;
                    accumulatedMax=accumulatedMax+(abs(dataArray(1,counter)-previousMax));
                    previousMax=dataArray(1,counter);
                    directionChanges(k,1)=directionChanges(k,1)+1;
                 end
                 if (dataArray(1,counter)<dataArray(1,counter-1)&&dataArray(1,counter)>dataArray(1,counter+1))%found new minimum
                     directionChanges(k,1)=directionChanges(k,1)+1;
                 end
             end
         end
         countBetweenMaxValues(k,1)=count;
         %calculate the normalised spectral energy
         fftArray=real(fft(dataArray));
         PeIi=0;
         for PeIiCounter=1:((i-helperCounter-1)/2)
             PeIi=PeIi+((fftArray(PeIiCounter)^2)/sum(fftArray(1,1:floor((i-helperCounter-1)/2))))^2;
         end
         energyValues(k,1)=PeIi;
         % calculate Entropy
         PeIiEnt=0;
         for PeIiEntCounter=1:((i-helperCounter-1)/2)
             PeIiEnt=PeIiEnt+(fftArray(PeIiEntCounter)^2)/sum(fftArray(1,1:floor((i-helperCounter-1)/2)))*log((fftArray(PeIiEntCounter)^2)/sum(fftArray(1,1:floor((i-helperCounter-1)/2))));
         end
         entropyValues(k,1)=PeIiEnt;
         % calculate DC component (this is the average of windowSize -> So,
         % is there any use for this? I could have an average of the
         % fftArray instead?
         averageFFTValues(k,1)=mean(fftArray);
         stdValues(k,1)=std(dataArray);
         k=k+1;
     end
end
    %% Write output files according to orange-syntax

% Syntax of the output file:
% No annotation:
%     rms1	snr1	avgmagsqr1	sit
%     c	c	c	d
% 			class
%     2542.14	13.9922	6033770.0	?
%     1748.28	15.736	3051700.0	?
%     
% Annotation:
%     rms1	snr1	avgmagsqr1	sit
%     c	c	c	d
% 			class
%     2542.14	13.9922	6033770.0	x
%     1748.28	15.736	3051700.0	y

%% TODO: calculate e.g. std from the values AVG(RMS) [mincount], amp(isa), sc, gsm_amp over some sample window and write this out to a file.
%       One question is, whether the window should be overlapping or not.
%       Also, the size of the window should be configurable
%       Probably do both? But then for the overlapping window, the value
%       would change only steadily over time
    
        for l=1:k-1
            if rand(1)<(p)     
                fprintf(EXfileFeaturesOverallOutAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n',num2str(meanValues(l,1)),num2str(medianValues(l,1)),num2str(varValues(l,1)),num2str(CM3Values(l,1)),num2str(RMSValues(l,1)),num2str(maxValues(l,1)),num2str(minValues(l,1)),num2str(diffValues(l,1)),num2str(countBetweenMaxValues(l,1)),num2str(directionChanges(l,1)),num2str(slopeValues(l,1)),num2str(slopeValues2(l,1)),num2str(meanValues2(l,1)),num2str(diffMinMaxValues(l,1)),'ADDCLASSNAME');
            else
                fprintf(EXfileFeaturesOverallOutNoAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n',num2str(meanValues(l,1)),num2str(medianValues(l,1)),num2str(varValues(l,1)),num2str(CM3Values(l,1)),num2str(RMSValues(l,1)),num2str(maxValues(l,1)),num2str(minValues(l,1)),num2str(diffValues(l,1)),num2str(countBetweenMaxValues(l,1)),num2str(directionChanges(l,1)),num2str(slopeValues(l,1)),num2str(slopeValues2(l,1)),num2str(meanValues2(l,1)),num2str(diffMinMaxValues(l,1)),'?','ADDCLASSNAME');
            end              
        end
        
        fclose(EXfileFeaturesOverallOutAnn);
        fclose(EXfileFeaturesOverallOutNoAnn);
end
   
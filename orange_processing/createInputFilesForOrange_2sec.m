% create input files for orange


function [] = createInputFilesForOrange_2sec(filenames)

%% Read contents of the directory-file
 
fileNames = fopen(filenames);
% Write the contents of the file into an array.
names=textscan(fileNames,'%s');
fclose(fileNames);
%% Go into each directory and extract data from the files isabell.txt, lisa.txt, isabell_rohdaten.txt and lisa_rohdaten.txt
[length breadth]=size(names{1,1});
%% Prepare outputfiles that contain all sample data
p=1; % this is the fraction defining how much of the data is written to training and how much is written to testing data set.

windowSize=20; % window size over which the standard deviation is build (1==0.05sec; 20=1sec)
% the samples have been taken with 70Hz -> 210==3 sec.

windowSizeTwoPassFirst=5;% window size for the 1st stage
windowSizeTwoPassSecond=4;% window size for the 2nd stage

%% Write Rohdaten.txt
    EXFilenameOverallOutAnn=strcat('WS1_raw_',num2str(p),'-annotated_[',filenames,'].tab');
    EXfileOverallOutAnn = fopen(EXFilenameOverallOutAnn,'w');
    EXFilenameOverallOutNoAnn=strcat('WS1_raw_',num2str(1-p),'-NOTannotated_[',filenames,'].tab');
    EXfileOverallOutNoAnn = fopen(EXFilenameOverallOutNoAnn,'w');
%% Write header for annotated file:
    fprintf(EXfileOverallOutAnn,'%s\t%s\n','raw','situation');
    fprintf(EXfileOverallOutAnn,'%s\t%s\n','c','d');
    fprintf(EXfileOverallOutAnn,'%s\t%s\n',' ','class');

%% Write header for non-annotated file:
    fprintf(EXfileOverallOutNoAnn,'%s\t%s\t%s\n','raw','situation','groundtruth');
    fprintf(EXfileOverallOutNoAnn,'%s\t%s\t%s\n','c','d','d');
    fprintf(EXfileOverallOutNoAnn,'%s\t%s\t%s\n',' ',' ','class');
    %% rohdaten with stdandardDeviation as preprocessing:

%% Write Features.txt
    EXFilenameFeaturesOverallOutAnn=strcat('WS',num2str(windowSize),'_Features_',num2str(p),'-annotated_[',filenames,'].tab');
    EXfileFeaturesOverallOutAnn = fopen(EXFilenameFeaturesOverallOutAnn,'w');
    EXFilenameFeaturesOverallOutNoAnn=strcat('WS',num2str(windowSize),'_Features_',num2str(1-p),'-NOTannotated_[',filenames,'].tab');
    EXfileFeaturesOverallOutNoAnn = fopen(EXFilenameFeaturesOverallOutNoAnn,'w');
%% Write header for annotated file:
    fprintf(EXfileFeaturesOverallOutAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n','mean','median','var','CM3','RMS','max','min','diff','count','diffMaxVal','dirChan','zeroCross','relDirChanZeroCross','distZeroCross','situation');
    fprintf(EXfileFeaturesOverallOutAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n','c','c','c','c','c','c','c','c','c','c','c','c','c','c','d');
    fprintf(EXfileFeaturesOverallOutAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','class');

%% Write header for non-annotated file:
    fprintf(EXfileFeaturesOverallOutNoAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n','mean','median','var','CM3','RMS','max','min','diff','count','diffMaxVal','dirChan','zeroCross','relDirChanZeroCross','distZeroCross','situation','groundtruth');
    fprintf(EXfileFeaturesOverallOutNoAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n','c','c','c','c','c','c','c','c','c','c','c','c','c','c','d','d');
    fprintf(EXfileFeaturesOverallOutNoAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','class');

     %% Write Features.txt for 1-pass and 2-pass files together
     EXFilenameFeaturesOverall1Pass2PassOutAnn=strcat('WS',num2str(windowSize),'_OnePassWS',num2str(windowSizeTwoPassFirst),'_TwoPassWS',num2str(windowSizeTwoPassSecond),'_Features_',num2str(p),'-annotated_[',filenames,'].tab');
     EXfileFeaturesOverall1Pass2PassOutAnn = fopen(EXFilenameFeaturesOverall1Pass2PassOutAnn,'w');
     EXFilenameFeaturesOverall1Pass2PassOutNoAnn=strcat('WS',num2str(windowSize),'_OnePassWS',num2str(windowSizeTwoPassFirst),'_TwoPassWS',num2str(windowSizeTwoPassSecond),'_Features_',num2str(1-p),'-NOTannotated_[',filenames,'].tab');
     EXfileFeaturesOverall1Pass2PassOutNoAnn = fopen(EXFilenameFeaturesOverall1Pass2PassOutNoAnn,'w');
 %% Write header for annotated file:
     fprintf(EXfileFeaturesOverall1Pass2PassOutAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n','mean','median','var','CM3','RMS','max','min','diff','count','diffMaxVal','dirChan','zeroCross','relDirChanZeroCross','distZeroCross','energy','entropy','averageFFT','std','CM3-mean','CM3-median','CM3-var','CM3-CM3','CM3-RMS','MAX-mean','MAX-median','MAX-var','MAX-CM3','MAX-RMS','MAX-max','MAX-min','MAX-diff','VAR-mean','VAR-median','VAR-var','VAR-CM3','VAR-RMS','VAR-max','VAR-min','VAR-diff','situation');
     fprintf(EXfileFeaturesOverall1Pass2PassOutAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','d');
     fprintf(EXfileFeaturesOverall1Pass2PassOutAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','class');
 
 %% Write header for non-annotated file:
     fprintf(EXfileFeaturesOverall1Pass2PassOutNoAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n','mean','median','var','CM3','RMS','max','min','diff','count','diffMaxVal','dirChan','zeroCross','relDirChanZeroCross','distZeroCross','energy','entropy','averageFFT','std','CM3-mean','CM3-median','CM3-var','CM3-CM3','CM3-RMS','MAX-mean','MAX-median','MAX-var','MAX-CM3','MAX-RMS','MAX-max','MAX-min','MAX-diff','VAR-mean','VAR-median','VAR-var','VAR-CM3','VAR-RMS','VAR-max','VAR-min','VAR-diff','situation','groundtruth');
     fprintf(EXfileFeaturesOverall1Pass2PassOutNoAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','d','d');
     fprintf(EXfileFeaturesOverall1Pass2PassOutNoAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','class');

    
    
%% Write Features for second row (VAR)
    EXFilename2ndVARFeaturesOverallOutAnn=strcat('WS',num2str(windowSizeTwoPassFirst),'-',num2str(windowSizeTwoPassSecond),'_Features2ndVAR_',num2str(p),'-annotated_[',filenames,'].tab');
    EXfile2ndVARFeaturesOverallOutAnn = fopen(EXFilename2ndVARFeaturesOverallOutAnn,'w');
    EXFilename2ndVARFeaturesOverallOutNoAnn=strcat('WS',num2str(windowSizeTwoPassFirst),'-',num2str(windowSizeTwoPassSecond),'_Features2ndVAR_',num2str(1-p),'-NOTannotated_[',filenames,'].tab');
    EXfile2ndVARFeaturesOverallOutNoAnn = fopen(EXFilename2ndVARFeaturesOverallOutNoAnn,'w');
%% Write header for annotated file:
    fprintf(EXfile2ndVARFeaturesOverallOutAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n','mean','median','var','CM3','RMS','max','min','diff','situation');
    fprintf(EXfile2ndVARFeaturesOverallOutAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n','c','c','c','c','c','c','c','c','d');
    fprintf(EXfile2ndVARFeaturesOverallOutAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n',' ',' ',' ',' ',' ',' ',' ',' ','class');

%% Write header for non-annotated file:
    fprintf(EXfile2ndVARFeaturesOverallOutNoAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n','mean','median','var','CM3','RMS','max','min','diff','situation','groundtruth');
    fprintf(EXfile2ndVARFeaturesOverallOutNoAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n','c','c','c','c','c','c','c','c','d','d');
    fprintf(EXfile2ndVARFeaturesOverallOutNoAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n',' ',' ',' ',' ',' ',' ',' ',' ',' ','class');

    %% Write Features for second row (CM3)
    EXFilename2ndCM3FeaturesOverallOutAnn=strcat('WS',num2str(windowSizeTwoPassFirst),'-',num2str(windowSizeTwoPassSecond),'_Features2ndCM3_',num2str(p),'-annotated_[',filenames,'].tab');
    EXfile2ndCM3FeaturesOverallOutAnn = fopen(EXFilename2ndCM3FeaturesOverallOutAnn,'w');
    EXFilename2ndCM3FeaturesOverallOutNoAnn=strcat('WS',num2str(windowSizeTwoPassFirst),'-',num2str(windowSizeTwoPassSecond),'_Features2ndCM3_',num2str(1-p),'-NOTannotated_[',filenames,'].tab');
    EXfile2ndCM3FeaturesOverallOutNoAnn = fopen(EXFilename2ndCM3FeaturesOverallOutNoAnn,'w');
%% Write header for annotated file:
    fprintf(EXfile2ndCM3FeaturesOverallOutAnn,'%s\t%s\t%s\t%s\t%s\t%s\n','mean','median','var','CM3','RMS','situation');
    fprintf(EXfile2ndCM3FeaturesOverallOutAnn,'%s\t%s\t%s\t%s\t%s\t%s\n','c','c','c','c','c','d');
    fprintf(EXfile2ndCM3FeaturesOverallOutAnn,'%s\t%s\t%s\t%s\t%s\t%s\n',' ',' ',' ',' ',' ','class');

%% Write header for non-annotated file:
    fprintf(EXfile2ndCM3FeaturesOverallOutNoAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\n','mean','median','var','CM3','RMS','situation','groundtruth');
    fprintf(EXfile2ndCM3FeaturesOverallOutNoAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\n','c','c','c','c','c','d','d');
    fprintf(EXfile2ndCM3FeaturesOverallOutNoAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\n',' ',' ',' ',' ',' ',' ','class');

%% Write Features for second row (max)
    EXFilename2ndmaxFeaturesOverallOutAnn=strcat('WS',num2str(windowSizeTwoPassFirst),'-',num2str(windowSizeTwoPassSecond),'_Features2ndmax_',num2str(p),'-annotated_[',filenames,'].tab');
    EXfile2ndmaxFeaturesOverallOutAnn = fopen(EXFilename2ndmaxFeaturesOverallOutAnn,'w');
    EXFilename2ndmaxFeaturesOverallOutNoAnn=strcat('WS',num2str(windowSizeTwoPassFirst),'-',num2str(windowSizeTwoPassSecond),'_Features2ndmax_',num2str(1-p),'-NOTannotated_[',filenames,'].tab');
    EXfile2ndmaxFeaturesOverallOutNoAnn = fopen(EXFilename2ndmaxFeaturesOverallOutNoAnn,'w');
%% Write header for annotated file:
    fprintf(EXfile2ndmaxFeaturesOverallOutAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n','mean','median','var','CM3','RMS','max','min','diff','situation');
    fprintf(EXfile2ndmaxFeaturesOverallOutAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n','c','c','c','c','c','c','c','c','d');
    fprintf(EXfile2ndmaxFeaturesOverallOutAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n',' ',' ',' ',' ',' ',' ',' ',' ','class');

%% Write header for non-annotated file:
    fprintf(EXfile2ndmaxFeaturesOverallOutNoAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n','mean','median','var','CM3','RMS','max','min','diff','situation','groundtruth');
    fprintf(EXfile2ndmaxFeaturesOverallOutNoAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n','c','c','c','c','c','c','c','c','d','d');
    fprintf(EXfile2ndmaxFeaturesOverallOutNoAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n',' ',' ',' ',' ',' ',' ',' ',' ',' ','class');

    
%% now write data to file
for i=1:length 
    RohdatenFilename=names{1,1}(i,1);
    fileRohdaten = fopen(RohdatenFilename{1});
    fgets(fileRohdaten);
    initialContentFileRohdaten = textscan(fileRohdaten, '%n' );
    fclose(fileRohdaten);
    
    %% Now identify the distinct variables and read them out into a matrix accordingly.
    [initialLengthContentFileRohdaten breadthContentFileRohdaten] = size(initialContentFileRohdaten{1});
    %% cut first and last x*100% of the data to remove noise at the beginning and end.
    %Shuyu: Cut 1/6+1/6 That is about 10sec for us. Seems reasonable to me.
    %cutPercentage=0.33; %% Important: This must be the SUM of the fraction
    %cut at the beginning and the end !!!
% % % %     cutPercentage=0.16;
% % % %     lengthContentFileRohdaten = initialLengthContentFileRohdaten*(1-cutPercentage);
% % % %     for cntr=1:lengthContentFileRohdaten
% % % %         contentFileRohdaten{1,1}(cntr,1)=initialContentFileRohdaten{1,1}(floor(initialLengthContentFileRohdaten*(cutPercentage/2))+cntr,1);
% % % %     end
    
    %% ALTERNATIVE (multiple-subject experiments): cut off last 30 seconds and then keep only the 2 minutes right before that.
    %One second is about 60 samples. 
    % Therefore: Cut off 30*60=1800 samples; then keep only the very last
    % 7200 samples and throw away the rest.
    
    lengthContentFileRohdaten = 2820; %%%% I changed this here to the length of the smallest file (For the mobile phone data, I already did the shortining of the data anyway
    for cntr=1:lengthContentFileRohdaten;
        contentFileRohdaten{1,1}(cntr,1)=initialContentFileRohdaten{1,1}(ceil((initialLengthContentFileRohdaten-lengthContentFileRohdaten)/2)+cntr,1);
    end
        
    %% Calculate features for 1Pass Process: 
    meanValues = zeros(floor(lengthContentFileRohdaten/windowSize),1);
    varValues = zeros(floor(lengthContentFileRohdaten/windowSize),1);
    medianValues = zeros(floor(lengthContentFileRohdaten/windowSize),1);
    CM3Values = zeros(floor(lengthContentFileRohdaten/windowSize),1);
    RMSValues = zeros(floor(lengthContentFileRohdaten/windowSize),1);
    maxValues = zeros(floor(lengthContentFileRohdaten/windowSize),1);
    minValues = zeros(floor(lengthContentFileRohdaten/windowSize),1);
    diffValues = zeros(floor(lengthContentFileRohdaten/windowSize),1);
    % #peaks with 10%<max
    countBetweenMaxValues = zeros(floor(lengthContentFileRohdaten/windowSize),1);
    % differenz aufeinanderfolgender Maxima
    diffMaxValues = zeros(floor(lengthContentFileRohdaten/windowSize),1);
    directionChanges = zeros(floor(lengthContentFileRohdaten/windowSize),1);
    zeroCrossings = zeros(floor(lengthContentFileRohdaten/windowSize),1);
    relationDirectionChangesZeroCrossings = zeros(floor(lengthContentFileRohdaten/windowSize),1);
    distanceBetweenZeroCrossings = zeros(floor(lengthContentFileRohdaten/windowSize),1);
    energyValues = zeros(floor(lengthContentFileRohdaten/windowSize),1);
    entropyValues = zeros(floor(lengthContentFileRohdaten/windowSize),1);
    averageFFTValues = zeros(floor(lengthContentFileRohdaten/windowSize),1);
    stdValues=zeros(floor(lengthContentFileRohdaten/windowSize),1);
    j=1;
    k=1;
    while j < lengthContentFileRohdaten-windowSize
        windowValues=zeros(1,windowSize);
        for l=1:windowSize
            windowValues(1,l) = contentFileRohdaten{1,1}(j+l-1,1);
        end
        j=j+windowSize;
        meanValues(k,1)=mean(windowValues);
        varValues(k,1)=var(windowValues);
        medianValues(k,1)=median(windowValues);
        CM3Values(k,1)=moment(windowValues,3);
        RMSValues(k,1)=sqrt(varValues(k,1));%RMS=sqrt(var)
        maxValues(k,1)=max(windowValues);
        minValues(k,1)=min(windowValues);
        diffValues(k,1)=maxValues(k,1)-minValues(k,1);
        count=0;
        previousMax=0;
        previousZeroCrossing=0;
        maxCounter=0;
        accumulatedMax=0;
        for counter=1:windowSize
            if (windowValues(1,counter)>(0.9*maxValues(k,1)) || windowValues(1,counter) < (0.9*minValues(k,1)))
                count=count+1;
            end
            if (counter > 1 && counter < windowSize) %shall not be applied for first and last value in the window
                if (windowValues(1,counter)>windowValues(1,counter-1)&&windowValues(1,counter)<windowValues(1,counter+1))%found new maximum
                    maxCounter=maxCounter+1;
                    accumulatedMax=accumulatedMax+(abs(windowValues(1,counter)-previousMax));
                    previousMax=windowValues(1,counter);
                    directionChanges(k,1)=directionChanges(k,1)+1;
                end
                if (windowValues(1,counter)<windowValues(1,counter-1)&&windowValues(1,counter)>windowValues(1,counter+1))%found new minimum
                    directionChanges(k,1)=directionChanges(k,1)+1;
                end
                if (windowValues(1,counter-1)>=0&&windowValues(1,counter)<0 || windowValues(1,counter-1)<0&&windowValues(1,counter)>=0) % found zero crossing
                    zeroCrossings(k,1)=zeroCrossings(k,1)+1;
                    distanceBetweenZeroCrossings(k,1) = distanceBetweenZeroCrossings(k,1)+(counter-previousZeroCrossing);
                    previousZeroCrossing=counter;
                end
            end
        end
        if (windowValues(1,windowSize-1)>=0&&windowValues(1,windowSize)<0 || windowValues(1,windowSize-1)<0&&windowValues(1,windowSize)>=0) % found zero crossing
                    zeroCrossings(k,1)=zeroCrossings(k,1)+1;
        end
        countBetweenMaxValues(k,1)=count;
        diffMaxValues(k,1)=accumulatedMax/maxCounter;%mean difference between subsequent maxima
        relationDirectionChangesZeroCrossings(k,1)=directionChanges(k,1)/zeroCrossings(k,1);
        distanceBetweenZeroCrossings(k,1)=distanceBetweenZeroCrossings(k,1)/zeroCrossings(k,1);
        %calculate the normalised spectral energy
        fftArray=real(fft(windowValues));
        PeIi=0;
        for PeIiCounter=1:(windowSize/2)
            PeIi=PeIi+((fftArray(PeIiCounter)^2)/sum(fftArray(1,1:floor(windowSize/2))))^2;
        end
        energyValues(k,1)=PeIi;
        % calculate Entropy
        PeIiEnt=0;
        for PeIiEntCounter=1:(windowSize/2)
            PeIiEnt=PeIiEnt+(fftArray(PeIiEntCounter)^2)/sum(fftArray(1,1:floor(windowSize/2)))*log((fftArray(PeIiEntCounter)^2)/sum(fftArray(1,1:floor(windowSize/2))));
        end
        entropyValues(k,1)=PeIiEnt;
        % calculate DC component (this is the average of windowSize -> So,
        % is there any use for this? I could have an average of the
        % fftArray instead?
        averageFFTValues(k,1)=mean(fftArray);
        stdValues(k,1)=std(windowValues);
        k=k+1;
    end
    %% Features based on 2Pass process:
    %% Calculate features for 1Pass: 
    meanValues1stPass = zeros(floor(lengthContentFileRohdaten/windowSizeTwoPassFirst),1);
    varValues1stPass = zeros(floor(lengthContentFileRohdaten/windowSizeTwoPassFirst),1);
    medianValues1stPass = zeros(floor(lengthContentFileRohdaten/windowSizeTwoPassFirst),1);
    CM3Values1stPass = zeros(floor(lengthContentFileRohdaten/windowSizeTwoPassFirst),1);
    RMSValues1stPass = zeros(floor(lengthContentFileRohdaten/windowSizeTwoPassFirst),1);
    maxValues1stPass = zeros(floor(lengthContentFileRohdaten/windowSizeTwoPassFirst),1);
    minValues1stPass = zeros(floor(lengthContentFileRohdaten/windowSizeTwoPassFirst),1);
    diffValues1stPass = zeros(floor(lengthContentFileRohdaten/windowSizeTwoPassFirst),1);
    % #peaks with 10%<max
    countBetweenMaxValues1stPass = zeros(floor(lengthContentFileRohdaten/windowSizeTwoPassFirst),1);
    % differenz aufeinanderfolgender Maxima
    diffMaxValues1stPass = zeros(floor(lengthContentFileRohdaten/windowSizeTwoPassFirst),1);
    directionChanges1stPass = zeros(floor(lengthContentFileRohdaten/windowSizeTwoPassFirst),1);
    zeroCrossings1stPass = zeros(floor(lengthContentFileRohdaten/windowSizeTwoPassFirst),1);
    relationDirectionChangesZeroCrossings1stPass = zeros(floor(lengthContentFileRohdaten/windowSizeTwoPassFirst),1);
    distanceBetweenZeroCrossings1stPass = zeros(floor(lengthContentFileRohdaten/windowSizeTwoPassFirst),1);
    j1stPass=1;
    k1stPass=1;
    while j1stPass < lengthContentFileRohdaten-windowSizeTwoPassFirst
        windowValues1stPass=zeros(1,windowSizeTwoPassFirst);
        for l1stPass=1:windowSizeTwoPassFirst
            windowValues1stPass(1,l1stPass) = contentFileRohdaten{1,1}(j1stPass+l1stPass-1,1);
        end
        j1stPass=j1stPass+windowSizeTwoPassFirst;
        meanValues1stPass(k1stPass,1)=mean(windowValues1stPass);
        varValues1stPass(k1stPass,1)=var(windowValues1stPass);
        medianValues1stPass(k1stPass,1)=median(windowValues1stPass);
        CM3Values1stPass(k1stPass,1)=moment(windowValues1stPass,3);
        RMSValues1stPass(k1stPass,1)=sqrt(varValues1stPass(k1stPass,1));%RMS=sqrt(var)
        maxValues1stPass(k1stPass,1)=max(windowValues1stPass);
        minValues1stPass(k1stPass,1)=min(windowValues1stPass);
        diffValues1stPass(k1stPass,1)=maxValues1stPass(k1stPass,1)-minValues1stPass(k1stPass,1);
        count1stPass=0;
        previousMax1stPass=0;
        previousZeroCrossing1stPass=0;
        maxCounter1stPass=0;
        accumulatedMax1stPass=0;
        for counter1stPass=1:windowSizeTwoPassFirst
            if (windowValues1stPass(1,counter1stPass)>(0.9*maxValues1stPass(k1stPass,1)) || windowValues1stPass(1,counter1stPass) < (0.9*minValues1stPass(k1stPass,1)))
                count1stPass=count1stPass+1;
            end
            if (counter1stPass > 1 && counter1stPass < windowSizeTwoPassFirst) %shall not be applied for first and last value in the window
                if (windowValues1stPass(1,counter1stPass)>windowValues1stPass(1,counter1stPass-1)&&windowValues1stPass(1,counter1stPass)<windowValues1stPass(1,counter1stPass+1))%found new maximum
                    maxCounter1stPass=maxCounter1stPass+1;
                    accumulatedMax1stPass=accumulatedMax1stPass+(abs(windowValues1stPass(1,counter1stPass)-previousMax1stPass));
                    previousMax1stPass=windowValues1stPass(1,counter1stPass);
                    directionChanges1stPass(k1stPass,1)=directionChanges1stPass(k1stPass,1)+1;
                end
                if (windowValues1stPass(1,counter1stPass)<windowValues1stPass(1,counter1stPass-1)&&windowValues1stPass(1,counter1stPass)>windowValues1stPass(1,counter1stPass+1))%found new minimum
                    directionChanges1stPass(k1stPass,1)=directionChanges1stPass(k1stPass,1)+1;
                end
                if (windowValues1stPass(1,counter1stPass-1)>=0&&windowValues1stPass(1,counter1stPass)<0 || windowValues1stPass(1,counter1stPass-1)<0&&windowValues1stPass(1,counter1stPass)>=0) % found zero crossing
                    zeroCrossings1stPass(k1stPass,1)=zeroCrossings1stPass(k1stPass,1)+1;
                    distanceBetweenZeroCrossings1stPass(k1stPass,1) = distanceBetweenZeroCrossings1stPass(k1stPass,1)+(counter1stPass-previousZeroCrossing1stPass);
                    previousZeroCrossing1stPass=counter1stPass;
                end
            end
        end
        if (windowValues1stPass(1,windowSizeTwoPassFirst-1)>=0&&windowValues1stPass(1,windowSizeTwoPassFirst)<0 || windowValues1stPass(1,windowSizeTwoPassFirst-1)<0&&windowValues1stPass(1,windowSizeTwoPassFirst)>=0) % found zero crossing
                    zeroCrossings1stPass(k1stPass,1)=zeroCrossings1stPass(k1stPass,1)+1;
        end
        countBetweenMaxValues1stPass(k1stPass,1)=count1stPass;
        diffMaxValues1stPass(k1stPass,1)=accumulatedMax1stPass/maxCounter1stPass;%mean difference between subsequent maxima
        relationDirectionChangesZeroCrossings1stPass(k1stPass,1)=directionChanges1stPass(k1stPass,1)/zeroCrossings1stPass(k1stPass,1);
        distanceBetweenZeroCrossings1stPass(k1stPass,1)=distanceBetweenZeroCrossings1stPass(k1stPass,1)/zeroCrossings1stPass(k1stPass,1);
        k1stPass=k1stPass+1;
    end
    %% variance as basis:
    % Variance on top of variance? does this make sense?
    [breadth2nd width2nd]=size(varValues1stPass);
    meanValues2ndVAR = zeros(floor(breadth2nd/windowSizeTwoPassSecond),1);
    varValues2ndVAR = zeros(floor(breadth2nd/windowSizeTwoPassSecond),1);
    medianValues2ndVAR = zeros(floor(breadth2nd/windowSizeTwoPassSecond),1);
    CM3Values2ndVAR = zeros(floor(breadth2nd/windowSizeTwoPassSecond),1);
    RMSValues2ndVAR = zeros(floor(breadth2nd/windowSizeTwoPassSecond),1);
    maxValues2ndVAR = zeros(floor(breadth2nd/windowSizeTwoPassSecond),1);
    minValues2ndVAR = zeros(floor(breadth2nd/windowSizeTwoPassSecond),1);
    diffValues2ndVAR = zeros(floor(breadth2nd/windowSizeTwoPassSecond),1);
    j2=1;
    k2=1;
    while j2 < breadth2nd-windowSizeTwoPassSecond
        windowValues2ndVAR=zeros(1,windowSizeTwoPassSecond);
        for l2=1:windowSizeTwoPassSecond
            windowValues2ndVAR(1,l2) = varValues1stPass(j2+l2-1,1);
        end
        j2=j2+windowSizeTwoPassSecond;
        meanValues2ndVAR(k2,1)=mean(windowValues2ndVAR);
        varValues2ndVAR(k2,1)=var(windowValues2ndVAR);
        medianValues2ndVAR(k2,1)=median(windowValues2ndVAR);
        CM3Values2ndVAR(k2,1)=moment(windowValues2ndVAR,3);
        RMSValues2ndVAR(k2,1)=sqrt(varValues2ndVAR(k2,1));%RMS=sqrt(var)
        maxValues2ndVAR(k2,1)=max(windowValues2ndVAR);
        minValues2ndVAR(k2,1)=min(windowValues2ndVAR);
        diffValues2ndVAR(k2,1)=maxValues2ndVAR(k2,1)-minValues2ndVAR(k2,1);
        k2=k2+1;
    end
    
    
    %% CM3 as basis:
    meanValues2ndCM3 = zeros(floor(breadth2nd/windowSizeTwoPassSecond),1);
    varValues2ndCM3 = zeros(floor(breadth2nd/windowSizeTwoPassSecond),1);
    medianValues2ndCM3 = zeros(floor(breadth2nd/windowSizeTwoPassSecond),1);
    CM3Values2ndCM3 = zeros(floor(breadth2nd/windowSizeTwoPassSecond),1);
    RMSValues2ndCM3 = zeros(floor(breadth2nd/windowSizeTwoPassSecond),1);
    j2CM3=1;
    k2CM3=1;
    while j2CM3 < breadth2nd-windowSizeTwoPassSecond
        windowValues2ndCM3=zeros(1,windowSizeTwoPassSecond);
        for l2CM3=1:windowSizeTwoPassSecond
            windowValues2ndCM3(1,l2CM3) = varValues1stPass(j2CM3+l2CM3-1,1);
        end
        j2CM3=j2CM3+windowSizeTwoPassSecond;
        meanValues2ndCM3(k2CM3,1)=mean(windowValues2ndCM3);
        varValues2ndCM3(k2CM3,1)=var(windowValues2ndCM3);
        medianValues2ndCM3(k2CM3,1)=median(windowValues2ndCM3);
        CM3Values2ndCM3(k2CM3,1)=moment(windowValues2ndCM3,3);
        RMSValues2ndCM3(k2CM3,1)=sqrt(varValues2ndCM3(k2CM3,1));%RMS=sqrt(var)
        k2CM3=k2CM3+1;
    end
    
    %% max as basis:
    meanValues2ndmax = zeros(floor(breadth2nd/windowSizeTwoPassSecond),1);
    varValues2ndmax = zeros(floor(breadth2nd/windowSizeTwoPassSecond),1);
    medianValues2ndmax = zeros(floor(breadth2nd/windowSizeTwoPassSecond),1);
    CM3Values2ndmax = zeros(floor(breadth2nd/windowSizeTwoPassSecond),1);
    RMSValues2ndmax = zeros(floor(breadth2nd/windowSizeTwoPassSecond),1);
    maxValues2ndmax = zeros(floor(breadth2nd/windowSizeTwoPassSecond),1);
    minValues2ndmax = zeros(floor(breadth2nd/windowSizeTwoPassSecond),1);
    diffValues2ndmax = zeros(floor(breadth2nd/windowSizeTwoPassSecond),1);
    j2max=1;
    k2max=1;
    while j2max < breadth2nd-windowSizeTwoPassSecond
        windowValues2ndmax=zeros(1,windowSizeTwoPassSecond);
        for l2max=1:windowSizeTwoPassSecond
            windowValues2ndmax(1,l2max) = varValues1stPass(j2max+l2max-1,1);
        end
        j2max=j2max+windowSizeTwoPassSecond;
        meanValues2ndmax(k2max,1)=mean(windowValues2ndmax);
        varValues2ndmax(k2max,1)=var(windowValues2ndmax);
        medianValues2ndmax(k2max,1)=median(windowValues2ndmax);
        CM3Values2ndmax(k2max,1)=moment(windowValues2ndmax,3);
        RMSValues2ndmax(k2max,1)=sqrt(varValues2ndmax(k2max,1));%RMS=sqrt(var)
        maxValues2ndmax(k2max,1)=max(windowValues2ndmax);
        minValues2ndmax(k2max,1)=min(windowValues2ndmax);
        diffValues2ndmax(k2max,1)=maxValues2ndmax(k2max,1)-minValues2ndmax(k2max,1);
        k2max=k2max+1;        
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
    
        for l=1:lengthContentFileRohdaten
            if rand(1)<(p)     
                fprintf(EXfileOverallOutAnn,'%s\t%s\n',num2str(contentFileRohdaten{1,1}(l,1)),names{1,1}{i,1}(1,:));
            else
                fprintf(EXfileOverallOutNoAnn,'%s\t%s\t%s\n',num2str(contentFileRohdaten{1,1}(l,1)),'?',names{1,1}{i,1}(1,:));
            end              
        end
        for l=1:k-1
            if rand(1)<(p)     
                fprintf(EXfileFeaturesOverallOutAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n',num2str(meanValues(l,1)),num2str(medianValues(l,1)),num2str(varValues(l,1)),num2str(CM3Values(l,1)),num2str(RMSValues(l,1)),num2str(maxValues(l,1)),num2str(minValues(l,1)),num2str(diffValues(l,1)),num2str(countBetweenMaxValues(l,1)),num2str(diffMaxValues(l,1)),num2str(directionChanges(l,1)),num2str(zeroCrossings(l,1)),num2str(relationDirectionChangesZeroCrossings(l,1)),num2str(distanceBetweenZeroCrossings(l,1)),names{1,1}{i,1}(1,:));
            else
                fprintf(EXfileFeaturesOverallOutNoAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n',num2str(meanValues(l,1)),num2str(medianValues(l,1)),num2str(varValues(l,1)),num2str(CM3Values(l,1)),num2str(RMSValues(l,1)),num2str(maxValues(l,1)),num2str(minValues(l,1)),num2str(diffValues(l,1)),num2str(countBetweenMaxValues(l,1)),num2str(diffMaxValues(l,1)),num2str(directionChanges(l,1)),num2str(zeroCrossings(l,1)),num2str(relationDirectionChangesZeroCrossings(l,1)),num2str(distanceBetweenZeroCrossings(l,1)),'?',names{1,1}{i,1}(1,:));
            end              
        end
        for l2=1:k2-1
            if rand(1)<(p)     
                fprintf(EXfile2ndVARFeaturesOverallOutAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n',num2str(meanValues2ndVAR(l2,1)),num2str(medianValues2ndVAR(l2,1)),num2str(varValues2ndVAR(l2,1)),num2str(CM3Values2ndVAR(l2,1)),num2str(RMSValues2ndVAR(l2,1)),num2str(maxValues2ndVAR(l2,1)),num2str(minValues2ndVAR(l2,1)),num2str(diffValues2ndVAR(l2,1)),names{1,1}{i,1}(1,:));
            else
                fprintf(EXfile2ndVARFeaturesOverallOutNoAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n',num2str(meanValues2ndVAR(l2,1)),num2str(medianValues2ndVAR(l2,1)),num2str(varValues2ndVAR(l2,1)),num2str(CM3Values2ndVAR(l2,1)),num2str(RMSValues2ndVAR(l2,1)),num2str(maxValues2ndVAR(l2,1)),num2str(minValues2ndVAR(l2,1)),num2str(diffValues2ndVAR(l2,1)),'?',names{1,1}{i,1}(1,:));
            end              
        end
        for l2CM3=1:k2CM3-1
            if rand(1)<(p)     
                 fprintf(EXfile2ndCM3FeaturesOverallOutAnn,'%s\t%s\t%s\t%s\t%s\t%s\n',num2str(meanValues2ndCM3(l2CM3,1)),num2str(medianValues2ndCM3(l2CM3,1)),num2str(varValues2ndCM3(l2CM3,1)),num2str(CM3Values2ndCM3(l2CM3,1)),num2str(RMSValues2ndCM3(l2CM3,1)),names{1,1}{i,1}(1,:));
            else
                fprintf(EXfile2ndCM3FeaturesOverallOutNoAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\n',num2str(meanValues2ndCM3(l2CM3,1)),num2str(medianValues2ndCM3(l2CM3,1)),num2str(varValues2ndCM3(l2CM3,1)),num2str(CM3Values2ndCM3(l2CM3,1)),num2str(RMSValues2ndCM3(l2CM3,1)),'?',names{1,1}{i,1}(1,:));
            end              
        end
        for l2max=1:k2max-1
            if rand(1)<(p)     
                 fprintf(EXfile2ndmaxFeaturesOverallOutAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n',num2str(meanValues2ndmax(l2max,1)),num2str(medianValues2ndmax(l2max,1)),num2str(varValues2ndmax(l2max,1)),num2str(maxValues2ndmax(l2max,1)),num2str(RMSValues2ndmax(l2max,1)),num2str(maxValues2ndmax(l2max,1)),num2str(minValues2ndmax(l2max,1)),num2str(diffValues2ndmax(l2max,1)),num2str(meanValues2ndVAR(l2,1)),num2str(medianValues2ndVAR(l2,1)),num2str(varValues2ndVAR(l2,1)),num2str(CM3Values2ndVAR(l2,1)),num2str(RMSValues2ndVAR(l2,1)),num2str(maxValues2ndVAR(l2,1)),num2str(minValues2ndVAR(l2,1)),num2str(diffValues2ndVAR(l2,1)),names{1,1}{i,1}(1,:));
            else
                fprintf(EXfile2ndmaxFeaturesOverallOutNoAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n',num2str(meanValues2ndmax(l2max,1)),num2str(medianValues2ndmax(l2max,1)),num2str(varValues2ndmax(l2max,1)),num2str(maxValues2ndmax(l2max,1)),num2str(RMSValues2ndmax(l2max,1)),num2str(maxValues2ndmax(l2max,1)),num2str(minValues2ndmax(l2max,1)),num2str(diffValues2ndmax(l2max,1)),'?',names{1,1}{i,1}(1,:));
            end              
        end
        %write a combined output file. 
        % Important here: take care that e.g. 2-Pass features in test did
        % not use data that was also used for 1-pass features in training.
        % Therefore: take decision on 
        %windowSize=70; 
        %windowSizeTwoPassFirst=20;
        %windowSizeTwoPassSecond=20;
        
        commonWindowSize=windowSizeTwoPassFirst*windowSizeTwoPassSecond;
        moduloResult=floor(commonWindowSize/windowSize);
        
        for lcounter=1:k2-1
            if rand(1)<(p)
                % write all corresponding data.
                % easy for 2Pass, but what then for 1-Pass?
                for zaehler=1:moduloResult
                    fprintf(EXfileFeaturesOverall1Pass2PassOutAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n',num2str(meanValues((lcounter-1)*moduloResult+zaehler,1)),num2str(medianValues((lcounter-1)*moduloResult+zaehler,1)),num2str(varValues((lcounter-1)*moduloResult+zaehler,1)),num2str(CM3Values((lcounter-1)*moduloResult+zaehler,1)),num2str(RMSValues((lcounter-1)*moduloResult+zaehler,1)),num2str(maxValues((lcounter-1)*moduloResult+zaehler,1)),num2str(minValues((lcounter-1)*moduloResult+zaehler,1)),num2str(diffValues((lcounter-1)*moduloResult+zaehler,1)),num2str(countBetweenMaxValues((lcounter-1)*moduloResult+zaehler,1)),num2str(diffMaxValues((lcounter-1)*moduloResult+zaehler,1)),num2str(directionChanges((lcounter-1)*moduloResult+zaehler,1)),num2str(zeroCrossings((lcounter-1)*moduloResult+zaehler,1)),num2str(relationDirectionChangesZeroCrossings((lcounter-1)*moduloResult+zaehler,1)),num2str(distanceBetweenZeroCrossings((lcounter-1)*moduloResult+zaehler,1)),num2str(energyValues((lcounter-1)*moduloResult+zaehler,1)),num2str(entropyValues((lcounter-1)*moduloResult+zaehler,1)),num2str(averageFFTValues((lcounter-1)*moduloResult+zaehler,1)),num2str(stdValues((lcounter-1)*moduloResult+zaehler,1)),num2str(meanValues2ndCM3(lcounter,1)),num2str(medianValues2ndCM3(lcounter,1)),num2str(varValues2ndCM3(lcounter,1)),num2str(CM3Values2ndCM3(lcounter,1)),num2str(RMSValues2ndCM3(lcounter,1)),num2str(meanValues2ndmax(lcounter,1)),num2str(medianValues2ndmax(lcounter,1)),num2str(varValues2ndmax(lcounter,1)),num2str(maxValues2ndmax(lcounter,1)),num2str(RMSValues2ndmax(lcounter,1)),num2str(maxValues2ndmax(lcounter,1)),num2str(minValues2ndmax(lcounter,1)),num2str(diffValues2ndmax(lcounter,1)),num2str(meanValues2ndVAR(lcounter,1)),num2str(medianValues2ndVAR(lcounter,1)),num2str(varValues2ndVAR(lcounter,1)),num2str(CM3Values2ndVAR(lcounter,1)),num2str(RMSValues2ndVAR(lcounter,1)),num2str(maxValues2ndVAR(lcounter,1)),num2str(minValues2ndVAR(lcounter,1)),num2str(diffValues2ndVAR(lcounter,1)),names{1,1}{i,1}(1,:));
                end
            else
                for zaehler=1:moduloResult
                    fprintf(EXfileFeaturesOverall1Pass2PassOutNoAnn,'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n',num2str(meanValues((lcounter-1)*moduloResult+zaehler,1)),num2str(medianValues((lcounter-1)*moduloResult+zaehler,1)),num2str(varValues((lcounter-1)*moduloResult+zaehler,1)),num2str(CM3Values((lcounter-1)*moduloResult+zaehler,1)),num2str(RMSValues((lcounter-1)*moduloResult+zaehler,1)),num2str(maxValues((lcounter-1)*moduloResult+zaehler,1)),num2str(minValues((lcounter-1)*moduloResult+zaehler,1)),num2str(diffValues((lcounter-1)*moduloResult+zaehler,1)),num2str(countBetweenMaxValues((lcounter-1)*moduloResult+zaehler,1)),num2str(diffMaxValues((lcounter-1)*moduloResult+zaehler,1)),num2str(directionChanges((lcounter-1)*moduloResult+zaehler,1)),num2str(zeroCrossings((lcounter-1)*moduloResult+zaehler,1)),num2str(relationDirectionChangesZeroCrossings((lcounter-1)*moduloResult+zaehler,1)),num2str(distanceBetweenZeroCrossings((lcounter-1)*moduloResult+zaehler,1)),num2str(energyValues((lcounter-1)*moduloResult+zaehler,1)),num2str(entropyValues((lcounter-1)*moduloResult+zaehler,1)),num2str(averageFFTValues((lcounter-1)*moduloResult+zaehler,1)),num2str(stdValues((lcounter-1)*moduloResult+zaehler,1)),num2str(meanValues2ndCM3(lcounter,1)),num2str(medianValues2ndCM3(lcounter,1)),num2str(varValues2ndCM3(lcounter,1)),num2str(CM3Values2ndCM3(lcounter,1)),num2str(RMSValues2ndCM3(lcounter,1)),num2str(meanValues2ndmax(lcounter,1)),num2str(medianValues2ndmax(lcounter,1)),num2str(varValues2ndmax(lcounter,1)),num2str(maxValues2ndmax(lcounter,1)),num2str(RMSValues2ndmax(lcounter,1)),num2str(maxValues2ndmax(lcounter,1)),num2str(minValues2ndmax(lcounter,1)),num2str(diffValues2ndmax(lcounter,1)),num2str(meanValues2ndVAR(lcounter,1)),num2str(medianValues2ndVAR(lcounter,1)),num2str(varValues2ndVAR(lcounter,1)),num2str(CM3Values2ndVAR(lcounter,1)),num2str(RMSValues2ndVAR(lcounter,1)),num2str(maxValues2ndVAR(lcounter,1)),num2str(minValues2ndVAR(lcounter,1)),num2str(diffValues2ndVAR(lcounter,1)),'?',names{1,1}{i,1}(1,:));
                end
            end              
        end
end
    fclose(EXfileOverallOutAnn);
    fclose(EXfileOverallOutNoAnn);

% choose appropriate rows from orange input files created by 'createOrangeInputFilesForOrange.m'

function [] = chooseColumnsFromOrangeInputFiles_Gestures(filenameInputFileOrange)
    %%Config:
        numColumnsToRead=15;
        outputFilename='1-5-9-13';

        columnsToWrite=[1,5,9,numColumnsToRead];
        %columnsToWrite=[1,2,7,18,numColumnsToRead];
        %columnsToWrite=[1,3,8,numColumnsToRead];
        %columnsToWrite=[1,3,6,8,numColumnsToRead]; % only non-combined features
        %columnsToWrite=[1,3,6,8,numColumnsToRead];
        %columnsToWrite=[3,numColumnsToRead-1,numColumnsToRead];
        
        
%%Before feature subset selection (15 attributes):
%0.073 variance                         03
%0.066 min                              11
%0.062 sign                             06
%0.060 distance2                        09
%0.030 levels                           07
%0.023 slope2                           14
%0.003 trend                            08
%0.002 median                           02
%0.001 distance                         04
%0.000 mean2                            15
%0.000 max                              10
%0.000 diffMinMax                       12
%-0.000 diff                            05
%-0.001 slope                           13
%-0.002 mean                            01

%%After feature subset selection with margin 0.010 (6 attributes):
%0.074 variance                         03 ***
%0.066 sign                             06
%0.062 distance2                        09 ***
%0.062 min                              11 ***
%0.028 levels                           07 ***               
%0.018 slope2                           14
        
%0.086 variance
%0.065 min
%0.053 slope2
%0.053 distance2
%0.035 sign
%0.018 levels

%After feature subset selection with margin 0.010 (5 attributes):
%0.065 slope2                           14
%0.056 variance                         03
%0.056 min                              11
%0.041 distance2                        09
%0.020 levels                           07
        
    %% Read input file provided

    fileInputOrange = fopen(strcat(filenameInputFileOrange,'.tab'));
    % Write the contents of the file into an array.
    % Here, the number of columns must be correctly specified
    
    stringColumnsToRead='%s\t';
    for i=1:numColumnsToRead
        stringColumnsToRead=strcat(stringColumnsToRead,'%s\t');
    end
    stringColumnsToRead=strcat(stringColumnsToRead,'\n');
    InputValues=textscan(fileInputOrange,stringColumnsToRead);
    % write the 'class' value to the correct location
    %this solution does not work since for the write later
    InputValues{1,numColumnsToRead}(3,1)=InputValues{1,1}(3,1);
    InputValues{1,1}(3,1)={''};
    
    fclose(fileInputOrange);
    
    
    [ctwle ctwbr] = size(columnsToWrite);
    stringColumnsToWrite='%s\t';
    for i=2:ctwbr
        %create string that determines the number of columns
        stringColumnsToWrite=strcat(stringColumnsToWrite,'%s\t');
    end
    stringColumnsToWrite=strcat(stringColumnsToWrite,'\n');
    
    
    %% Write predefined columns again
    [le br]=size(InputValues{1,1});
    fileOutputFile = fopen(strcat('output_',filenameInputFileOrange,'_',outputFilename,'.tab'),'w');
    for i=1:le
        if (i==3)
            for j=1:ctwbr-1
                fprintf(fileOutputFile,'\t');
            end
            fprintf(fileOutputFile,'%s\t',InputValues{1,columnsToWrite(1,ctwbr)}{i,1}(1,:));
        else
            for j=1:ctwbr
                fprintf(fileOutputFile,'%s\t',InputValues{1,columnsToWrite(1,j)}{i,1}(1,:));
            end
        end
        fprintf(fileOutputFile,'\n');
    end    
    fclose(fileOutputFile);
end
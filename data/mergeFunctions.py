import csv
import glob
import os
import sys

def mergeCSV(filename=str):
    data_path = ""
    outfile_path = filename+".csv"
    filewriter = csv.writer(open(outfile_path,'wb'))
    file_counter = 0
    for input_file in glob.glob(os.path.join(data_path,'*.csv')):
            with open(input_file,'rU') as csv_file:
                    filereader = csv.reader(csv_file)
                    yr=input_file[6:10] 
                    if file_counter < 1:
                            for row in filereader:
                                    filewriter.writerow(row)
                    else:
                            header = next(filereader,None)
                            for row in filereader:
                                    filewriter.writerow(row+[yr])
            file_counter += 1

def processMerged(filename):
    unclean_file = filename+".csv"
    columns = ['name', 'team','age', 'position', 'games_played',
           'games_started', 'rushing_attempts', 'rushing_yards', 'rushing_TD',
          'rushing_long','rushing_ydsAvg', 'rushing_ydsGame', 'rushing_attGame',
          'receiving_targets','receiving_receptions','receiving_yards','receiving_ydsAvg',
          'receiving_TD','receiving_long','receiving_recsGame','receiving_ydsGame',
          'yardsfromScrimmage', 'RRTD', 'fumbles','year']
    unclean_df = pd.read_csv(unclean_file, header=None)
    unclean_df=unclean_df.drop([0], axis=1)
    unclean_df.columns=columns
    unclean_df['position']=unclean_df['position'].astype('str')
    unclean_df['position'] = unclean_df['position'].str.upper()
    clean_df = unclean_df[pd.notnull(unclean_df['name'])]
    clean_df.to_csv("%s.csv" % filename, index=False )

def mergeCleanFiles(outputFileName):
    mergeCSV(outputFileName)
    processMerged(outputFileName)
    

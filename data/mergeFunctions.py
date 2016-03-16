import os
import glob
import pandas as pd


def cleanPassing(folder_path, output_filename):
    """
    Cleans and processes multiple .csv passing data files
    Creates new merged passing .csv file
    folder_path: string of file folder with .csv of passing data files
    output_filename: string name for merged .csv file
    """
    try:
        os.remove(output_filename+".csv")
    except OSError:
        pass
    current_dir = folder_path
    df_list = []
    for input_file in glob.glob(os.path.join(current_dir, '*.csv')):
        df = pd.read_csv(input_file)
        filename_year = input_file.split("_")[1]
        df = df.drop(['Rk'],  axis=1)
        df.rename(columns={'Unnamed: 1': 'Name'}, inplace=True)
        df['year'] = filename_year
        df_list.append(df)
    joined_data = pd.concat(df_list)
    passing_columns = {
                      'Name': 'name', 'Tm': 'team', 'Age': 'age',
                      'Pos': 'position', 'G': 'games_played', 'GS':
                      'games_started', 'QBrec': 'record', 'Cmp': 'completions',
                      'Att': 'attempts', 'Cmp%': 'completionPct', 'Yds':
                      'passing_yards', 'TD': 'passing_TD',  'TD%':
                      'passing_TDPct', 'Int': 'passing_INT', 'Int%':
                      'passing_INTPct', 'Lng': 'passing_long', 'Y/A':
                      'passing_ydsAtt', 'AY/A': 'passing_airydsAtt', 'Y/C':
                      'passing_ydsComp', 'Y/G': 'passing_ydsGame', 'Rate':
                      'passing_rating', 'Sk': 'passing_sacks', 'Yds.1':
                      'passing_sacksyds', 'ANY/A': 'passing_airnetydsAtt',
                      'Sk%': 'passing_sackPct',  '4QC': 'FourthQtrComebacks',
                      'GWD': 'gamewinningdrives', 'NY/A': 'netydsAtt'
                      }
    ordered_columns = [
                      'name', 'team',  'year', 'age', 'position', 'wins',
                      'losses', 'games_played', 'games_started', 'completions',
                      'attempts', 'completionPct', 'passing_yards',
                      'passing_TD', 'passing_TDPct',  'passing_INT',
                      'passing_INTPct', 'passing_long', 'passing_ydsAtt',
                      'passing_airydsAtt', 'passing_ydsComp',
                      'passing_ydsGame', 'passing_rating', 'passing_sacks',
                      'passing_sacksyds', 'passing_airnetydsAtt',
                      'passing_sackPct', 'FourthQtrComebacks',
                      'gamewinningdrives'
                       ]
    joined_data = joined_data.rename(columns=passing_columns)
    unclean_df = joined_data
    unclean_df['record'] = unclean_df['record'].astype('str')
    unclean_df['position'] = unclean_df['position'].astype('str')
    unclean_df['position'] = unclean_df['position'].str.upper()
    unclean_df['record'].loc[unclean_df.record == 'QBrec'] = "0-0-0"
    unclean_df['record'].loc[unclean_df.record == 'nan'] = "0-0-0"
    unformatted_record = unclean_df['record'].str[:]
    unformatted_record = unformatted_record.str.replace("-",  "/")
    unclean_df['wins'] = unformatted_record.str.split("/").str[0]
    unclean_df['losses'] = unformatted_record.str.split("/").str[1]
    unclean_df['name'] = unclean_df['name'].str.replace('[+|*]', "")
    unclean_df['wins'] = unclean_df['wins'].astype('float')
    unclean_df = pd.DataFrame(data=unclean_df, columns=ordered_columns)
    clean_df = unclean_df[pd.notnull(unclean_df['name'])]
    clean_df.sort_values('wins', ascending=False, axis=0, inplace=True)
    clean_df.to_csv("%s.csv" % output_filename, index=False)


def cleanRushingReceiving(folder_path, output_filename):
    """
    Cleans and processes multiple .csv files of rushing-receiving data
    Creates new merged rushing-receiving .csv file
    folder_path: string of file folder with .csvs of rushing-receiving data
    output_filename: string name for merged rushing-receiving .csv file
    """
    try:
        os.remove(output_filename+".csv")
    except OSError:
        pass
    current_dir = folder_path
    df_list = []
    for input_file in glob.glob(os.path.join(current_dir, '*.csv')):
        df = pd.read_csv(input_file)
        filename_year = input_file.split("_")[1]
        df = df.drop(['Unnamed: 0'], axis=1)
        df.rename(columns={'Unnamed: 1': 'Name'}, inplace=True)
        df['year'] = filename_year
        df_list.append(df)
    joined_data = pd.concat(df_list)
    rushing_rec_columns = {
                          'Name': 'name', 'Unnamed: 2': "team", 'Unnamed: 3':
                          'age', 'Unnamed: 4': 'position', 'Games':
                          'games_played', 'Games.1': 'games_started',
                          'Rushing': 'rushing_attempts', 'Rushing.1':
                          'rushing_yards', 'Rushing.2': 'rushing_TD',
                          'Rushing.3': 'rushing_long',
                          'Rushing.4': 'rushing_ydsAtt',
                          'Rushing.5': 'rushing_ydsGame',
                          'Rushing.6': 'rushing_attGame', 'Receiving':
                          'receiving_targets', 'Receiving.1':
                          'receiving_receptions', 'Receiving.2':
                          'receiving_yards', 'Receiving.3': 'receiving_ydsRec',
                          'Receiving.4': 'receiving_TD', 'Receiving.5':
                          'receiving_long',
                          'Receiving.6': 'receiving_recsGame',
                          'Receiving.7': 'receiving_ydsGame', 'Unnamed: 22':
                          'yardsfromScrimmage', 'Unnamed: 23': 'RRTD',
                          'Unnamed: 24': 'fumbles'
                          }
    joined_data = joined_data.rename(columns=rushing_rec_columns)
    unclean_df = joined_data
    unclean_df['name'] = unclean_df['name'].str.replace('[+|*]', "")
    clean_df = unclean_df[pd.notnull(unclean_df['name'])]
    clean_df.to_csv("%s.csv" % output_filename, index=False)


def processPlayerDB(folder_path, input_file):
    """
    Cleans and processes .csv player database file
    Creates new player database .csv from input_file with suffix "-processed"
    folder_path: string of file folder with .csv of player database
    input_file: string of .csv player database file name
    """
    try:
        os.remove("%s-processed.csv" % input_file)
    except OSError:
        pass
    os.chdir(folder_path)
    DBfile = input_file+'.csv'
    playerDB = pd.read_csv(DBfile)
    height_map = {
                 '4-Jun': '76', '8-May': '58', '11-May': '71', '10-May': '70',
                 '1-Jun': '73', '2-Jun': '74', 'Jun-00': '72',  '5-Jun': '77',
                 '3-Jun': '75', '9-May': '69', '6-Jun': '78', '4-May': '64',
                 '7-May': '67', '6-May': '66', '7-Jun': '79', '8-Jun': '80',
                 '5-May': '65', '9-Jun': '81', '12-May': '72', '3-May': '63',
                 '1-May': '61', 'Jul-00': '72', '10-Jun': '82', '77-6': '77',
                 'nan': '0'
                 }
    playerDB['height'] = playerDB['height'].astype('string')
    playerDB['height'].replace(height_map, inplace=True)
    playerDB['height'] = playerDB['height'].replace(
                         '', '', regex=True).astype('int64')
    playerDB['draft_round'] = playerDB['draft_round'].replace(
                              '[^0-9]', '', regex=True).astype('string')
    playerDB['draft_round'].replace({'nan': '0'}, inplace=True)
    playerDB['draft_round'] = playerDB['draft_round'].astype('int64')
    playerDB['draft_pick'] = playerDB['draft_pick'].replace(
                             '[^0-9]', '', regex=True).astype('string')
    playerDB['draft_pick'].replace({'nan': '0', '': '0'}, inplace=True)
    playerDB['draft_pick'] = playerDB['draft_pick'].astype('int64')
    playerDB.to_csv("%s-processed.csv" % input_file, index=False)

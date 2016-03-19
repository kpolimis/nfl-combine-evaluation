import os
import glob
import sqlite3
import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, output_notebook, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models.widgets import Panel, Tabs
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
sns.set()


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
import numpy as np
import pandas as pd
import sqlite3
from bokeh.plotting import figure, output_file, output_notebook, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models.widgets import Panel, Tabs

#Create database connection
con = sqlite3.connect('../data/nflPPdb.sqlite')

#Create RB and WR dataframes
def make_dfs():
    """
    Creates dataframes for plotting using SQL queries.

    Returns a dataframe for each positional group (dfRB, dfWR, dfQB).
    """
    df1 = pd.read_sql_query('SELECT combine.name, combine.fortyyd, combine.heightinchestotal,\
                            combine.weight, combine.twentyss, combine.vertical, combine.year\
                            FROM combine\
                            WHERE combine.year < 2009 AND combine.pickround != 0', con)
    df1['speedscore'] = (df1['weight']*200)/(df1['fortyyd']**4)
    df2 = pd.read_sql_query('SELECT combine.name, combine.year, players.position\
                            FROM combine, players\
                            WHERE combine.name = players.name AND combine.year = players.draft_year', con)
    df3 = pd.merge(df1, df2, on=['name', 'year'], how='inner', suffixes=('df1','df2'))
    df3 = df3.drop_duplicates(subset='name', keep=False)
    df4 = pd.read_sql_query('SELECT DISTINCT combine.name, rr.rushing_yards, rr.receiving_yards\
                            FROM combine, rr\
                            WHERE combine.name = rr.name AND combine.year < 2009', con)
    df4 = pd.pivot_table(df4,index=['name'],aggfunc=np.sum).reset_index().fillna(0)
    df4['totYds'] = (df4['receiving_yards'] + df4['rushing_yards']).astype(int)
    df5 = pd.merge(df3,df4, on='name', how='inner', suffixes=('df3','df4'))
    dfRB = df5[df5.position == 'RB']
    dfRB = dfRB[dfRB.fortyyd < 5] #remove outliers
    dfWR = df5[df5.position == 'WR']
    dfWR = dfWR[dfWR.fortyyd < 5] #remove outliers

    #Create QB data frame
    dfQB = pd.read_sql_query('SELECT DISTINCT combine.name, combine.fortyyd, combine.heightinchestotal,\
                            combine.weight, combine.twentyss, combine.vertical, passing.passing_yards\
                            FROM combine, passing\
                            WHERE combine.name = passing.name AND combine.year < 2009', con)
    dfQB['count'] = 1 #use to get 40 yard time back after aggregating
    dfQB = pd.pivot_table(dfQB,index=['name'],aggfunc=np.sum).reset_index()
    dfQB['fortyyd'] = dfQB['fortyyd']/dfQB['count']
    dfQB['heightinchestotal'] = dfQB['heightinchestotal']/dfQB['count']
    dfQB['twentyss'] = dfQB['twentyss']/dfQB['count']
    dfQB['vertical'] = dfQB['vertical']/dfQB['count']
    dfQB['weight'] = dfQB['weight']/dfQB['count']
    dfQB['speedscore'] = (dfQB['weight']*200)/(dfQB['fortyyd']**4)
    dfQB = dfQB.drop('count', 1)
    dfQB = dfQB[dfQB.passing_yards > 175] #remove outliers

    return (dfRB, dfWR, dfQB)

def rb(xvar, hover_lab, title, x_lab, dfRB, dfWR, dfQB):
    """
    Defines plot within RB tab.

    Parameters:
    xvar        x-axis variable (string)
    hover_lab   hover label for x-axis variable (string)
    title       title of plot (string)
    x_lab       x-axis label (string)
    dfRB        running back dataframe (dataframe)
    dfWR        wide receiver dataframe (dataframe)
    dfQB        quarterback dataframe (dataframe)
    """
    source = ColumnDataSource(data=dict(x=dfRB[xvar], y=dfRB['totYds'],
                                        rush=dfRB['rushing_yards'],
                                        rec=dfRB['receiving_yards'], name=dfRB['name'],))
    hover = HoverTool(tooltips=[('Player', '@name'),(hover_lab, '$x{1.11}'),
                                ('Career Rushing Yards', '@rush'),('Career Receiving Yards', '@rec'),
                                ('Total Yards', '@y'),])
    p1 = figure(plot_width=600, plot_height=700, tools='pan,wheel_zoom,box_zoom,reset,resize,save',
               title=title, x_axis_label =x_lab, y_axis_label ='Career Rushing and Receiving Yards')
    p1.add_tools(hover)
    p1.circle('x', 'y', size=7, color='cyan', source=source)
    tab1 = Panel(child=p1, title='RB')
    return tab1

def wr(xvar, hover_lab, title, x_lab, dfRB, dfWR, dfQB):
    """
    Defines plot within WR tab.

    Parameters:
    xvar        x-axis variable (string)
    hover_lab   hover label for x-axis variable (string)
    title       title of plot (string)
    x_lab       x-axis label (string)
    dfRB        running back dataframe (dataframe)
    dfWR        wide receiver dataframe (dataframe)
    dfQB        quarterback dataframe (dataframe)
    """
    source = ColumnDataSource(data=dict(x=dfWR[xvar], y=dfWR['totYds'], rush=dfWR['rushing_yards'],
                                        rec=dfWR['receiving_yards'], name=dfWR['name'],))
    hover = HoverTool(tooltips=[('Player', '@name'),(hover_lab, '$x{1.11}'),
                                ('Career Rushing Yards', '@rush'),('Career Receiving Yards', '@rec'),
                                ('Total Yards', '@y'),])
    p2 = figure(plot_width=600, plot_height=700, tools="pan,wheel_zoom,box_zoom,reset,resize,save",
               title=title,
               x_axis_label =x_lab, y_axis_label ='Career Rushing and Receiving Yards')
    p2.add_tools(hover)
    p2.circle('x', 'y', size=7, color='cyan', source=source)
    tab2 = Panel(child=p2, title='WR')
    return tab2

def qb(xvar, hover_lab, title, x_lab, dfRB, dfWR, dfQB):
    """
    Defines plot within QB tab.

    Parameters:
    xvar        x-axis variable (string)
    hover_lab   hover label for x-axis variable (string)
    title       title of plot (string)
    x_lab       x-axis label (string)
    dfRB        running back dataframe (dataframe)
    dfWR        wide receiver dataframe (dataframe)
    dfQB        quarterback dataframe (dataframe)
    """
    source = ColumnDataSource(data=dict(x=dfQB[xvar], y=dfQB['passing_yards'], name=dfQB['name'],))
    hover = HoverTool(
            tooltips=[('Player', '@name'),(hover_lab, '$x{1.11}'),('Career Passing Yds', '@y'),])
    p3 = figure(plot_width=600, plot_height=700, tools="pan,wheel_zoom,box_zoom,reset,resize,save",
               title=title,
               x_axis_label =x_lab, y_axis_label ='Career Passing Yards')
    p3.add_tools(hover)
    p3.circle('x', 'y', size=7, color='cyan', source=source)
    tab3 = Panel(child=p3, title='QB')
    return tab3


def plot_40dash():
    """
    Plot of 40 yard times by yardage with tabs for each position.

    Calls:
    make_dfs(), rb(), wr(), qb()
    """
    dfRB, dfWR, dfQB = make_dfs()
    output_notebook()
#    output_file('40yd.html')
    tab1 = rb('fortyyd', '40 Yard Dash', 'RB: Total Yards by 40 Yard Dash', '40 Yard Dash', dfRB, dfWR, dfQB)
    tab2 = wr('fortyyd', '40 Yard Dash', 'WR: Total Yards by 40 Yard Dash', '40 Yard Dash', dfRB, dfWR, dfQB)
    tab3 = qb('fortyyd', '40 Yard Dash', 'QB: Total Yards by 40 Yard Dash', '40 Yard Dash', dfRB, dfWR, dfQB)
    tabs = Tabs(tabs=[ tab1, tab2, tab3 ])
    show(tabs)

def plot_twentyss():
    """
    Plot of 20 yard shuttle times by yardage with tabs for each position.

    Calls:
    make_dfs(), rb(), wr(), qb()
    """
    dfRB, dfWR, dfQB = make_dfs()
    dfRB = dfRB[dfRB.twentyss > 0]
    dfWR = dfWR[dfWR.twentyss > 0]
    dfQB = dfQB[dfQB.twentyss > 2] #Remove Alex Smith (incorrect time)

    output_notebook()
#    output_file('40yd.html')
    tab1 = rb('twentyss', '20 Yd Shuttle', 'RB: Total Yards by Short Shuttle', '20 Yard Short Shuttle', dfRB, dfWR, dfQB)
    tab2 = wr('twentyss', '20 Yd Shuttle', 'WR: Total Yards by Short Shuttle', '20 Yard Short Shuttle', dfRB, dfWR, dfQB)
    tab3 = qb('twentyss', '20 Yd Shuttle', 'QB: Total Yards by Short Shuttle', '20 Yard Short Shuttle', dfRB, dfWR, dfQB)
    tabs = Tabs(tabs=[ tab1, tab2, tab3 ])
    show(tabs)

def plot_vertical():
    """
    Plot of vertical jump by yardage with tabs for each position.

    Calls:
    make_dfs(), rb(), wr(), qb()
    """
    dfRB, dfWR, dfQB = make_dfs()
    dfRB = dfRB[dfRB.vertical > 0]
    dfWR = dfWR[dfWR.vertical > 0]
    dfQB = dfQB[dfQB.vertical > 20] #Remove Alex Smith (incorrect measurement)

    output_notebook()
#    output_file('40yd.html')
    tab1 = rb('vertical', 'Vertical Jump (in)', 'RB: Total Yards by Vertical Jump', 'Vertical Jump (in)', dfRB, dfWR, dfQB)
    tab2 = wr('vertical', 'Vertical Jump (in)', 'WR: Total Yards by Vertical Jump', 'Vertical Jump (in)', dfRB, dfWR, dfQB)
    tab3 = qb('vertical', 'Vertical Jump (in)', 'QB: Total Yards by Vertical Jump', 'Vertical Jump (in)', dfRB, dfWR, dfQB)
    tabs = Tabs(tabs=[ tab1, tab2, tab3 ])
    show(tabs)

def plot_height():
    """
    Plot of height by yardage with tabs for each position.

    Calls:
    make_dfs(), rb(), wr(), qb()
    """
    dfRB, dfWR, dfQB = make_dfs()
    output_notebook()
#    output_file('40yd.html')
    tab1 = rb('heightinchestotal', 'Height (in)', 'RB: Total Yards by Height', 'Height (in)', dfRB, dfWR, dfQB)
    tab3 = qb('heightinchestotal', 'Height (in)', 'QB: Total Yards by Height', 'Height (in)', dfRB, dfWR, dfQB)
    tab2 = wr('heightinchestotal', 'Height (in)', 'WR: Total Yards by Height', 'Height (in)', dfRB, dfWR, dfQB)
    tabs = Tabs(tabs=[ tab1, tab2, tab3 ])
    show(tabs)


def plot_speedscore():
    """
    Plot of speedscore by yardage with tabs for each position.

    Calls:
    make_dfs(), rb(), wr(), qb()
    """
    dfRB, dfWR, dfQB = make_dfs()
    output_notebook()
#    output_file('40yd.html')
    tab1 = rb('speedscore', 'Speed Score', 'RB: Total Yards by Speed Score', 'Speed Score', dfRB, dfWR, dfQB)
    tab3 = qb('speedscore', 'Speed Score', 'QB: Total Yards by Speed Score', 'Speed Score', dfRB, dfWR, dfQB)
    tab2 = wr('speedscore', 'Speed Score', 'WR: Total Yards by Speed Score', 'Speed Score', dfRB, dfWR, dfQB)
    tabs = Tabs(tabs=[ tab1, tab2, tab3 ])
    show(tabs)


def select_columns():

    positions = {
        1: 'QB', 2:'WR', 3:'RB'
    }
    combinedata = {
        1: 'fortyyd', 2:'twentyyd', 3:'tenyd', 4: 'twentyss', 5:'threecone',
        6: 'vertical', 7:'picktotal', 8:'BMI', 9:'speedscore'
    }
    rrdata = {
        1: 'rushing_yards', 2:'receiving_yards', 3:'totYds'
    }
    passingdata = {
        1: 'passing_rating', 2: 'passing_yards', 3: 'passing_TD'
    }

    print('Linear regression between combine data and performance')

    #Get user input(combine data and performance)
    positionpick = 0
    while (positionpick < 1) or (positionpick > 4):
        print(positions)
        positionpick = int(input('Enter number for position: '))
    combinepick = 0
    while (combinepick < 1) or (combinepick > 9):
        print(combinedata)
        combinepick = int(input('Enter number for combine data: '))
    rrpick = 0
    while (rrpick < 1) or (rrpick > 3):
        print(rrdata)
        rrpick = int(input('Enter number for rushing/receiving data: '))

    regdata = import_data(positions[positionpick],combinedata[combinepick],rrdata[rrpick])
    R = fit_line(regdata,combinedata[combinepick],rrdata[rrpick])

def import_data(position,combinedata,rrdata):

    con = sqlite3.connect('data/nflPPdb.sqlite')
    df1 = pd.read_sql_query('SELECT DISTINCT combine.name, rr.year, rr.rushing_yards, rr.receiving_yards, rr.games_played\
                        FROM combine, rr\
                        WHERE combine.name = rr.name AND combine.year < 2008', con)
    df2 = pd.read_sql_query('SELECT combine.name, combine.fortyyd, combine.twentyyd, combine.tenyd, \
                        combine.twentyss, combine.threecone, combine.vertical, combine.picktotal, \
                        combine.BMI, combine.speedscore \
                        FROM combine\
                        WHERE combine.year < 2009 AND combine.pickround != 0', con)
    df3 = pd.merge(df1, df2, on='name', how='inner', suffixes=('df1','df2'))
    df4 = pd.read_sql_query('SELECT players.name, players.position\
                        FROM players', con)
    df5 = pd.merge(df3,df4, on='name', how='inner', suffixes=('df3','df4'))
    df5 = df5.drop_duplicates()
    df5['totYds'] = (df5.receiving_yards + df5.rushing_yards)
    df5 = df5[df5.position.isin([position])]
    regdata = df5.groupby('name').head(3).reset_index(drop=True)
    regdata = regdata.groupby('name').sum()
    regdata = df5[[combinedata,rrdata]]
    return regdata

def fit_line(regdata,combinedata,rrdata):

    X = regdata[combinedata]
    X = sm.add_constant(X)
    Y = regdata[rrdata]
    mod = sm.OLS(Y,X)
    res = mod.fit()
    plt.scatter(regdata[combinedata],Y)
    plt.plot(regdata[combinedata],res.fittedvalues,'r--', label="OLS")
    plt.show(block=False)
    s = 'R^2 = ' + res.rsquared
    print s

    return res.rsquaredimport pandas as pd


def plot_graph():
    """
    Plots statistics of two NFL teams for any year from 1990-2008.

    This function asks the user to select two teams and a year. It then
    aggregates pro-football-reference data on those attributes and plots
    the results as a bar chart. The resulting graph is saved as a .png file.
    """

    # Create team dictionary for user input options
    teams = {
        1: 'atl', 2: 'buf', 3: 'car', 4: 'chi', 5:'cin', 6:'cle', 7:'clt',
        8: 'crd', 9: 'dal', 10: 'den', 11: 'det', 12:'gnb', 13:'htx',
        14:'jax', 15: 'kan', 16: 'mia', 17: 'min', 18: 'nor', 19:'nwe',
        20:'nyg', 21:'nyj', 22: 'oti', 23: 'phi', 24: 'pit', 25: 'rai',
        26:'ram', 27:'rav', 28:'sdg', 29: 'sea', 30: 'sfo', 31: 'tam',
        32: 'was'
        }

    print('COMPARE PRODUCTION BETWEEN TWO TEAMS FOR A GIVEN SEASON')

    #Get user input (teams and season)
    teamA = 0
    while (teamA < 1) or (teamA > 32):
        print(teams)
        teamA = int(input('Enter number for the first team: '))
    teamB = 0
    while (teamB < 1) or (teamB > 32):
        print(teams)
        teamB = int(input('Now select the second team: '))
    year = 0
    while (year < 1990) or (year > 2008):
        year = int(input('Enter season (any year between 1990 and 2008): '))

    #Filter dataset based on user selections
    pfr = pd.read_csv('data/pfr1990_2008.csv')
    userSelection = [teams[teamA], teams[teamB], year]
    pfr.columns = ['ID', 'LastName', 'FirstName', 'Year', 'Team', 'Position',
        'G', 'GS', 'COMP', 'ATT', 'PassYD','PassTD', 'INT', 'rush', 'rushYD',
        'rushTD', 'rec', 'recYD', 'recTD']
    pfrTeams = pfr[pfr.Team.isin(userSelection)]
    pfrTeamsYear = pfrTeams[pfrTeams.Year.isin(userSelection)]
    pfrAgg = pfrTeamsYear[['COMP','ATT','PassYD','PassTD','INT','rush',
                           'rushYD','rushTD','rec','recYD','recTD']]. \
             groupby(pfrTeamsYear['Team']).sum().transpose()

    #Plot data as bar chart and save to .png
    plt.figure()
    pfrAgg.plot(kind='bar', figsize=(7, 13))
    plt.legend(fontsize = 14, loc = 'best')
    plt.suptitle(year, fontsize=24)
    plt.savefig('sample_plot.png', bbox_inches='tight')

#Create database connection
con = sqlite3.connect('data/nflPPdb.sqlite')

#Create RB and WR dataframes
def make_dfs():
    """
    Creates dataframes for plotting using SQL queries.

    Returns a dataframe for each positional group (dfRB, dfWR, dfQB).
    """
    df1 = pd.read_sql_query('SELECT combine.name, combine.fortyyd, combine.heightinchestotal,\
                            combine.weight, combine.twentyss, combine.vertical, combine.year\
                            FROM combine\
                            WHERE combine.year < 2009 AND combine.pickround != 0', con)
    df1['speedscore'] = (df1['weight']*200)/(df1['fortyyd']**4)
    df2 = pd.read_sql_query('SELECT combine.name, combine.year, players.position\
                            FROM combine, players\
                            WHERE combine.name = players.name AND combine.year = players.draft_year', con)
    df3 = pd.merge(df1, df2, on=['name', 'year'], how='inner', suffixes=('df1','df2'))
    df3 = df3.drop_duplicates(subset='name', keep=False)
    df4 = pd.read_sql_query('SELECT DISTINCT combine.name, rr.rushing_yards, rr.receiving_yards\
                            FROM combine, rr\
                            WHERE combine.name = rr.name AND combine.year < 2009', con)
    df4 = df4.fillna(0)
    df4['totYds'] = (df4['receiving_yards'] + df4['rushing_yards']).astype(int)
    df5 = pd.merge(df3,df4, on='name', how='inner', suffixes=('df3','df4'))
    dfRB = df5[df5.position == 'RB']
    dfRB = dfRB.groupby('name').head(3).reset_index(drop=True)
    dfRB = dfRB.groupby('name').mean()
    dfRB = dfRB[dfRB.fortyyd < 5] #remove outliers
    dfWR = df5[df5.position == 'WR']
    dfWR = dfWR.groupby('name').head(3).reset_index(drop=True)
    dfWR = dfWR.groupby('name').mean()
    dfWR = dfWR[dfWR.fortyyd < 5] #remove outliers

    #Create QB data frame
    dfQB = pd.read_sql_query('SELECT DISTINCT combine.name, combine.fortyyd, combine.heightinchestotal,\
                            combine.weight, combine.twentyss, combine.vertical, passing.passing_yards\
                            FROM combine, passing\
                            WHERE combine.name = passing.name AND combine.year < 2009', con)
    dfQB['count'] = 1 #use to get 40 yard time back after aggregating
    #dfQB = pd.pivot_table(dfQB,index=['name'],aggfunc=np.sum).reset_index()
    dfQB = dfQB.groupby('name').head(3).reset_index(drop=True)
    dfQB = dfQB.groupby('name').sum()
    dfQB['fortyyd'] = dfQB['fortyyd']/dfQB['count']
    dfQB['heightinchestotal'] = dfQB['heightinchestotal']/dfQB['count']
    dfQB['twentyss'] = dfQB['twentyss']/dfQB['count']
    dfQB['vertical'] = dfQB['vertical']/dfQB['count']
    dfQB['weight'] = dfQB['weight']/dfQB['count']
    dfQB['speedscore'] = (dfQB['weight']*200)/(dfQB['fortyyd']**4)
    dfQB = dfQB.drop('count', 1)
    dfQB = dfQB[dfQB.passing_yards > 175] #remove outliers

    return (dfRB, dfWR, dfQB)

def rb(xvar, hover_lab, title, x_lab, dfRB, dfWR, dfQB):
    """
    Defines plot within RB tab.

    Parameters:
    xvar        x-axis variable (string)
    hover_lab   hover label for x-axis variable (string)
    title       title of plot (string)
    x_lab       x-axis label (string)
    dfRB        running back dataframe (dataframe)
    dfWR        wide receiver dataframe (dataframe)
    dfQB        quarterback dataframe (dataframe)
    """
    source = ColumnDataSource(data=dict(x=dfRB[xvar], y=dfRB['totYds'],
                                        rush=dfRB['rushing_yards'],
                                        rec=dfRB['receiving_yards'], name=dfRB.index,))
    hover = HoverTool(tooltips=[('Player', '@name'),(hover_lab, '$x{1.11}'),
                                ('Career Rushing Yards', '@rush'),('Career Receiving Yards', '@rec'),
                                ('Total Yards', '@y'),])
    p1 = figure(plot_width=600, plot_height=700, tools='pan,wheel_zoom,box_zoom,reset,resize,save',
               title=title, x_axis_label =x_lab, y_axis_label ='Career Rushing and Receiving Yards')
    p1.add_tools(hover)
    p1.circle('x', 'y', size=7, color='cyan', source=source)
    tab1 = Panel(child=p1, title='RB')
    return tab1

def wr(xvar, hover_lab, title, x_lab, dfRB, dfWR, dfQB):
    """
    Defines plot within WR tab.

    Parameters:
    xvar        x-axis variable (string)
    hover_lab   hover label for x-axis variable (string)
    title       title of plot (string)
    x_lab       x-axis label (string)
    dfRB        running back dataframe (dataframe)
    dfWR        wide receiver dataframe (dataframe)
    dfQB        quarterback dataframe (dataframe)
    """
    source = ColumnDataSource(data=dict(x=dfWR[xvar], y=dfWR['totYds'], rush=dfWR['rushing_yards'],
                                        rec=dfWR['receiving_yards'], name=dfWR.index,))
    hover = HoverTool(tooltips=[('Player', '@name'),(hover_lab, '$x{1.11}'),
                                ('Career Rushing Yards', '@rush'),('Career Receiving Yards', '@rec'),
                                ('Total Yards', '@y'),])
    p2 = figure(plot_width=600, plot_height=700, tools="pan,wheel_zoom,box_zoom,reset,resize,save",
               title=title,
               x_axis_label =x_lab, y_axis_label ='Career Rushing and Receiving Yards')
    p2.add_tools(hover)
    p2.circle('x', 'y', size=7, color='cyan', source=source)
    tab2 = Panel(child=p2, title='WR')
    return tab2

def qb(xvar, hover_lab, title, x_lab, dfRB, dfWR, dfQB):
    """
    Defines plot within QB tab.

    Parameters:
    xvar        x-axis variable (string)
    hover_lab   hover label for x-axis variable (string)
    title       title of plot (string)
    x_lab       x-axis label (string)
    dfRB        running back dataframe (dataframe)
    dfWR        wide receiver dataframe (dataframe)
    dfQB        quarterback dataframe (dataframe)
    """
    source = ColumnDataSource(data=dict(x=dfQB[xvar], y=dfQB['passing_yards'], name=dfQB.index,))
    hover = HoverTool(
            tooltips=[('Player', '@name'),(hover_lab, '$x{1.11}'),('Career Passing Yds', '@y'),])
    p3 = figure(plot_width=600, plot_height=700, tools="pan,wheel_zoom,box_zoom,reset,resize,save",
               title=title,
               x_axis_label =x_lab, y_axis_label ='Career Passing Yards')
    p3.add_tools(hover)
    p3.circle('x', 'y', size=7, color='cyan', source=source)
    tab3 = Panel(child=p3, title='QB')
    return tab3


def plot_40dash():
    """
    Plot of 40 yard times by yardage with tabs for each position.

    Calls:
    make_dfs(), rb(), wr(), qb()
    """
    dfRB, dfWR, dfQB = make_dfs()
    output_notebook()
#    output_file('40yd.html')
    tab1 = rb('fortyyd', '40 Yard Dash', 'RB: Total Yards by 40 Yard Dash', '40 Yard Dash', dfRB, dfWR, dfQB)
    tab2 = wr('fortyyd', '40 Yard Dash', 'WR: Total Yards by 40 Yard Dash', '40 Yard Dash', dfRB, dfWR, dfQB)
    tab3 = qb('fortyyd', '40 Yard Dash', 'QB: Total Yards by 40 Yard Dash', '40 Yard Dash', dfRB, dfWR, dfQB)
    tabs = Tabs(tabs=[ tab1, tab2, tab3 ])
    show(tabs)

def plot_twentyss():
    """
    Plot of 20 yard shuttle times by yardage with tabs for each position.

    Calls:
    make_dfs(), rb(), wr(), qb()
    """
    dfRB, dfWR, dfQB = make_dfs()
    dfRB = dfRB[dfRB.twentyss > 0]
    dfWR = dfWR[dfWR.twentyss > 0]
    dfQB = dfQB[dfQB.twentyss > 2] #Remove Alex Smith (incorrect time)

    output_notebook()
#    output_file('40yd.html')
    tab1 = rb('twentyss', '20 Yd Shuttle', 'RB: Total Yards by Short Shuttle', '20 Yard Short Shuttle', dfRB, dfWR, dfQB)
    tab2 = wr('twentyss', '20 Yd Shuttle', 'WR: Total Yards by Short Shuttle', '20 Yard Short Shuttle', dfRB, dfWR, dfQB)
    tab3 = qb('twentyss', '20 Yd Shuttle', 'QB: Total Yards by Short Shuttle', '20 Yard Short Shuttle', dfRB, dfWR, dfQB)
    tabs = Tabs(tabs=[ tab1, tab2, tab3 ])
    show(tabs)

def plot_vertical():
    """
    Plot of vertical jump by yardage with tabs for each position.

    Calls:
    make_dfs(), rb(), wr(), qb()
    """
    dfRB, dfWR, dfQB = make_dfs()
    dfRB = dfRB[dfRB.vertical > 0]
    dfWR = dfWR[dfWR.vertical > 0]
    dfQB = dfQB[dfQB.vertical > 20] #Remove Alex Smith (incorrect measurement)

    output_notebook()
#    output_file('40yd.html')
    tab1 = rb('vertical', 'Vertical Jump (in)', 'RB: Total Yards by Vertical Jump', 'Vertical Jump (in)', dfRB, dfWR, dfQB)
    tab2 = wr('vertical', 'Vertical Jump (in)', 'WR: Total Yards by Vertical Jump', 'Vertical Jump (in)', dfRB, dfWR, dfQB)
    tab3 = qb('vertical', 'Vertical Jump (in)', 'QB: Total Yards by Vertical Jump', 'Vertical Jump (in)', dfRB, dfWR, dfQB)
    tabs = Tabs(tabs=[ tab1, tab2, tab3 ])
    show(tabs)

def plot_height():
    """
    Plot of height by yardage with tabs for each position.

    Calls:
    make_dfs(), rb(), wr(), qb()
    """
    dfRB, dfWR, dfQB = make_dfs()
    output_notebook()
#    output_file('40yd.html')
    tab1 = rb('heightinchestotal', 'Height (in)', 'RB: Total Yards by Height', 'Height (in)', dfRB, dfWR, dfQB)
    tab3 = qb('heightinchestotal', 'Height (in)', 'QB: Total Yards by Height', 'Height (in)', dfRB, dfWR, dfQB)
    tab2 = wr('heightinchestotal', 'Height (in)', 'WR: Total Yards by Height', 'Height (in)', dfRB, dfWR, dfQB)
    tabs = Tabs(tabs=[ tab1, tab2, tab3 ])
    show(tabs)

def plot_speedscore():
    """
    Plot of speedscore by yardage with tabs for each position.

    Calls:
    make_dfs(), rb(), wr(), qb()
    """
    dfRB, dfWR, dfQB = make_dfs()
    output_notebook()
#    output_file('40yd.html')
    tab1 = rb('speedscore', 'Speed Score', 'RB: Total Yards by Speed Score', 'Speed Score', dfRB, dfWR, dfQB)
    tab3 = qb('speedscore', 'Speed Score', 'QB: Total Yards by Speed Score', 'Speed Score', dfRB, dfWR, dfQB)
    tab2 = wr('speedscore', 'Speed Score', 'WR: Total Yards by Speed Score', 'Speed Score', dfRB, dfWR, dfQB)
    tabs = Tabs(tabs=[ tab1, tab2, tab3 ])
    show(tabs)

import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import statsmodels.api as sm


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

    return res.rsquared
import numpy as np
import pandas as pd
import sqlite3
from bokeh.plotting import figure, output_file, output_notebook, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models.widgets import Panel, Tabs

#Create database connection
con = sqlite3.connect('data/nflPPdb.sqlite')

#Create RB and WR dataframes
def make_dfs():
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

def rb(yvar, hover_lab, title, x_lab, dfRB, dfWR, dfQB):
    source = ColumnDataSource(data=dict(x=dfRB[yvar], y=dfRB['totYds'],
                                        rush=dfRB['rushing_yards'],
                                        rec=dfRB['receiving_yards'], name=dfRB['name'],))
    hover = HoverTool(tooltips=[('Player', '@name'),(hover_lab, '$x{1.11}'),
                                ('Career Rushing Yards', '@rush'),('Career Receiving Yards', '@rec'),
                                ('Total Yards', '@y'),])
    p1 = figure(plot_width=600, plot_height=700, tools='pan,wheel_zoom,box_zoom,reset,resize',
               title=title, x_axis_label =x_lab, y_axis_label ='Career Rushing and Receiving Yards')
    p1.add_tools(hover)
    p1.circle('x', 'y', size=7, color='cyan', source=source)
    tab1 = Panel(child=p1, title='RB')
    return tab1

def wr(yvar, hover_lab, title, x_lab, dfRB, dfWR, dfQB):
    source = ColumnDataSource(data=dict(x=dfWR[yvar], y=dfWR['totYds'], rush=dfWR['rushing_yards'],
                                        rec=dfWR['receiving_yards'], name=dfWR['name'],))
    hover = HoverTool(tooltips=[('Player', '@name'),(hover_lab, '$x{1.11}'),
                                ('Career Rushing Yards', '@rush'),('Career Receiving Yards', '@rec'),
                                ('Total Yards', '@y'),])
    p2 = figure(plot_width=600, plot_height=700, tools="pan,wheel_zoom,box_zoom,reset,resize",
               title=title,
               x_axis_label =x_lab, y_axis_label ='Career Rushing and Receiving Yards')
    p2.add_tools(hover)
    p2.circle('x', 'y', size=7, color='cyan', source=source)
    tab2 = Panel(child=p2, title='WR')
    return tab2

def qb(yvar, hover_lab, title, x_lab, dfRB, dfWR, dfQB):
    source = ColumnDataSource(data=dict(x=dfQB[yvar], y=dfQB['passing_yards'], name=dfQB['name'],))
    hover = HoverTool(
            tooltips=[('Player', '@name'),(hover_lab, '$x{1.11}'),('Career Passing Yds', '@y'),])
    p3 = figure(plot_width=600, plot_height=700, tools="pan,wheel_zoom,box_zoom,reset,resize",
               title=title,
               x_axis_label =x_lab, y_axis_label ='Career Passing Yards')
    p3.add_tools(hover)
    p3.circle('x', 'y', size=7, color='cyan', source=source)
    tab3 = Panel(child=p3, title='QB')
    return tab3


def plot_40dash():
    dfRB, dfWR, dfQB = make_dfs()
    output_notebook()
#    output_file('40yd.html')
    tab1 = rb('fortyyd', '40 Yard Dash', 'RB: Total Yards by 40 Yard Dash', '40 Yard Dash', dfRB, dfWR, dfQB)
    tab2 = wr('fortyyd', '40 Yard Dash', 'WR: Total Yards by 40 Yard Dash', '40 Yard Dash', dfRB, dfWR, dfQB)
    tab3 = qb('fortyyd', '40 Yard Dash', 'QB: Total Yards by 40 Yard Dash', '40 Yard Dash', dfRB, dfWR, dfQB)
    tabs = Tabs(tabs=[ tab1, tab2, tab3 ])
    show(tabs)


def plot_twentyss():
    dfRB, dfWR, dfQB = make_dfs()
    dfRB = dfRB[dfRB.twentyss > 0]
    dfWR = dfWR[dfWR.twentyss > 0]
    dfQB = dfQB[dfQB.twentyss > 0]

    output_notebook()
#    output_file('40yd.html')
    tab1 = rb('twentyss', '20 Yd Shuttle', 'RB: Total Yards by Short Shuttle', '20 Yard Short Shuttle', dfRB, dfWR, dfQB)
    tab2 = wr('twentyss', '20 Yd Shuttle', 'WR: Total Yards by Short Shuttle', '20 Yard Short Shuttle', dfRB, dfWR, dfQB)
    tab3 = qb('twentyss', '20 Yd Shuttle', 'QB: Total Yards by Short Shuttle', '20 Yard Short Shuttle', dfRB, dfWR, dfQB)
    tabs = Tabs(tabs=[ tab1, tab2, tab3 ])
    show(tabs)

def plot_vertical():
    dfRB, dfWR, dfQB = make_dfs()
    dfRB = dfRB[dfRB.vertical > 0]
    dfWR = dfWR[dfWR.vertical > 0]
    dfQB = dfQB[dfQB.vertical > 0]

    output_notebook()
#    output_file('40yd.html')
    tab1 = rb('vertical', 'Vertical Jump (in)', 'RB: Total Yards by Vertical Jump', 'Vertical Jump (in)', dfRB, dfWR, dfQB)
    tab2 = wr('vertical', 'Vertical Jump (in)', 'WR: Total Yards by Vertical Jump', 'Vertical Jump (in)', dfRB, dfWR, dfQB)
    tab3 = qb('vertical', 'Vertical Jump (in)', 'QB: Total Yards by Vertical Jump', 'Vertical Jump (in)', dfRB, dfWR, dfQB)
    tabs = Tabs(tabs=[ tab1, tab2, tab3 ])
    show(tabs)

def plot_height():
    dfRB, dfWR, dfQB = make_dfs()
    output_notebook()
#    output_file('40yd.html')
    tab1 = rb('heightinchestotal', 'Height (in)', 'RB: Total Yards by Height', 'Height (in)', dfRB, dfWR, dfQB)
    tab3 = qb('heightinchestotal', 'Height (in)', 'QB: Total Yards by Height', 'Height (in)', dfRB, dfWR, dfQB)
    tab2 = wr('heightinchestotal', 'Height (in)', 'WR: Total Yards by Height', 'Height (in)', dfRB, dfWR, dfQB)
    tabs = Tabs(tabs=[ tab1, tab2, tab3 ])
    show(tabs)

def plot_speedscore():
    dfRB, dfWR, dfQB = make_dfs()
    output_notebook()
#    output_file('40yd.html')
    tab1 = rb('speedscore', 'Speed Score', 'RB: Total Yards by Speed Score', 'Speed Score', dfRB, dfWR, dfQB)
    tab3 = qb('speedscore', 'Speed Score', 'QB: Total Yards by Speed Score', 'Speed Score', dfRB, dfWR, dfQB)
    tab2 = wr('speedscore', 'Speed Score', 'WR: Total Yards by Speed Score', 'Speed Score', dfRB, dfWR, dfQB)
    tabs = Tabs(tabs=[ tab1, tab2, tab3 ])
    show(tabs)

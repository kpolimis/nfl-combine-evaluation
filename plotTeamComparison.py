import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

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

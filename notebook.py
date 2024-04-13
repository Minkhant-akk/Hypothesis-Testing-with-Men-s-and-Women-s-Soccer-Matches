import pandas as pd
import pingouin 
from scipy.stats import mannwhitneyu

women_results = pd.read_csv('women_results.csv');
men_results = pd.read_csv('men_results.csv');

women_tournament_count = women_results['tournament'].value_counts()
men_tournament_count = men_results['tournament'].value_counts()

women_results['date'] = pd.to_datetime(women_results['date'])

womenFilteredDate = women_results[(women_results['tournament'].isin(['FIFA World Cup'])) & (women_results['date'] > '2002-01-01')]

men_results['date'] = pd.to_datetime(men_results['date'])
menFilteredDate = men_results[(men_results['tournament'].isin(['FIFA World Cup'])) & (men_results['date'] > '2002-01-01')]

womenFilteredDate['group'] = "women"
menFilteredDate['group'] = "men"

womenFilteredDate['goalScored'] = womenFilteredDate['home_score'] + womenFilteredDate['away_score']
menFilteredDate['goalScored'] = menFilteredDate['home_score'] + menFilteredDate['away_score']

womenAndMenTeam = pd.concat([womenFilteredDate,menFilteredDate], axis=0,ignore_index=True)

womenAndMenGroupAndScore = womenAndMenTeam[['group','goalScored']]
womenAndMenGroupAndScorePivot = womenAndMenGroupAndScore.pivot(columns='group', values="goalScored")

resultWithPg = pingouin.mwu(x=womenAndMenGroupAndScorePivot['women'],y=womenAndMenGroupAndScorePivot['men'],alternative="greater")

resultWithScipy = mannwhitneyu(x=womenFilteredDate['goalScored'],y=menFilteredDate['goalScored'],alternative="greater")

p_val = round(resultWithPg['p-val'].values[0],4)

if p_val <= 0.01:
    result = "reject"
else:
    result ="fail to reject"
    
result_dict = {"p_val": p_val, "result": result}

print(womenAndMenGroupAndScorePivot)
print(womenAndMenGroupAndScore)
print(womenAndMenTeam)
print(menFilteredDate)
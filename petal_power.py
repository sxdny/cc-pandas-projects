import pandas as pd
import math

# ad_clicks = pd.read_csv('ad_clicks.csv') --> need access to the .csv file

print(ad_clicks.head())

n_of_views_by_source = ad_clicks.groupby('utm_source').user_id.count().reset_index().rename(columns={'user_id': 'n_of_visits'})

# 3
ad_clicks['is_click'] = ~ad_clicks.ad_click_timestamp.isnull()

# 4
clicks_by_source = ad_clicks.groupby(['utm_source', 'is_click']).user_id.count().reset_index()

clicks_pivot = clicks_by_source.pivot(
  columns='is_click',
  index='utm_source',
  values='user_id'
).reset_index()

calculate_percentage = lambda row: str(round(row[True] * 100 / (row[True] + row[False]))) + "%"

clicks_pivot['percent_clicked'] = clicks_pivot.apply(calculate_percentage, axis=1)

#7. yes, they were the same ammount
count_of_users = ad_clicks.groupby('experimental_group').user_id.count().reset_index().rename(columns={'user_id' : 'total_users_in_group'})

# 8. check to see if a greater percentage of users clicked on ad A or B

print(ad_clicks)

n_person_clicked_by_group = ad_clicks.groupby(['experimental_group', 'is_click']).user_id.count().reset_index()

pv_n_person_clicked_by_group = n_person_clicked_by_group.pivot(
  columns='is_click',
  index='experimental_group',
  values='user_id'
).reset_index().rename(columns={
  False : 'not_clicked',
  True : 'clicked'
})

get_percentage = lambda row: row.clicked * 100 / (row.not_clicked + row.clicked)

pv_n_person_clicked_by_group['pcnt_clicked'] = pv_n_person_clicked_by_group.apply(
  get_percentage,
  axis=1,
)

print(pv_n_person_clicked_by_group)

# 9. create respective dataframes for results of the test a and b
a_clicks = ad_clicks[ad_clicks.experimental_group == 'A']

b_clicks = ad_clicks[ad_clicks.experimental_group == 'B']

# 10. calculate the percent of users who clicked on the ad by ad

is_click_a = a_clicks[a_clicks.is_click == True]

rvw_a = is_click_a.groupby('day').user_id.count().reset_index()

calculate_percentage_a = lambda row: round(row.user_id * 100 / 827)

rvw_a['pct'] = rvw_a.apply(
  calculate_percentage_a,
  axis=1
)

print(rvw_a)

is_click_b = b_clicks[b_clicks.is_click == True]

rvw_b = is_click_b.groupby('day').user_id.count().reset_index()

calculate_percentage_b = lambda row: round(row.user_id * 100 / 827)

rvw_b['pct'] = rvw_b.apply(
  calculate_percentage_b,
  axis=1
)

print(rvw_b)



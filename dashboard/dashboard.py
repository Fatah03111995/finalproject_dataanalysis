import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

# MELIHAT JUMLAH RENTAL BY MONTH
def by_month(df):
    by_month = df.groupby(by=['yr','mnth'])['cnt'].sum().reset_index()
    return by_month

# MELIHAT JUMLAH RENTAL BY SEASON
def by_season(df):
    by_season = df.groupby(by=['yr','season'])['cnt'].sum().reset_index()
    return by_season

# MELIHAT JUMLAH RENTAL BY HOLIDAY
def by_holiday(df):
    by_holiday = df.groupby(by=['yr','holiday'])['cnt'].sum().reset_index()
    return by_holiday

# MELIHAT JUMLAH RENTAL BY WORKDAY
def by_workingday(df):
    by_workday = df.groupby(by=['yr','workingday'])['cnt'].sum().reset_index()
    return by_workday

# MELIHAT JUMLAH HARI BY CLUSTERING
def by_clustering(df):
    newdf = create_clustering(df)
    by_clustering = newdf.groupby(by=['yr','cluster'])['dteday'].count().reset_index()
    return by_clustering

# CLUSTERING BERDASARKAN JUMLAH PELANGGAN YANG MELAKUKAN RENTAL
# PENGGUNAAN TINGGI : > 7000
# PENGGUNAAN SEDANG : 3000 - 6000
# PENGGUNAAN RENDAH : < 3000
def create_clustering(df):
    df['cluster'] = df['cnt'].apply(lambda x: 'high' if x > 6000 else('moderate' if x > 3000 else ' low'))
    return df

all_df = pd.read_csv('https://drive.google.com/uc?id=1CCbIYrI8CzKonDb7zKskSJ9gxoVkIz9w')
all_df['dteday'] = pd.to_datetime(all_df['dteday'])
min_date = all_df['dteday'].min()
max_date = all_df['dteday'].max()

with st.sidebar:
    # MENAMBAHKAN LOGO
    st.image('logo.png')
    # MENGAMBIL START DATE DAN END DATE INPUT
    start_date, end_date = st.date_input(
        label='Range Date',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )


main_df = all_df[
   ( all_df['dteday'] >= str(start_date) ) &
   ( all_df['dteday'] <= str(end_date) )
]

by_monthdf = by_month(main_df)
by_seasondf = by_season(main_df)
by_holidaydf = by_holiday(main_df)
by_workingdaydf = by_workingday(main_df)
by_clusteringdf = by_clustering(main_df)

print(by_clusteringdf)
st.header('Project Tugas Akhir')

col1, col2 = st.columns(2)

with col1:
    total_orders = main_df['cnt'].sum()
    st.metric('Total Rent', value=total_orders)

with col2:
    seasons = main_df['season'].unique()
    seasons_txt = ', '.join(seasons)
    st.metric('Seasons','All Season' if len(seasons) == 4 else seasons_txt)

# PERFORMING BY MONTH
st.subheader('Performing by Month')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35,15))
maxdata_bymonth_2011 = by_monthdf[by_monthdf['yr'] == 2011]['cnt'].max()
maxdata_bymonth_2012 = by_monthdf[by_monthdf['yr'] == 2012]['cnt'].max()
year = [2011, 2012]

for i in range(len(year)):
    maxdata_bymonth = [maxdata_bymonth_2011, maxdata_bymonth_2012]
    colors = ['green' if cnt == maxdata_bymonth[i] else 'grey' for cnt in by_monthdf[by_monthdf['yr'] == year[i]]['cnt']]
    sns.barplot(x='mnth', y='cnt', data=by_monthdf[by_monthdf['yr'] == year[i]], ax=ax[i], palette=colors)
    ax[i].set_ylabel('Total Rent', fontsize=30)
    ax[i].set_xlabel('Month', fontsize=30)
    ax[i].tick_params(axis='y', labelsize=35)
    ax[i].tick_params(axis='x', labelsize=35)
    ax[i].set_title(f'{year[i]}', fontsize=50)

st.pyplot(fig)

# PERFRORMING BY SEASON
st.subheader('Performing by Season')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35,15))
maxdata_byseason_2011 = by_seasondf[by_seasondf['yr'] == 2011]['cnt'].max()
maxdata_byseason_2012 = by_seasondf[by_seasondf['yr'] == 2012]['cnt'].max()
year = [2011, 2012]

for i in range(len(year)):
    maxdata_byseason = [maxdata_byseason_2011, maxdata_byseason_2012]
    colors = ['green' if cnt == maxdata_byseason[i] else 'grey' for cnt in by_seasondf[by_seasondf['yr'] == year[i]]['cnt']]
    sns.barplot(x='season', y='cnt', data=by_seasondf[by_seasondf['yr'] == year[i]], ax=ax[i], palette=colors)
    ax[i].set_ylabel('Total Rent', fontsize=30)
    ax[i].set_xlabel('Season', fontsize=30)
    ax[i].tick_params(axis='y', labelsize=35)
    ax[i].tick_params(axis='x', labelsize=35)
    ax[i].set_title(f'{year[i]}', fontsize=50)

st.pyplot(fig)

# PERFRORMING ON HOLIDAY
st.subheader('Performing on Holiday')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35,15))
maxdata_byholiday_2011 = by_holidaydf[by_holidaydf['yr'] == 2011]['cnt'].max()
maxdata_byholiday_2012 = by_holidaydf[by_holidaydf['yr'] == 2012]['cnt'].max()
year = [2011, 2012]

for i in range(len(year)):
    maxdata_byholiday = [maxdata_byholiday_2011, maxdata_byholiday_2012]
    colors = ['green' if cnt == maxdata_byholiday[i] else 'grey' for cnt in by_holidaydf[by_holidaydf['yr'] == year[i]]['cnt']]
    sns.barplot(x='holiday', y='cnt', data=by_holidaydf[by_holidaydf['yr'] == year[i]], ax=ax[i], palette=colors)
    ax[i].set_ylabel('Total Rent', fontsize=30)
    ax[i].set_xlabel('holiday', fontsize=30)
    ax[i].tick_params(axis='y', labelsize=35)
    ax[i].tick_params(axis='x', labelsize=35)
    ax[i].set_title(f'{year[i]}', fontsize=50)

st.pyplot(fig)

# PERFRORMING ON WORKINGDAY
st.subheader('Performing on Working Day')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35,15))
maxdata_byworkingday_2011 = by_workingdaydf[by_workingdaydf['yr'] == 2011]['cnt'].max()
maxdata_byworkingday_2012 = by_workingdaydf[by_workingdaydf['yr'] == 2012]['cnt'].max()
year = [2011, 2012]

for i in range(len(year)):
    maxdata_byworkingday = [maxdata_byworkingday_2011, maxdata_byworkingday_2012]
    colors = ['green' if cnt == maxdata_byworkingday[i] else 'grey' for cnt in by_workingdaydf[by_workingdaydf['yr'] == year[i]]['cnt']]
    sns.barplot(x='workingday', y='cnt', data=by_workingdaydf[by_workingdaydf['yr'] == year[i]], ax=ax[i], palette=colors)
    ax[i].set_ylabel('Total Rent', fontsize=30)
    ax[i].set_xlabel('workingday', fontsize=30)
    ax[i].tick_params(axis='y', labelsize=35)
    ax[i].tick_params(axis='x', labelsize=35)
    ax[i].set_title(f'{year[i]}', fontsize=50)

st.pyplot(fig)

#CLUSTER
st.subheader('Clustering')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35,15))
year = [2011, 2012]

for i in range(len(year)):
    sns.barplot(x='cluster', y='dteday', data=by_clusteringdf[by_clusteringdf['yr'] == year[i]], ax=ax[i], palette='viridis')
    ax[i].set_ylabel('Total Day', fontsize=30)
    ax[i].set_xlabel('Clustering', fontsize=30)
    ax[i].tick_params(axis='y', labelsize=35)
    ax[i].tick_params(axis='x', labelsize=35)
    ax[i].set_title(f'{year[i]}', fontsize=50)

st.pyplot(fig)
st.write('CLUSTERING BERDASARKAN JUMLAH PELANGGAN YANG MELAKUKAN RENTAL')
st.write('PENGGUNAAN TINGGI : > 7000/hari')
st.write('PENGGUNAAN SEDANG : 3000 - 6000/hari')
st.write('PENGGUNAAN RENDAH : < 3000/hari')

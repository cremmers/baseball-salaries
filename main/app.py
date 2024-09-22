import streamlit as st
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn.objects as so
import plotly.express as px
import plotly.graph_objects as go

def salary_rank(year: str) -> pd.DataFrame:
	salaries = pd.read_csv('../static/Salaries.csv')

	salaries['yearID'] = salaries['yearID'].astype('str')
	salaries.drop('playerID', axis=1, inplace=True)
	salaries = salaries.groupby(by=['yearID', 'lgID', 'teamID'], as_index=False).sum()
	salaries = salaries.loc[salaries['yearID'] == year]
        
	salaries['rank'] = salaries['salary'].rank(ascending=False)
	salaries.sort_values(by=['rank'], inplace=True)

	return salaries

def champ_rank(year: str) -> pd.DataFrame:
	champs = pd.read_csv('../static/SeriesPost.csv')

	champs.drop(['wins', 'losses', 'ties'], axis=1, inplace=True)
	champs = champs.loc[champs['yearID'] >= 1985]
	champs = champs.astype('str')
	champs = champs.loc[champs['yearID'] == year]

	nlwc_df = champs.loc[champs['round'] == 'NLWC']
	alcs_df = champs.loc[champs['round'] == 'ALCS']
	nlcs_df = champs.loc[champs['round'] == 'NLCS']
	ws_df = champs.loc[champs['round'] == 'WS']

	champs.drop(champs.loc[champs['round'] == 'NLWC'].index, axis=0, inplace=True)
	champs = pd.concat([nlwc_df, champs])

	champs.drop(champs.loc[champs['round'] == 'ALCS'].index, axis=0, inplace=True)
	champs = pd.concat([champs, alcs_df])

	champs.drop(champs.loc[champs['round'] == 'NLCS'].index, axis=0, inplace=True)
	champs = pd.concat([champs, nlcs_df])

	champs.drop(champs.loc[champs['round'] == 'WS'].index, axis=0, inplace=True)
	champs = pd.concat([champs, ws_df])
	
	return champs

def get_years() -> list:
	salaries = pd.read_csv('../static/Salaries.csv')
	salaries['yearID'] = salaries['yearID'].astype('str')
	years = salaries.groupby(by='yearID', as_index=False).sum()
	year_list = years['yearID']
	return year_list


def get_teams() -> list:
	salaries = pd.read_csv('../static/Salaries.csv')
	teams = salaries.groupby(by='teamID', as_index=False).sum()
	team_list = teams['teamID']
	return team_list


def team_salary(teams: list) -> pd.DataFrame:
	salaries = pd.read_csv('../static/Salaries.csv')

	salaries['yearID'] = salaries['yearID'].astype('str')
	salaries.drop(['playerID', 'lgID'], axis=1, inplace=True)
	salaries = salaries.groupby(by=['teamID', 'yearID'], as_index=False).sum()
	# for team in teams:
	salaries = salaries[salaries['teamID'].isin(teams)]
	return salaries


def create_plot(salaries, champs) -> None:
	team_list = []
	for team in champs['teamIDloser']:
		team_list.append(team)
	team_list.append(champs['teamIDwinner'].iloc[-1])
	# st.write(team_list)

	round_list = []
	for rd in champs['round']:
		round_list.append(rd)
	round_list.append('CHAMP')
	team_dict = dict(zip(team_list, round_list))
	# st.write(team_dict)

	for key, value in team_dict.items():
		team_dict[key] = [value]
		team_dict[key].append(salaries.loc[salaries['teamID'] == key, 'salary'].iloc[0])
	
	x_list = []
	y_list = []
	
	for key, value in team_dict.items():
		x_list.append(value[0])
		y_list.append(value[1])
	x = x_list
	y = y_list

	# plt.figure(figsize=(4,4))
	# fig, ax = plt.subplots()
	# ax.set_xlabel('Playoff Round')
	# ax.set_ylabel('Team Salary')
	# plt.scatter(x_list, y_list)
	# for i, txt in enumerate(team_list):
	# 	ax.annotate(txt, (x[i], y[i]))

	# fig = px.scatter(x=x_list, y=y_list, text=team_list, textposition='top center')

	fig = go.Figure()

	# Add the scatter trace
	fig.add_trace(go.Scatter(
	    x=x_list, 
	    y=y_list,
	    mode='markers+text',  # Use markers and text
	    text=team_list,  # Set the text for each point
	    textposition='top center'  # Position the text above the markers
	))

	fig.update_layout(
		xaxis_title="Playoff Round",
		yaxis_title="Team Salary"
	)

	data_shaded_regions = [round_list]
	df_shaded_regions = pd.DataFrame(data=data_shaded_regions, columns=round_list)

	for index, row in df_shaded_regions.iterrows():
		if 'NLWC' in df_shaded_regions.columns:
			# retrieve the columns
		    start = row['NLWC']
		    end = row['ALWC']

		    # add shaded region
		    fig.add_vrect(
		            x0=start,
		            x1=end,
		            fillcolor="grey",
		            opacity=0.1,
		            line_width=1,
		        )

		if 'ALDS1' in df_shaded_regions.columns:
		    start = row['ALDS1']
		    end = row['NLDS2']

		    fig.add_vrect(
		            x0=start,
		            x1=end,
		            fillcolor="grey",
		            opacity=0.1,
		            line_width=1,
		        )
		if 'ALCS' in df_shaded_regions.columns:
		    start = row['ALCS']
		    end = row['NLCS']

		    fig.add_vrect(
		            x0=start,
		            x1=end,
		            fillcolor="grey",
		            opacity=0.1,
		            line_width=1,
		        )

	return fig

# def shading(champs):
# 	round_list = []
# 	for rd in champs['round']:
# 		round_list.append(rd)
# 	round_list.append('CHAMP')

# 	data_shaded_regions = [round_list]
# 	df_shaded_regions = pd.DataFrame(data=data_shaded_regions, columns=round_list)

# 	return df_shaded_regions


def create_team_plot(team) -> None:
	year_list = []
	for year in team['yearID']:
		year_list.append(year)

	salary_list = []
	for salary in team['salary']:
		salary_list.append(salary)

	team_list = []
	for team in team['teamID']:
		team_list.append(team)

	fig = px.line(x=year_list, 
	    		  y=salary_list,
	    		  color=team_list,
	    		  markers=True)

	fig.update_layout(
		xaxis_title="Year",
		yaxis_title="Team Salary"
	)

	return fig


def app(name: str) -> None:

	col1, col2 = st.columns(2)
	with col1:
		year_list = get_years()
		# year = st.text_input('Enter a year (1985-2015)', value='2015')
		year = st.selectbox('Select a year (1985-2015)', year_list)
		# st.write(type(year))
	with col2:
		team_list = get_teams()
		# st.write(team_list)
		teams = st.multiselect('Or, select teams', team_list)

	if year and not teams:
		salaries = salary_rank(year)
		champs = champ_rank(year)

		# st.write(shading(champs))

		# st.pyplot(fig)
		fig = create_plot(salaries, champs)
		st.plotly_chart(fig)

		col1, col2 = st.columns(spec=[0.6, 0.4])
		with col1:
			st.write(f'Salary ranks from {year}')
			st.dataframe(salaries, use_container_width=True, hide_index=True)
		with col2:
			st.write(f'Playoff teams from {year}')
			st.dataframe(data=champs, use_container_width=True, hide_index=True)

	if teams:
		team_table = team_salary(teams)
		fig = create_team_plot(team_table)
		# st.write(fig)
		st.plotly_chart(fig)

		st.dataframe(team_table, use_container_width=True, hide_index=True)

		
if __name__ == '__main__':
	app_name = 'Baseball Salaries'
	st.set_page_config(
		page_title=f'{app_name}',
		layout="wide")
	app(app_name)


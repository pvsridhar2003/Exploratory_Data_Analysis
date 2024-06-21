# Required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the datasets
deliveries = pd.read_csv('.../deliveries.csv')
matches = pd.read_csv('.../matches.csv')

# Function to calculate team performance
def team_performance(df):
    team_stats = df['winner'].value_counts().reset_index()
    team_stats.columns = ['Team', 'Wins']
    team_matches = pd.concat([df['team1'], df['team2']]).value_counts().reset_index()
    team_matches.columns = ['Team', 'Matches']
    team_stats = pd.merge(team_stats, team_matches, on='Team')
    team_stats['Win_Percentage'] = (team_stats['Wins'] / team_stats['Matches']) * 100
    return team_stats.sort_values(by='Win_Percentage', ascending=False)

# Function to calculate player performance
def player_performance(df):
    player_stats = df.groupby('player_of_match').size().reset_index(name='Awards')
    return player_stats.sort_values(by='Awards', ascending=False)

# Calculate team performance
team_stats = team_performance(matches)

# Calculate player performance
player_stats = player_performance(matches)

# Factors contributing to wins
def factors_contributing_wins(df):
    factors = df[['toss_winner', 'toss_decision', 'winner', 'win_by_runs', 'win_by_wickets']].copy()
    factors['toss_win_match_win'] = factors.apply(lambda x: 1 if x['toss_winner'] == x['winner'] else 0, axis=1)
    toss_decision_stats = factors.groupby('toss_decision')['toss_win_match_win'].mean().reset_index()
    win_margin_stats = factors[['win_by_runs', 'win_by_wickets']].describe().T
    return toss_decision_stats, win_margin_stats

toss_decision_stats, win_margin_stats = factors_contributing_wins(matches)

# Visualization
# Win percentage plot
plt.figure(figsize=(12, 6))
sns.barplot(x='Team', y='Win_Percentage', data=team_stats)
plt.xticks(rotation=90)
plt.title('Team Win Percentage')
plt.show()

# Plot of top 10 players
plt.figure(figsize=(12, 6))
sns.barplot(x='player_of_match', y='Awards', data=player_stats.head(10))
plt.xticks(rotation=90)
plt.title('Top 10 Players with Most Player of the Match Awards')
plt.show()

# Plot on the impact of toss decision
plt.figure(figsize=(6, 4))
sns.barplot(x='toss_decision', y='toss_win_match_win', data=toss_decision_stats)
plt.title('Impact of Toss Decision on Match Win')
plt.show()

# Team performance statistics
print("Team Performance:")
print(team_stats)

# Player performance statistics
print("\nPlayer Performance:")
print(player_stats.head(10))

# Toss decision impact
print("\nToss Decision Impact:")
print(toss_decision_stats)

# Win margin statistics
print("\nWin Margin Statistics:")
print(win_margin_stats)

# Recommendations for endorsement
top_teams = team_stats.head(3)
top_players = player_stats.head(5)

print("\nRecommended Teams for Endorsement:")
print(top_teams[['Team', 'Win_Percentage']])
print("\nRecommended Players for Endorsement:")
print(top_players[['player_of_match', 'Awards']])

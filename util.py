## This is my makeshift ORM that populates my player foreign keys.
## I should learn how to do this for real before this project goes too far
def populateMatch(match, db):
    match['teams'] = [populateTeam(team, db) for team in match['teams']]
    return match

def populateTeam(team, db):
    team['players'] = [db.players.find_one({"_id": player_id}) for player_id in team['players'] ]
    return team

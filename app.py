from database import connect_db, create_tables
from models import Team, Match, Group
import random

class Tournament:
    def __init__(self, groups):
        self.groups = groups

    def start(self):
        print("Tournament started!")
        # Add tournament logic here

def team_management_menu():
    while True:
        print("\nTeam Management Menu:")
        print("1. Add Team")
        print("2. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            team_name = input("Enter team name: ")
            team = Team(team_name)
            team.save()
            print(f"Team '{team_name}' added.")
        elif choice == '2':
            break
        else:
            print("Invalid choice, please try again.")

def match_management_menu():
    while True:
        print("\nMatch Management Menu:")
        print("1. Add Match")
        print("2. Update Match Score")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            team1_id = int(input("Enter Team 1 ID: "))
            team2_id = int(input("Enter Team 2 ID: "))
            match = Match(team1_id, team2_id)
            match.save()
            print(f"Match added between Team {team1_id} and Team {team2_id}.")
        elif choice == '2':
            match_id = int(input("Enter Match ID: "))
            score1 = int(input("Enter score for Team 1: "))
            score2 = int(input("Enter score for Team 2: "))
            match = Match.get_match(match_id)
            match.update_score(score1, score2)
            print(f"Score updated for match between Team {match.team1_id} and Team {match.team2_id}.")
        elif choice == '3':
            break
        else:
            print("Invalid choice, please try again.")

def group_management_menu():
    while True:
        print("\nGroup Management Menu:")
        print("1. Create Group")
        print("2. Add Team to Group")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            group_name = input("Enter group name: ")
            group = Group(group_name)
            group.save()
            print(f"Group '{group_name}' added.")
        elif choice == '2':
            group_id = int(input("Enter Group ID: "))
            team_id = int(input("Enter Team ID: "))
            Group.add_team(group_id, team_id)
            print(f"Team {team_id} added to Group {group_id}.")
        elif choice == '3':
            break
        else:
            print("Invalid choice, please try again.")

def random_group_assignment():
    num_teams = int(input("Enter the number of teams: "))
    num_groups = int(input("Enter the number of groups: "))
    
    teams = []
    for i in range(num_teams):
        team_name = input(f"Enter name for Team {i + 1}: ")
        teams.append(team_name)

    random.shuffle(teams)
    
    groups = {f'Group {i + 1}': [] for i in range(num_groups)}
    
    for i, team in enumerate(teams):
        group_number = i % num_groups
        groups[f'Group {group_number + 1}'].append(team)

    for group, team_list in groups.items():
        print(f"{group}: {', '.join(team_list)}")

    return groups

def main():
    conn = connect_db()
    create_tables(conn)
    conn.close()

    main_menu()

def main_menu():
    tournament = None  # Initialize the tournament variable

    while True:
        print("\nMain Menu:")
        print("1. Team Management")
        print("2. Match Management")
        print("3. Group Management")
        print("4. Randomly Assign Teams to Groups")
        print("5. Start Tournament")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            team_management_menu()
        elif choice == '2':
            match_management_menu()
        elif choice == '3':
            group_management_menu()
        elif choice == '4':
            groups = random_group_assignment()  # Modify this to return groups
            tournament = Tournament(groups)  # Create a new tournament instance
        elif choice == '5':
            if tournament:
                tournament.start()
            else:
                print("Please assign teams to groups before starting the tournament.")
        elif choice == '6':
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main()

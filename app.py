from database import connect_db, create_tables
from models import Team, Match, Group
import random
import tkinter as tk
from tkinter import ttk, messagebox

class TournamentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tournament Manager")
        self.root.geometry("800x600")
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Create tabs
        self.team_frame = ttk.Frame(self.notebook)
        self.match_frame = ttk.Frame(self.notebook)
        self.group_frame = ttk.Frame(self.notebook)
        self.random_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.team_frame, text='Team Management')
        self.notebook.add(self.match_frame, text='Match Management')
        self.notebook.add(self.group_frame, text='Group Management')
        self.notebook.add(self.random_frame, text='Random Assignment')
        
        self.setup_team_tab()
        self.setup_match_tab()
        self.setup_group_tab()
        self.setup_random_tab()

    def setup_team_tab(self):
        # Team Name Entry
        ttk.Label(self.team_frame, text="Team Name:").pack(pady=5)
        self.team_name_entry = ttk.Entry(self.team_frame)
        self.team_name_entry.pack(pady=5)
        
        ttk.Button(self.team_frame, text="Add Team", 
                  command=self.add_team).pack(pady=10)

    def setup_match_tab(self):
        # Match Management Controls
        ttk.Label(self.match_frame, text="Team 1 ID:").pack(pady=5)
        self.team1_id_entry = ttk.Entry(self.match_frame)
        self.team1_id_entry.pack(pady=5)
        
        ttk.Label(self.match_frame, text="Team 2 ID:").pack(pady=5)
        self.team2_id_entry = ttk.Entry(self.match_frame)
        self.team2_id_entry.pack(pady=5)
        
        ttk.Button(self.match_frame, text="Add Match", 
                  command=self.add_match).pack(pady=10)
        
        # Score Update Section
        ttk.Label(self.match_frame, text="Update Score").pack(pady=10)
        ttk.Label(self.match_frame, text="Match ID:").pack(pady=5)
        self.match_id_entry = ttk.Entry(self.match_frame)
        self.match_id_entry.pack(pady=5)
        
        ttk.Label(self.match_frame, text="Score Team 1:").pack(pady=5)
        self.score1_entry = ttk.Entry(self.match_frame)
        self.score1_entry.pack(pady=5)
        
        ttk.Label(self.match_frame, text="Score Team 2:").pack(pady=5)
        self.score2_entry = ttk.Entry(self.match_frame)
        self.score2_entry.pack(pady=5)
        
        ttk.Button(self.match_frame, text="Update Score", 
                  command=self.update_match_score).pack(pady=10)

    def setup_group_tab(self):
        # Group Management Controls
        ttk.Label(self.group_frame, text="Group Name:").pack(pady=5)
        self.group_name_entry = ttk.Entry(self.group_frame)
        self.group_name_entry.pack(pady=5)
        
        ttk.Button(self.group_frame, text="Create Group", 
                  command=self.create_group).pack(pady=10)
        
        # Add Team to Group Section
        ttk.Label(self.group_frame, text="Add Team to Group").pack(pady=10)
        ttk.Label(self.group_frame, text="Group ID:").pack(pady=5)
        self.group_id_entry = ttk.Entry(self.group_frame)
        self.group_id_entry.pack(pady=5)
        
        ttk.Label(self.group_frame, text="Team ID:").pack(pady=5)
        self.team_id_entry = ttk.Entry(self.group_frame)
        self.team_id_entry.pack(pady=5)
        
        ttk.Button(self.group_frame, text="Add Team to Group", 
                  command=self.add_team_to_group).pack(pady=10)

    def setup_random_tab(self):
        # Random Assignment Controls
        ttk.Label(self.random_frame, text="Number of Teams:").pack(pady=5)
        self.num_teams_entry = ttk.Entry(self.random_frame)
        self.num_teams_entry.pack(pady=5)
        
        ttk.Label(self.random_frame, text="Number of Groups:").pack(pady=5)
        self.num_groups_entry = ttk.Entry(self.random_frame)
        self.num_groups_entry.pack(pady=5)
        
        ttk.Button(self.random_frame, text="Start Random Assignment", 
                  command=self.start_random_assignment).pack(pady=10)
        
        self.result_text = tk.Text(self.random_frame, height=10, width=40)
        self.result_text.pack(pady=10)

    def add_team(self):
        team_name = self.team_name_entry.get()
        if team_name:
            team = Team(team_name)
            team.save()
            messagebox.showinfo("Success", f"Team '{team_name}' added successfully!")
            self.team_name_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please enter a team name!")

    def add_match(self):
        try:
            team1_id = int(self.team1_id_entry.get())
            team2_id = int(self.team2_id_entry.get())
            match = Match(team1_id, team2_id)
            match.save()
            messagebox.showinfo("Success", f"Match added between Team {team1_id} and Team {team2_id}!")
            self.team1_id_entry.delete(0, tk.END)
            self.team2_id_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid team IDs!")

    def update_match_score(self):
        try:
            match_id = int(self.match_id_entry.get())
            score1 = int(self.score1_entry.get())
            score2 = int(self.score2_entry.get())
            match = Match.get_match(match_id)
            match.update_score(score1, score2)
            messagebox.showinfo("Success", "Match score updated successfully!")
            self.match_id_entry.delete(0, tk.END)
            self.score1_entry.delete(0, tk.END)
            self.score2_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")

    def create_group(self):
        group_name = self.group_name_entry.get()
        if group_name:
            group = Group(group_name)
            group.save()
            messagebox.showinfo("Success", f"Group '{group_name}' created successfully!")
            self.group_name_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please enter a group name!")

    def add_team_to_group(self):
        try:
            group_id = int(self.group_id_entry.get())
            team_id = int(self.team_id_entry.get())
            Group.add_team(group_id, team_id)
            messagebox.showinfo("Success", f"Team {team_id} added to Group {group_id}!")
            self.group_id_entry.delete(0, tk.END)
            self.team_id_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid IDs!")

    def start_random_assignment(self):
        try:
            num_teams = int(self.num_teams_entry.get())
            num_groups = int(self.num_groups_entry.get())
            
            if num_teams < num_groups:
                messagebox.showerror("Error", "Number of teams must be greater than number of groups!")
                return
                
            self.result_text.delete(1.0, tk.END)
            teams = []
            
            def get_team_names():
                dialog = tk.Toplevel(self.root)
                dialog.title("Enter Team Names")
                entries = []
                
                for i in range(num_teams):
                    ttk.Label(dialog, text=f"Team {i + 1}:").grid(row=i, column=0, pady=2)
                    entry = ttk.Entry(dialog)
                    entry.grid(row=i, column=1, pady=2)
                    entries.append(entry)
                
                def submit():
                    for entry in entries:
                        teams.append(entry.get())
                    dialog.destroy()
                
                ttk.Button(dialog, text="Submit", command=submit).grid(row=num_teams, column=0, columnspan=2, pady=10)
                
                dialog.wait_window()
            
            get_team_names()
            
            if len(teams) == num_teams:
                random.shuffle(teams)
                groups = {f'Group {i + 1}': [] for i in range(num_groups)}
                
                for i, team in enumerate(teams):
                    group_number = i % num_groups
                    groups[f'Group {group_number + 1}'].append(team)
                
                result = ""
                for group, team_list in groups.items():
                    result += f"{group}: {', '.join(team_list)}\n"
                
                self.result_text.insert(tk.END, result)
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")

def main():
    conn = connect_db()
    create_tables(conn)
    
    root = tk.Tk()
    app = TournamentGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()

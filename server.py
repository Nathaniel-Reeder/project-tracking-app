from flask import Flask, render_template, redirect, url_for
from forms import TeamForm, ProjectForm
from model import db, User, Team, Project, connect_to_db

app = Flask(__name__)

app.secret_key = 'so so secret'

user_id = 1

@app.route('/')
def home():
    team_form = TeamForm()
    project_form = ProjectForm()
    project_form.update_teams(User.query.get(user_id).teams)
    
    return render_template('home.html', team_form = team_form, project_form = project_form)

@app.route('/add-team', methods=["POST"])
def add_team():
    team_form = TeamForm()
    
    if team_form.validate_on_submit():
        team_name = team_form.team_name.data
        new_team = Team(team_name, user_id)
        db.session.add(new_team)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route('/add-project', methods=['POST'])
def add_project():
    project_form = ProjectForm()
    project_form.update_teams(User.query.get(user_id).teams)
    
    if project_form.validate_on_submit():
        project_name = project_form.project_name.data
        project_description = project_form.description.data
        is_completed = project_form.completed.data
        team_id = project_form.team_id.data
        new_project = Project(project_name, team_id, project_description, is_completed)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route('/user-profile')
def user_profile():
    teams = User.query.get(user_id).teams
    # print(teams)
    project_list = []
    for team in teams:
        projects = Team.query.get(team.id).projects
        for project in projects:
            project_list.append(project)
    # print(project_list)
    user = User.query.get(user_id).username
    
    return render_template('profile.html', teams=teams, project_list=project_list, user=user)

@app.route('/delete-project/<project_id>')
def delete_project(project_id):
    
    if project_id:
        project_to_delete = Project.query.get(project_id)
        db.session.delete(project_to_delete)
        db.session.commit()
        return redirect(url_for('user_profile'))
    else:
        print('Problem With ID')
        return redirect(url_for('user_profile'))
    
@app.route('/update-project/<project_id>')
def update_project(project_id):
    project_to_update = Project.query.get(project_id)
    
    project_form = ProjectForm()
    project_form.update_teams(User.query.get(user_id).teams)
    
    if project_form.validate_on_submit():
        print('Valid On Submit')
        project_name = project_form.project_name.data
        project_description = project_form.description.data
        is_completed = project_form.completed.data
        team_id = project_form.team_id.data
        
        project_to_update.name = project_name
        project_to_update.description = project_description
        project_to_update.completed = is_completed
        project_to_update.team_id = team_id
        
        db.session.add(project_to_update)
        db.session.commit()
        return redirect(url_for('user_profile'))
    else:
        print('Not Valid on Submit')
    
    return render_template('update.html', project_form=project_form, project_id=project_id)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug = True)
    
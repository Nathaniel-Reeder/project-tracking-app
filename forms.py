from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length

class TeamForm(FlaskForm):
    team_name = StringField('team name', validators=[DataRequired(), Length(min=4, max=255)])
    submit = SubmitField('submit')
    
class ProjectForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired(), Length(min=4, max=255)])
    description = StringField('Description')
    completed = BooleanField('Completed', validators=[DataRequired()])
    team_id = SelectField('Team ID')
    submit = SubmitField('Submit')
    
    def update_teams(self, teams):
        self.team_id.choices = [ (team.id, team.team_name) for team in teams ]
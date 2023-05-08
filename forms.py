from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, InputRequired

class TeamForm(FlaskForm):
    team_name = StringField('Team Name', validators=[DataRequired(), Length(min=4, max=255)])
    submit = SubmitField('Submit')
    
class ProjectForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired(), Length(min=4, max=255)])
    description = StringField('Description')
    completed = BooleanField('Completed')
    team_id = SelectField('Team ID')
    submit = SubmitField('Submit')
    
    def update_teams(self, teams):
        self.team_id.choices = [ (team.id, team.team_name) for team in teams ]


        
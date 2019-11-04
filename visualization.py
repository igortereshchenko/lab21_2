from models import db, Users, Skills
import plotly
import plotly.graph_objs as go
import json


def visualization_data():
    data = db.session.query(Users.Username,
                            db.func.count(Skills.Id).label("SkillsQuantity")
                            ).join(Skills, Users.Username == Skills.UsernameFk).group_by(Users.Username).all()

    bar = [
        go.Bar(
            x=[value[0] for value in data],
            y=[value[1] for value in data]
        )
    ]

    return json.dumps(bar, cls=plotly.utils.PlotlyJSONEncoder)

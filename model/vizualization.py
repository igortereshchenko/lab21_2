from model.model import db, StudentTable, CarsTable
import plotly
import plotly.graph_objs as go
import json


def visualization_data():
    data = db.session.query(CarsTable.Model,
                            db.func.count(StudentTable.Student_card).label("StudentsQuantity")
                            ).join(StudentTable, CarsTable.StudentCardFk == StudentTable.Student_card).group_by(
        CarsTable.Model).all()

    bar = [
        go.Bar(
            x=[value[0] for value in data],
            y=[value[1] for value in data]
        )
    ]

    return json.dumps(bar, cls=plotly.utils.PlotlyJSONEncoder)

from flask import render_template
from flask.views import MethodView
import gbmodel

class Index(MethodView):
    def get(self):
        model = gbmodel.get_model()
        entries = [dict(title=row[0], author=row[1], ingredients=row[2], instructions=row[3]) for row in model.select()]
        return render_template('/index.html', entries=entries)
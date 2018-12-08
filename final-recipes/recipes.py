from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel

class Recipes(MethodView):
    def get(self):
        model = gbmodel.get_model()
        entries = [dict(title=row[0],
                        author=row[1],
                        ingredients=row[2],
                        instructions=row[3])
                   for row in model.select()]
        return render_template('../final_recipes/templates/recipes.html', entries=entries)
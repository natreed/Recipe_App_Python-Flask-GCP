from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel

class Recipes(MethodView):
    def get(self):
        return render_template('../final_recipes/templates/recipes.html')

    def post(self):
        """
        Accepts POST requests, and processes the form;
        Redirect to index when completed.
        """
        model = gbmodel.get_model()
        model.insert(request.form['title'],
                     request.form['author'],
                     request.form['ingredients'],
                     request.form['instructions'])
        return redirect(url_for('index'))

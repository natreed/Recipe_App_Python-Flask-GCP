from gbmodel.Model import Model



class model(Model):
    def __init__(self):
        """initialize recipes as a list of dictionary entries"""
        self.recipes = [{'title': 'bread',
                         'author': 'nate',
                         'ingredients': '1c flour, 1c water',
                         'instructions': 'mix flour with water and bake at 375f for 10 min.'},
                        {'title': 'chocolate chip cookies',
                         'author': 'Great Aunt Gurdy',
                         'ingredients': '2c flour, 1c milk, 3 eggs, 2 cups chocolate chips, 1/2 lb butter, 2c sugar',
                         'instructions': 'Mix ingredients with a mixer till smooth.\n Roll into 1 inch diameter balls'
                                         'and put them on a cookie sheet.\nBake at 400f for 15 minutes.'}
                        ]

    def select(self):
        """returns self.recipes"""
        return self.recipes

    def insert(self, title, author, ingredients, instructions):
        self.recipes.append({'title': title,
                                'author': author,
                                'ingredients': ingredients,
                                'instructions': instructions
                            })
        return True

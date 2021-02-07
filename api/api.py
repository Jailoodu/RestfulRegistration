from flask_restplus import Resource, Api

# Initialize an API instance
api = Api(version='1.0', title='Registration API',
          description='An API which allows interactivity with users')
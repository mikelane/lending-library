from api import create_app

"""
This is a workaround for pytest collection of flask-sqlalchemy models.
When running tests, the first thing that pytest does is to collect the
tests by importing all the test files. If a test file imports a model,
as they will surely do, then the model tries to use the api.db before
the app has been created. Doing this makes flask-sqlalchemy raise a
RuntimeError saying that there is no application found. The following
code only exists to set the app context during test import to avoid
this RuntimeError. The tests will us the app fixture which sets up the
context and so this has no effect on the tests when they are run.
"""

app = create_app()
app.app_context().push()

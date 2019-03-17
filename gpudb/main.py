from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import jinja2
import os
from design import Data
from edit import AddGraphicsData
from edit import DisplayGraphics
from editfeature import UpdateGgraphics
from edit import GraphicFeaturesQuery

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainDisplayPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        logout_string = ''
        gpu_data = None
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            logout_string = 'logout'
            gpu_data = Data.query().fetch()

        else:
            url = users.create_login_url(self.request.uri)
            logout_string = 'login'
            gpu_data = Data.query().fetch()
        template_values = {
            'url': url,
            'logout_string': logout_string,
            'user': user,
            'gpu_data': gpu_data
        }
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


class CompareGraphics(webapp2.RequestHandler):
    def post(self):


        gpus = self.request.params.getall('compare')
        gpu_names = [str(x) for x in gpus]

        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        logout_string = ''
        user = users.get_current_user()
        obj = Data.query(ndb.OR(Data.name.IN(gpu_names)))
        gpu_data = obj.fetch()
        template_values = {
            'url': url,
            'logout_string': logout_string,
            'user': user,
            'gpu_data': gpu_data
        }

        template = JINJA_ENVIRONMENT.get_template('compare.html')
        self.response.write(template.render(template_values))




class DeleteGraphics(webapp2.RequestHandler):
    def get(self, gpu_name):
        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        logout_string = ''
        gpu_data = None
        user = users.get_current_user()
        delete_row = Data.query(Data.name == gpu_name)
        for row in delete_row.fetch(limit=1):
            row.key.delete()
        gpu_data = Data.query().fetch()
        template_values = {
            'url': url,
            'logout_string': logout_string,
            'user': user,
            'gpu_data': gpu_data
        }
        self.redirect('/')



app = webapp2.WSGIApplication([

    ('/edit', AddGraphicsData),
    ('/features/([\w|\W]+)', DisplayGraphics),
    ('/editfeatures/([\w|\W]+)', UpdateGgraphics),
    ('/editfeatures', UpdateGgraphics),
    ('/select', GraphicFeaturesQuery),
    ('/compare', CompareGraphics),
    ('/delete/([\w|\W]+)', DeleteGraphics),
    ('/', MainDisplayPage),
], debug=True)

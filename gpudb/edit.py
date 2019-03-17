from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import jinja2
import os
from design import Data
import logging
from datetime import datetime


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)



class GraphicFeaturesQuery (webapp2.RequestHandler):

    def post(self, *args, **kwargs):

            if len(self.request.POST.keys()) == 0:
                self.redirect('/')

            query = dict()
            for key in self.request.POST.keys():
                query[key] = bool(self.request.POST[key])

            gpu_data = None
            gpu_details = Data.query()
            for key, value in query.items():
                gpu_data = gpu_details.filter(ndb.BooleanProperty(key) == value)
            gpu_data = gpu_data.fetch()
            user = users.get_current_user()
            if user:
                url = users.create_logout_url(self.request.uri)
                logout_string = 'logout'
                # gpu_data = Data.query(ndb.BooleanProperty(key) == value).fetch()
            else:
                url = users.create_login_url(self.request.uri)
                logout_string = 'login'

            template_values = {
                'url': url,
                'logout_string': logout_string,
                'user': user,
                'gpu_data': gpu_data,
                'filter_key' : key,
                'filter_value' : value
            }

            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.write(template.render(template_values))


class DisplayGraphics(webapp2.RequestHandler):

    def get(self, gpu_name):
        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        gpu_data = Data.query(Data.name == gpu_name).get()

        template_values = {
            'url': url,
            'gpu_data': gpu_data,
        }
        template = JINJA_ENVIRONMENT.get_template('feature.html')
        self.response.write(template.render(template_values))


class AddGraphicsData(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        template_values = {
            'myuser': user
        }
        template = JINJA_ENVIRONMENT.get_template('add.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        if self.request.get('button') == 'Add':
            name = self.request.get('device_name')
            manufacturer = self.request.get('manufacturer', name)
            dateIssue = datetime.strptime(self.request.get('dateIssue'), '%Y-%m-%d')
            geometry_shader = self.request.get('GeometryShader') == "on"
            tesselation_shader = self.request.get('TesselationShaderr') == "on"
            shader_int16 = self.request.get('ShaderInt16') == "on"
            sparse_binding = self.request.get('SparseBinding') == "on"
            texture_compressionetc2 = self.request.get('TextureCompressionETC2') == "on"
            vertex_pipeline_stores_and_atomics = self.request.get('vertexPipelineStoresAndAtomics') == "on"

            if Data.query(Data.name==name).get():
                 self.response.headers['Content-Type'] = 'text/html'
                 template_values = {
                 "error" : "The Name already exists. Please enter another device name."
                 }
                 template = JINJA_ENVIRONMENT.get_template('add.html')
                 self.response.write(template.render(template_values))
            else :
                update = Data(name=name, manufacturer=manufacturer,
                                                dateIssue=dateIssue, geometry_shader=geometry_shader,
                                                tesselation_shader=tesselation_shader, shader_int16=shader_int16,
                                                sparse_binding=sparse_binding,
                                                texture_compressionetc2=texture_compressionetc2,
                                                vertex_pipeline_stores_and_atomics=vertex_pipeline_stores_and_atomics)

                update.put()
                self.redirect('/')
        elif self.request.get('button') == 'Cancel':
            self.redirect('/')

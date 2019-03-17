from google.appengine.ext import ndb

class Data(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    manufacturer = ndb.StringProperty()
    dateIssue = ndb.DateProperty(auto_now_add=True)
    geometry_shader = ndb.BooleanProperty()
    tesselation_shader = ndb.BooleanProperty()
    shader_int16 = ndb.BooleanProperty()
    sparse_binding = ndb.BooleanProperty()
    texture_compressionetc2 = ndb.BooleanProperty()
    vertex_pipeline_stores_and_atomics = ndb.BooleanProperty()

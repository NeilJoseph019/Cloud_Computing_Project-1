from google.appengine.ext import ndb


class GPUModel(ndb.Model):
        GPU_name = ndb.StringProperty()
        manufacturer_name = ndb.StringProperty()
        date = ndb.DateProperty()
        geometry_Shader = ndb.BooleanProperty()
        tesselation_Shader = ndb.BooleanProperty()
        shader_Int = ndb.BooleanProperty()
        sparse_Binding = ndb.BooleanProperty()
        texture_Compression = ndb.BooleanProperty()
        vertex_Pipeline = ndb.BooleanProperty()
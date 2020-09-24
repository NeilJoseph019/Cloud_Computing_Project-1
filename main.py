#NeilJoseph 2992108

import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from datetime import datetime
from myuser import MyUser
from gpu import GPUModel


JINJA_ENVIRONMENT= jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainPage(webapp2.RequestHandler):
    def get(self):
        title = "GPUinfo - Home Page"
        self.response.headers['Content-Type'] = 'text/html'

        geometry_Shader = False
        tesselation_Shader = False
        shader_Int = False
        sparse_Binding = False
        texture_Compression = False
        vertex_Pipeline = False

        user = users.get_current_user()

        d_name=self.request.get("gpuname")
        selected_device_name = bool(self.request.get("gpuName"))

        if self.request.GET.get("search_device") == "Search":

            geometry_Shader = bool(self.request.GET.get("checkbox_geometry_shader"))
            tesselation_Shader = bool(self.request.GET.get("checkbox_tesselation_shader"))
            shader_Int = bool(self.request.GET.get("checkbox_shader_int"))
            sparse_Binding = bool(self.request.GET.get("checkbox_sparse_blinding"))
            texture_Compression = bool(self.request.GET.get("checkbox_textureC"))
            vertex_Pipeline = bool(self.request.GET.get("checkbox_vertexP"))

            list_device = GPUModel.query()

            if geometry_Shader == True:
                list_device = list_device.filter(GPUModel.geometry_Shader == True)
            if tesselation_Shader == True:
                list_device = list_device.filter(GPUModel.tesselation_Shader == True)
            if shader_Int == True:
                list_device = list_device.filter(GPUModel.shader_Int == True)
            if sparse_Binding == True:
                list_device = list_device.filter(GPUModel.sparse_Binding == True)
            if texture_Compression == True:
                list_device = list_device.filter(GPUModel.texture_Compression == True)
            if vertex_Pipeline == True:
                list_device = list_device.filter(GPUModel.vertex_Pipeline == True)

            list_device_query = list_device.fetch()

        else:
            list_device_query = GPUModel.query().fetch()

        template_values = {
            'title': title,
            "user": user,
            "list_device": list_device_query,
            "checkbox_geometry_shader": geometry_Shader,
            "checkbox_tesselation_shader": tesselation_Shader,
            "checkbox_shader_int": shader_Int,
            "checkbox_sparse_blinding": sparse_Binding,
            "checkbox_textureC": texture_Compression,
            "checkbox_vertexP": vertex_Pipeline
        }

        template = JINJA_ENVIRONMENT.get_template('Home.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers["Content-Type"] = "text/html"

class LoginPage(webapp2.RequestHandler):
        def get(self):
            title = "GPUinfo - Login Page"
            url = ''
            url_string = ''
            welcome = 'Welcome back'

            user = users.get_current_user()

            if user:
                url = users.create_logout_url(self.request.uri)
                url_string = 'logout'

                myuser_key = ndb.Key('MyUser', user.email())
                myuser = myuser_key.get()

                if myuser == None:
                    welcome = 'Welcome to the application'
                    myuser = MyUser(id=user.email(),
                                    email_address=user.email())
                    myuser.put()

            else:
                url = users.create_login_url(self.request.uri)
                url_string = 'login'

            template_values = {
                'title': title,
                'url': url,
                'url_string': url_string,
                'user': user,
                'welcome': welcome
            }
            template = JINJA_ENVIRONMENT.get_template('Login.html')
            self.response.write(template.render(template_values))

class InfoPage(webapp2.RequestHandler):
    def get(self):
        title = "GPUinfo - Information Page"
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        gpu_name = self.request.get("device_name")

        device_key = ndb.Key("GPUModel", gpu_name)
        device = device_key.get()

        listDevice_query=device.query(ndb.OR(GPUModel.GPU_name == gpu_name)).fetch()

        template_values = {
            'title': title,
            'user' : user,
            'list_drivers': listDevice_query
        }

        template = JINJA_ENVIRONMENT.get_template('Info.html')
        self.response.write(template.render(template_values))


class ComparePage(webapp2.RequestHandler):
    def get(self):

        title = "GPUinfo - Comparision Page"
        self.response.headers['Content-Type'] = 'text/html'

        selected_name = self.request.get("selected_device")
        current_name = self.request.get("current_device")

        if selected_name != None and current_name != None:
            selected_device_key = ndb.Key("GPUModel", selected_name)
            selected_device = selected_device_key.get()

            current_device_key = ndb.Key("GPUModel", current_name)
            current_device = current_device_key.get()

            list_device_query = GPUModel.query(ndb.OR(GPUModel.GPU_name == selected_name,
                                                         GPUModel.GPU_name == current_name)).fetch()

        else:
            list_device_query = GPUModel.query().fetch()

        if self.request.get("cancel"):
                self.redirect("/")

        template_values = {
            'title': title,
            "gpu": list_device_query
        }


        template = JINJA_ENVIRONMENT.get_template('Compare.html')
        self.response.write(template.render(template_values))

class AddDevicePage(webapp2.RequestHandler):

    def get(self):

        title = "GPUinfo - Add Device Page"
        self.response.headers['Content-Type'] = 'text/html'

        button_action = "Add Device"

        entered_name = self.request.GET.get('device_name')

        if entered_name == None:
            entered_name= ""
            entered_device = GPUModel(GPU_name="",
                                      manufacturer_name="",
                                      date=None,
                                      geometry_Shader=False,
                                      tesselation_Shader=False,
                                      shader_Int=False,
                                      sparse_Binding=False,
                                      texture_Compression=False,
                                      vertex_Pipeline=False)

        else:
            button_action = "Update Device"
            entered_device_key = ndb.Key("GPUModel", entered_name)
            entered_device = entered_device_key.get()

        template_values = {
             'title': title,
             'button_action' : button_action,
             'device_name': entered_name,
             'entered_device': entered_device
        }

        template = JINJA_ENVIRONMENT.get_template('AddDevice.html')
        self.response.write(template.render(template_values))

    def post(self):

        self.response.headers["Content-Type"] = "text/html"

        if self.request.get("add_Device") == "Add Device":

            # entered_name = self.request.GET.get('device_name')
            name=self.request.get("GPU_name")


            if self.request.get("date") == "" or name == "" :
                self.redirect('/AddDevice.html')
                return

            device_query = GPUModel.query(GPUModel.GPU_name == name).fetch()

            if len(device_query) > 0:
                self.redirect('/AddDevice.html')
                return
            else:

                entered_device = GPUModel(id=self.request.get("GPU_name"),
                                          GPU_name=self.request.get("GPU_name"),
                                          manufacturer_name=self.request.get("manufacturer_name"),
                                          date=datetime.strptime(self.request.get("date"), '%Y-%m-%d'),
                                          geometry_Shader=bool(self.request.get("checkbox_geometry_shader")),
                                          tesselation_Shader=bool(self.request.get("checkbox_tesselation_shader")),
                                          shader_Int=bool(self.request.get("checkbox_shader_int")),
                                          sparse_Binding=bool(self.request.get("checkbox_sparse_blinding")),
                                          texture_Compression = bool(self.request.get("checkbox_textureC")),
                                          vertex_Pipeline=bool(self.request.get("checkbox_vertexP"))
                                          )

                entered_device.put()
                self.redirect('/')

        if self.request.get("add_Device") == "Update Device":

                entered_name = self.request.get('device_name')
                entered_device_key = ndb.Key("GPUModel", entered_name)
                entered_device = entered_device_key.get()

                GPU_name = self.request.get("GPU_name")
                manufacturer_name = self.request.get("manufacturer_name")
                date = datetime.strptime(self.request.get("date"), '%Y-%m-%d')
                geometry_Shader = bool(self.request.get("checkbox_geometry_shader"))
                tesselation_Shader = bool(self.request.get("checkbox_tesselation_shader"))
                shader_Int = bool(self.request.get("checkbox_shader_int"))
                sparse_Binding = bool(self.request.get("checkbox_sparse_blinding"))
                texture_Compression = bool(self.request.get("checkbox_textureC"))
                vertex_Pipeline = bool(self.request.get("checkbox_vertexP"))

                entered_device.entered_name = GPU_name
                entered_device.GPU_name = GPU_name
                entered_device.manufacturer_name = manufacturer_name
                entered_device.date = date
                entered_device.geometry_Shader = geometry_Shader
                entered_device.tesselation_Shader = tesselation_Shader
                entered_device.shader_Int = shader_Int
                entered_device.sparse_Binding = sparse_Binding
                entered_device.texture_Compression = texture_Compression
                entered_device.vertex_Pipeline = vertex_Pipeline


                entered_device.put()
                self.redirect('/')

        if self.request.get("cancel"):
                self.redirect('/')

app = webapp2.WSGIApplication([('/',MainPage), ('/Info.html', InfoPage),('/Compare', ComparePage), ('/Login.html', LoginPage), ('/AddDevice.html', AddDevicePage)], debug=True)

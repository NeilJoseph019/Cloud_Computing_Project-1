# Cloud_Computing_Project-1
This application allows users to access information about the GPU’s used in the market for studying or research or purchasing purposes.
It portraits the following mechanisms:

1. Login and Logout mechanism.
2. Adding a new GPU in the system.
3. Editing and Updating the existing GPU information.
4. List view of the GPUs in the system.
5. Viewing all the Details of a GPU.
6. Comparison between selected GPU’s. 
---
* ## Application Overview
For this project the following directories were created:
* app.yaml
* myuser.py
* gpu.py
* Home.html
* Login.html
* AddDevice.html
* Info.html
* Compare.html
* main.py 
---
A. In app.yaml :

The yaml file is first created as its main responsibility is to keep the Google App Engine
informed about the various libraries, handlers and runtime required to run the application. It helps to define where the requests are to be routed amongst the available applications.

Runtime lets the Google App Engine know that we would be using python version 2.7 as few of the components of the latest python version 3 are not compatible with the version 1 of Google App Engine that is use for the application. Threadsafe states that the application is safe to use or launch multiple instances on the same server using threads in order to synchronize correctly and avoid loss of any data or race condition.

The Jinja2 library is being specified that is being used to generate html templates that can render dynamic content for the user. We use the latest version of library to avoid as many security vulnerabilities as possible.

Various handles are also specified that informs the Google App Engine which python modules and objects are responsible for handling the requests sent to a certain url’s defined in the main.py file. Handlers can also control access of url’s by the user, such as
should the user not be logged in and much more. 

B. In myuser.py :

The ndb (that is NoSql Database) client library is being imported from google.appengine.ext package. ndb is a client library for use with Google Cloud Datastore. It was designed specifically to be used from within the Google App Engine Python runtime. ndb is included in the Python runtime.

The class MyUser takes in the argument ndb.Model, this will enable all of the datastore operations to understand how to store and retrieve our class. It will handles the necessary conversions between python and their representation in the Google Cloud
Datastore. The email_address variable is created and it’s a StringProperty() as it will take in string values while its stored in the datastore.

C. In gpu.py :

This is a class named GPUModel that stores the various information related to the GPU device such as GPU name, manufacturer, date or issue and also various features of the GPU (geometry shader, tessellation shader, shaderInt16, sparse binding, texture
compression and vertex pipeline stores and atomics).

Since the GPU name and manufacturer name is a string, StringProperty is used for it and for date DateProperty is used. For the GPU features, BooleanProperty is used as in the main program checkboxes are used which returns a boolean that is either a true or false.

D. In Home.html :

This html page contains the outline format and connects various other html pages with each other. Since the basic features such as navigation bar,background and footer is common for all the pages, the part which changes in all the pages is kept within the block “{% block content %}” and “{% endblock %}”.The title is different for all the pages hence it’s kept as a variable. The style tags contain the various designs used in the page such as background colour, title, headings, etc.

In order to enable the feature selection, checkboxes are made for the selection and button is used to enable the search feature which will then display the list of GPU’s that contains the selected features.

Table tags are used in order to display the GPU name, manufacturer name and the date issued of the GPU. The GPU names are hyperlinks, which will display all the information including the features of the GPU. The table also contains the compare feature using checkbox which will allow the user to select the GPU’s that the user wishes to compare.

E. In Login.html :

This html file allows the user to login and logout, as only the user who is logged-in can make changes to the data.

The code is written within the block “{% block content %}” and “{% endblock %}”. 

F. AddDevice.html :

This page allows the logged-in user to add a device to the already existing list or edit and update the device information.

The input text type is put for entering the details and the checkboxes are for the features as it’s easier to select a single or multiple among the various mentioned.

There is a back button that takes the user back to the login/logout page. And also there is a add device which will add the entered data to the database.

G. Info.html :

This page will help the user to view all the information about the device.

There is also an edit button that redirects to the edit page that allows the logged-in user only to edit the info and update the data.

H. Compare.html :

This page will allow the user to select a device in the dropdown option list and click on the compare button to compare various selected devices with the full information about the device.

I. main.py :

At first the Jinja variable “JINJA_ENVIRONMENT” is defined as it’s considered to be unchanging. Jinja2 uses a central object called the template Environment. Instances of this class are used to store the configuration and global objects, and are used to load templates from the file system or other locations.
This python code contains totally 5 classes for various functionalities.

The classes are :
a. MainPage
b. LoginPage
c. InfoPage
d. AddDevicePage
e. ComparePage


========
Services
========

A service is a Python class that performs an action. You can define all the parameters you need as SQL Alchemy columns: portl will inspect the class parameters to automatically generate a service creation form in the web UI.

In ``portl/portl/automation/services/examples``, you will find the file ``example_service.py`` with a service template that you can use as starting point to create your own services.
This file contains the following code :

::

  # This class serves as a template example for the user to understand
  # how to implement their own custom services to portl.
  # It can be removed if you are deploying portl in production.

  # Each new service must inherit from the "Service" class.
  # portl will automatically generate a form in the web GUI by looking at the
  # SQL parameters of the class.
  # By default, a property (String, Float, Integer) will be displayed in the GUI
  # with a text area for the input.
  # If the property in a Boolean, it will be displayed as a tick box instead.
  # If the class contains a "property_name_values" property with a list of
  # values, it will be displayed:
  # - as a multiple selection list if the property is an SQL "MutableList".
  # - as a single selection drop-down list in all other cases.
  # If you want to see a few examples of services, you can have a look at the
  # /netmiko, /napalm and /miscellaneous subfolders in /portl/portl/services.

  # Importing SQL Alchemy column types to handle all of the types of
  # form additions that the user could have.
  from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, PickleType, String
  from sqlalchemy.ext.mutable import MutableDict, MutableList

  from portl.automation.models import Service
  from portl.base.classes import service_classes


  class ExampleService(Service):

      __tablename__ = "ExampleService"

      id = Column(Integer, ForeignKey("Service.id"), primary_key=True)
      # the "string1" property will be displayed as a drop-down list, because
      # there is an associated "string1_values" property in the class.
      string1 = Column(String)
      # the "string2" property will be displayed as a text area.
      string2 = Column(String)
      string2_name = "String 2 !"
      string2_length = 5
      # Text area
      an_integer = Column(Integer)
      # Text area
      a_float = Column(Float)
      # the "a_list" property will be displayed as a multiple selection list
      # list, with the values contained in "a_list_values".
      a_list = Column(MutableList.as_mutable(PickleType))
      # Text area where a python dictionary is expected
      a_dict = Column(MutableDict.as_mutable(PickleType))
      # "boolean1" and "boolean2" will be displayed as tick boxes in the GUI.
      boolean1 = Column(Boolean)
      boolean1_name = "Boolean N°1"
      boolean2 = Column(Boolean)

      # these values will be displayed in a single selection drop-down list,
      # for the property "a_list".
      string1_values = [("cisco", "Cisco"), ("juniper", "Juniper"), ("arista", "Arista")]

      # these values will be displayed in a multiple selection list,
      # for the property "a_list".
      a_list_values = [
          ("value1", "Value 1"),
          ("value2", "Value 2"),
          ("value3", "Value 3"),
      ]

      __mapper_args__ = {"polymorphic_identity": "ExampleService"}

      # Some services will take action or interrogate a device. The job method
      # can also take device as a parameter for these types of services.
      # def job(self, device, payload):
      def job(self, payload: dict) -> dict:
          # The "job" function is called when the service is executed.
          # The parameters of the service can be accessed with self (self.string1,
          # self.boolean1, etc)
          # You can look at how default services (netmiko, napalm, etc.) are
          # implemented in the /services subfolders (/netmiko, /napalm, etc).
          # "results" is a dictionary that will be displayed in the logs.
          # It must contain at least a key "success" that indicates whether
          # the execution of the service was a success or a failure.
          # In a workflow, the "success" value will determine whether to move
          # forward with a "Success" edge or a "Failure" edge.
          return {"success": True, "result": "example"}


  service_classes["ExampleService"] = ExampleService

When the application starts, it loads all python files in ``portl/portl/automation/services``, and adds all models to the database.
You can create instances of that service from the web UI.

portl looks at the class parameters (SQL Alchemy columns) to auto-generate a form for the user to create new instances of that service.
Parameters with _values sets the options in selection lists. Parameters with _name set the display name, or pretty-printed name in the UI.
Parameters with _length restricts text input to a maximum length for length-sensitive APIs.

For the ``ExampleService`` class displayed above, the SQL columns are the following ones:

::

      string1 = Column(String)
      # the "string2" property will be displayed as a text area.
      string2 = Column(String)
      string2_name = "String 2 !"
      string2_length = 5
      # Text area
      an_integer = Column(Integer)
      # Text area
      a_float = Column(Float)
      # the "a_list" property will be displayed as a multiple selection list
      # list, with the values contained in "a_list_values".
      a_list = Column(MutableList.as_mutable(PickleType))
      # Text area where a python dictionary is expected
      a_dict = Column(MutableDict.as_mutable(PickleType))
      # "boolean1" and "boolean2" will be displayed as tick boxes in the GUI.
      boolean1 = Column(Boolean)
      boolean1_name = "Boolean N°1"
      boolean2 = Column(Boolean)

      # these values will be displayed in a single selection drop-down list,
      # for the property "a_list".
      string1_values = [("cisco", "Cisco"), ("juniper", "Juniper"), ("arista", "Arista")]

      # these values will be displayed in a multiple selection list,
      # for the property "a_list".
      a_list_values = [
          ("value1", "Value 1"),
          ("value2", "Value 2"),
          ("value3", "Value 3"),
      ]

Here is the associated auto-generated form:

.. image:: /_static/services/service_system/example_service.png
   :alt: Example service
   :align: center

The rules for the auto-generation of service forms are the following:
- A String, Integer or Float property is by default displayed as a text area. However, if the service class has another property whose name is ``<property_name>_values``, portl will generate a drop-down list to choose a value from instead. In the aforementioned example, ``operating_system`` is a String column that will be displayed as a text area in the web UI. On the other hand, ``vendor`` is a String column and the class has a ``vendor_values`` property that contains a list of possible values: the ``vendor`` property will be displayed as a (single-selection) drop-down list.
- A Boolean property is displayed as a checkbox.
- A MutableList property is displayed as a multi-selection list. It must have an associated "_values" property containing the list of values that can be selected.
- A MutableDict property is displayed as a text area. You can write a dictionary in that text area: it will be converted to an actual python dictionary.

Inside the ``portl/portl/automation/services`` folder, you are free to create subfolders to organize your own services any way you want: portl will automatically detect all python files. After adding a new custom service, you must reload the application before it appears in the web UI.

portl comes with a list of "default" services based on network automation frameworks such as ``netmiko``, ``napalm``, ``nornir`` and ``ansible``.

Custom Services Path
--------------------

By default, portl will scan the ``portl/portl/automation/services`` folder to instantiate all services you created in that folder.
If you want portl to scan another folder (e.g to not have custom services in portl .git directory, so that you can safely pull the latest code from Github), you can set the ``CUSTOM_SERVICES_PATH`` environment variable to the path of the folder that contains your custom services.

Service Management
------------------

Once a service has been customized with parameters, devices selected, etc, we refer to it as a Service Instance. All Service Instances are displayed in the :guilabel:`automation/service_management` page in the ``Automation`` section.

.. image:: /_static/services/service_system/service_management.png
   :alt: Service Management page
   :align: center

From the :guilabel:`automation/service_management` page, you can:

- Start a Service Instance (``Run`` button).
- View and compare the logs of the Service Instance.
- Edit the Service Instance properties.
- Delete the Service Instance.

When running a service instance, the device progress (current device/total devices selected to run) will be displayed in the table, unless Multiprocessing is selected to run the devices in parallel, in which case portl cannot keep track of how many devices are completed until the service instance finishes.

Each field in the table allows for searching that field by inclusion match. The Status field however, needs to perform an exact search, so fully input 'Running' or 'Idle' to search.

Service devices
---------------

When you create a new Service Instance, the form will also contain multiple selection fields for you to select "target devices".

.. image:: /_static/services/service_system/target_selection.png
   :alt: Target selection
   :align: center

The service will run on all selected devices in parallel (multiprocessing). If you select pools, it will run on the union of all devices in the selected pools.
Some services have no target device at all, depending on what the service does.

Variable substitution
---------------------

For some services, it is useful for a string to include variables such as a timestamp or device parameters.
For example, if you run a ReST call script on several devices to send a request at a given URL, you might want the URL to depend on the name of the device.
Any code between double curved brackets will be evaluated at runtime and replaced with the appropriate value.

For example, you can POST a request on several devices at ``/url/{{device.name}}``, and ``{{device.name}}`` will be replaced on each execution iteration by the name of each device.

Let's consider the following ReST call service:

.. image:: /_static/services/service_system/variable_substitution.png
   :alt: Variable substitution
   :align: center

When this service is executed, the following GET requests will be sent in parallel:

::

  INFO:werkzeug:127.0.0.1 - - [13/Oct/2018 14:07:49] "GET /rest/object/device/router18 HTTP/1.1" 200 -
  INFO:werkzeug:127.0.0.1 - - [13/Oct/2018 14:07:49] "GET /rest/object/device/router14 HTTP/1.1" 200 -
  INFO:werkzeug:127.0.0.1 - - [13/Oct/2018 14:07:49] "GET /rest/object/device/router8 HTTP/1.1" 200 -

Variable substitution is also valid in a configuration string (for a Netmiko or Napalm configuration) service, as well as a validation string (Netmiko validation service, Ansible playbook, etc).

Result Validation
-----------------

For some services, the success or failure of the service is decided by a "Validation" process.
The validation consists in:
- Either looking for a string in the output of the service
- Or matching the output of the service against a regular expression

In addition to text matching, for some services where output is either expected in JSON/dictionary format, or where expected XML output can be converted to dictionary format, matching against a dictionary becomes possible:
- Dictionary matching can be by inclusion:  Are my provided key:value pairs included in the output?
- Dictionary matching can be by equality: Are my provided key:value pairs exactly matching the output key:value pairs?

A few options are available to the user:
- ``Negative logic``: the result is inverted: a success becomes a failure and vice-versa. This prevents the user from using negative look-ahead regular expressions.
- ``Delete spaces before matching``: the output returned by the device will be stripped from all spaces and newlines, as those can sometimes result in false negative.


Run multiple services
---------------------

- Service instance tasks will run in parallel to other service instance tasks as long as they are standalone and do not exist within a workflow.
- Service Instance (and workflows) that exist inside of a workflow will run in sequential order as defined in the workflow builder.
- If multiple inventory devices are selected within the individual service instance definitions (but not at the workflow instance level, since that overrides any devices selected for the individual service instances), these will run in parallel.

Retry mechanism
---------------

Each service can be configured to run again in case of failures.
There are two parameters to configure:

- The number of retries (default: 0)
- The time between retries (default: 10 seconds)

.. note:: The retry will affect only the devices for which the service failed. Let's consider a service configured to run on 3 devices D1, D2, and D3 with 2 "retries". If it fails on D2 and D3 when the service runs for the first time, portl will run the service again for D2 and D3 at the first retry. If D2 succeeds and D3 fails, the second and last retry will run on D3 only.

Service logs
------------

Logs are stored for each run of the Service Instance (and for Workflows at large). In the event that no retries are configured for a service instance, the results will simply be shown in the logs in a dictionary organized by device. In the event that retries are configured, the Logs dictionary will contain an overall results section, as well as a section for each attempt, where failed and retried devices are shown in subsequent sections starting with attempt2.

You can compare two versions of the logs from the ``Logs`` window (a line-by-line diff is generated).
Here's a comparison of a ``Napalm get_facts`` service:

.. image:: /_static/services/service_system/service_compare_logs.png
   :alt: Compare logs
   :align: center

Service notification
--------------------

When a service (or a workflow) finishes, you can choose to receive a notification that contains the logs of the service (whether it was successful or not for each device, etc).

There are three types of notification:
- Mail notification: portl sends a mail to an address of your choice.
- Slack notification: portl sends a message to a channel of your choice.
- Mattermost notification: same as Slack, with Mattermost.

To set up the mail system, you must export the following environment variables before starting portl:

::

  MAIL_SERVER = environ.get('MAIL_SERVER', 'smtp.googlemail.com')
  MAIL_PORT = int(environ.get('MAIL_PORT', '587'))
  MAIL_USE_TLS = int(environ.get('MAIL_USE_TLS', True))
  MAIL_USERNAME = environ.get('MAIL_USERNAME')
  MAIL_PASSWORD = environ.get('MAIL_PASSWORD')

From the :guilabel:`admin/administration` panel, you must configure the sender and recipient addresses of the mail (Mail notification), as well as an Incoming webhook URL and channel for the Mattermost/Slack notifications.

.. image:: /_static/services/service_system/notifications.png
   :alt: Notification
   :align: center

The ``Mail Recipients`` parameter must be set for the mail system to work; the `Admin/Administration` panel parameter can
also be overriden from Step2 of the Service Instance and Workflow configuration panels. For Mail notification, there is
also an option in the Service Instance configuration to display only failed objects in the email summary versus seeing a
list of all passed and failed objects.

In Mattermost, if the ``Mattermost Channel`` is not set, the default ``Town Square`` will be used.

Gitlab Export
-------------

In the :guilabel:`admin/administration` page, you can configure a remote Git repository with the property ``Git Repository Automation``. Each service has a ``Push to Git`` option to push the results of the service to this remote repository.
This allows comparing the results of a service between any two runs.

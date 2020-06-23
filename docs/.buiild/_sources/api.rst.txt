.. _api:

API
===

.. currentmodule:: api

.. autofunction:: api


Error Handler
-------------

.. currentmodule:: api.error_handler

.. autoclass:: Base_Handler
    :members:
    :inherited-members:

.. aucoclass:: Bad_Request_Handler
    :members:
    :inherited-members:

.. autoclass:: Internal_Server_Error_Handler
    :members:
    :inherited-members:

.. autoclass:: Unsupported_Media_Type_Handler
    :members:
    :inherited-members:


Media Handler
-------------

.. currentmodulee:: api.media_handler

.. autoclass:: XML_Handler
    :members:
    :inherited-members:

.. autoclass:: YAML_Handler
    :members:
    :inherited-members:


Middleware
----------

.. currentmodule:: api.Middleware

.. autoclass:: Basic_Auth_Backend_Middleware
    :members:
    :inherited-members:

.. autoclass:: Negotiation_Middleware
    :members:
    :inherited-members:


Spec
----

.. currentmodule:: api.spec

.. autoclass:: Spec
    :members:
    :inherited-members:


Docstring
---------

.. currentmodule:: docstring

.. autodecorator:: docstring


Document
--------

.. currentmodule:: documennt

.. autoclass:: Base_Document
    :members:
    :inherited-members:


.. autoclass:: Agent_Catalog_Document
    :members:
    :inherited-members:

.. autoclass:: Agent_Instance_Document
    :members:
    :inherited-members:

.. autoclass:: eBPF_Program_Catalog_Document
    :members:
    :inherited-members:

.. autoclass:: eBPF_Program_Instance_Document
    :members:
    :inherited-members:

.. autoclass:: Connection_Document
    :members:
    :inherited-members:

.. autoclass:: Data_Document
    :members:
    :inherited-members:

.. autoclass:: Exec_Env_Document
    :members:
    :inherited-members:

.. autoclass:: Exec_Env_Type_Document
    :members:
    :inherited-members:

.. autoclass:: Network_Link_Document
    :members:
    :inherited-members:

.. autoclass:: Network_Link_Type_Document
    :members:
    :inherited-members:

Lib
---

.. currentmodule:: lib

.. autofunction:: elasticsearch.connection

.. autofunction:: heartbeat.heartbeat

.. autofunction:: heartbeat.heartbeat

.. autoclass:: http.Status_Method
    :members:
    :inherited-members:

.. autoclass:: http.HTTP_Method
    :members:
    :inherited-members:


Response
--------

.. currentmodule:: lib.response

.. autoclass:: Base_Response
    :members:
    :inherited-members:

.. autoclass:: Bad_Request_Response
    :members:
    :inherited-members:

.. autoclass:: Conflict_Response
    :members:
    :inherited-members:

.. autoclass:: Content_Response
    :members:
    :inherited-members:

.. autoclass:: Created_Response
    :members:
    :inherited-members:

.. autoclass:: Internal_Server_Error_Response
    :members:
    :inherited-members:

.. autoclass:: No_Content_Response
    :members:
    :inherited-members:

.. autoclass:: Not_Acceptable_Response
    :members:
    :inherited-members:

.. autoclass:: Not_Found_Response
    :members:
    :inherited-members:

.. autoclass:: Not_Modified_Response
    :members:
    :inherited-members:

.. autoclass:: Ok_Response
    :members:
    :inherited-members:

.. autoclass:: Reset_Content_Response
    :members:
    :inherited-members:

.. autoclass:: Unauthorized_Response
    :members:
    :inherited-members:

.. autoclass:: Unprocessable_Entity_Response
    :members:
    :inherited-members:

.. autoclass:: Unsupported_Media_Type_Response
    :members:
    :inherited-members:


Reader
------

.. currentmodule:: reader

.. autoclass:: arg.ArgReader
    :members:
    :inherited-members:

.. autoclass:: config.configReader
    :members:
    :inherited-members:

.. autoclass:: query.QueryReader
    :members:
    :inherited-members:


Resource
--------

.. currentmodule:: resource

.. autoclass:: Agent_Catalog_Resource
    :members:
    :inherited-members:

.. autoclass:: Agent_Catalog_Selected_Resource
    :members:
    :inherited-members:


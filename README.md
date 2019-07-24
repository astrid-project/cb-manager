# Context Broker APIs

## Data Model

![Data Model](data_model.png)

Each table in the figure represents an index in the Elastic nomenclature. Considering the NoSQL nature of the Elasticsearch engine for each document of any indices it is possible to add additional properties. The schema is not static and defined at priori, but it is dynamic allowing the possibility to add custom properties for a specific document.

The Data index contains the all the data collected from the Execution Environments (ExEnvs) by means of the agent[^1]. The common attributes are:

1. id (unique identifier)[^2];
2. id of the source execution environment; and 
3. id of the agent that collect the data.

Then, the other two properties are related to the time-stamp:
1. timestamp when event is occurred; and
2. timestamp-agent when the agent collect the data.

The ExecEnv index contains the host-name of the remote host where is it allocated and the list of agent IDs that are available in that ExEnv. In addition, it contain the type field that correspond a specified type of ExEnv. The different type of execution environment are defined with the index ExecEnvType. Currently, the available types are: *i*) *Virtual Machine* and *ii*) *Container*. Obviously, it is possible to add other types depending on the specific requirements. Finally, the ExeEnvs could contain the information regarding the installed software. The field software contains the list of IDs of the sofware defined with the index Software. This part is not out of scope of the ASTRID project context and, for this reason, in Figure 4, it is this highlighted with a dashed box. The API implementation, that will be described in the next sections, does not consider the software index. Nervelessness, this example represent a typical solution for various common cases. The proposed data model allows the customization with the integration of additional entities in very simple way.
The Agent index contains specific information related to the agents, and in particular the Beats of the Elastic stack. For a detailed description of these properties see [^3].
In addition, the data model allow to see the status of the connections between the execution environments. The Connection index couples the ExEnv and network link to which it belongs. This index should contains all the information regarding the network link and the ExEnv as, for example, the IP address (version 4 and/or 6) or if the link is encrypted and how (which method, etc.).
The network links are defined with the relative index where it indicated the type. All the possible network link types are defined in the NetworkLinkType index. At the moment, the possible types are: Point to Point (Point 2 Point), Multi-point, and Slice.


[^1]: In the reference architecture the agents are Beats from Elastic Stack. Notwithstanding, the data model refers to a generic agent allowing to possibility to use different types.

[^2]: In Elasticsearch, each document is identified by a unique id. For obvious reasons, in the description of the following indices, we omit the description of all the id fields.

[^3]: “Getting started with Beats,” [Online]. Available: https://www.elastic.co/guide/en/beats/libbeat/current/getting-started.html.

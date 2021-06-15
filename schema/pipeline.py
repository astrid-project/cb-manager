from marshmallow.fields import Str

from document.agent.instance import Agent_Instance_Document
from document.algorithm.instance import Algorithm_Instance_Document
from document.pipeline import Pipeline_Document
from schema.base import Base_Schema
from schema.validate import In
from utils.schema import List_or_One


class Pipeline_Schema(Base_Schema):
    """Represents the stored pipelines."""

    doc = Pipeline_Document
    id = Str(required=True, example='BXrHRn5RPU55Qh9JwMZn', description='Id of the pipeline.')
    name = Str(description='Used by the UI to create a new pipeline.', example='test-pipeline')
    agent_instance_ids = List_or_One(Str(validate=In.apply(Agent_Instance_Document.get_ids),
                                         error_messages=In.error_messages),
                                     description='Ids of the agent instances included in this pipeline.')
    algorithm_instance_ids = List_or_One(Str(validate=In.apply(Algorithm_Instance_Document.get_ids),
                                             error_messages=In.error_messages),
                                         description='Ids of the algorithm instances included in this pipeline.')

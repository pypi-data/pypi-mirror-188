from .graph.graph_endpoints import GraphEndpoints
from .model.model_endpoints import ModelEndpoints
from .pipeline.pipeline_endpoints import PipelineEndpoints
from .query_runner.query_runner import QueryRunner
from .server_version.server_version import ServerVersion
from .system.system_endpoints import DirectSystemEndpoints
from .utils.util_endpoints import DirectUtilEndpoints

"""
This class should inherit endpoint classes that only contain endpoints that can be called directly from
the `gds` namespace. Example of such endpoints are: "graph" and "list".
"""


class DirectEndpoints(DirectSystemEndpoints, DirectUtilEndpoints, GraphEndpoints, PipelineEndpoints, ModelEndpoints):
    def __init__(self, query_runner: QueryRunner, namespace: str, server_version: ServerVersion):
        super().__init__(query_runner, namespace, server_version)

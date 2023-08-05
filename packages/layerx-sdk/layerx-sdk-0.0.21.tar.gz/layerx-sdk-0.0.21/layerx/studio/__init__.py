
from layerx.studio.project import Project
from .studiointerface import StudioInterface
from .logger import get_debug_logger

# studio_logger = get_debug_logger('StudioClient')


class StudioClient:
    """
    Python SDK of Datalake
    """

    def __init__(self, encoded_key_secret: str, layerx_url: str) -> None:
        _studio_url = f'{layerx_url}/studio' #/sudio  :8080
        self.studio_interface = StudioInterface(encoded_key_secret, _studio_url)
    
    def create_project(self, project_name, selection_id, fps):
        print('project details: ', project_name, selection_id)
        _project = Project(client=self)
        response = _project.craete_project(project_name, selection_id, fps)
        return response
    
    """
    update the project
    """
    def update_project(self, project_id, selection_id, fps):
        print('project details: ', project_id, selection_id)
        _project = Project(client=self)
        response = _project.update_project(project_id, selection_id, fps)
        return response

    """
    delete the project
    """
    def delete_project(self, project_id):
        print('project details: ', project_id)
        _project = Project(client=self)
        response = _project.delete_project(project_id)
        return response

    """
    update the labels of project
    """
    def update_labels_to_project(self, project_id, add_list, remove_list):
        _project = Project(client=self)
        response = _project.update_labels_to_project(project_id, add_list, remove_list)
        return response

    """
    Get list of studio project
    """
    def studio_project_list(self):
        _project = Project(client=self)
        response = _project.get_project_list()
        return response




import requests
from pydantic import BaseModel

class Experiment(BaseModel):
    graph: dict
    task_type: str
    target_column: str
    experiment_id:str

    def __init__(self, experiment_id: str) -> None:
        self.experiment_id = experiment_id
        self.graph, self.task_type, self.target_column = self.__get_experiment_details(experiment_id=experiment_id)

    def __get_experiment_details(self, experiment_id: str):
        try:
            response = requests.get(
                f"http://localhost:8000/experiments/{experiment_id}",
            )
            response = response.json()
        except:
            raise Exception("Unable to connect to the server")
        try:
            graph = response["pipelineJSON"]
            project = response["project"]
            target_column = project["targetColumn"]
            task_type = project["taskType"]
        except:
            raise Exception("Invalid Experiment ID")
        return graph, task_type, target_column

    def upload_metrics(self, metrics):
        requests.put(f"http://localhost:8000/experiments/results/{self.experiment_id}", data=metrics)

from .sklearn import generate_file
from .connector import Experiment


def run_experiment(experiment_id : str, auth_key=""):
    # TODO: Implement auth keys
    experiment = Experiment(experiment_id=experiment_id)
    generate_file(graph=experiment.graph, task_type=experiment.task_type, target_column=experiment.target_column)

try:
  run_experiment("b9c36c0e-5a1c-4ce2-86cd-f146dd2a5e58")
except:
  print("erroo")
import shutil
import subprocess
from jinja2 import Template
from create_new_orchestrator import create_new_orchestration_function
from update_repository import push

orchestratorName = "PruebaDemoWirdFinal2"
activityName = "ActividadDePrueba"
templateSources = 'templates/DurableOrchestratorTemplate.txt'
destination = f'outputs/{orchestratorName}Function.ts'
repoDestination = f'src/functions/{orchestratorName}Function.ts'

if __name__ == "__main__":
    # This block of code will be executed when the script is run
    result = create_new_orchestration_function(templateSources, orchestratorName, activityName, destination)
    if(result):
        push(destination, repoDestination)

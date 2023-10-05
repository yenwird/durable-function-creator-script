import shutil
import subprocess
from jinja2 import Template

def copyTemplate (source, destination, value1, value2, value3):
    try:
        # Copy file
        shutil.copy(source, destination)  # Uncomment this line to copy the source file to the destination
        # Read and modify file content
        with open(destination, 'a') as file:
            code_template = Template(file.read())
            rendered_code = code_template.render(value1=value1, value2=value2, value3=value3)
            file.write(rendered_code)
        return 'Success'
    except:
        return 'Error'


def createAzureFuncProject (projectName): 
    try:
        # Run the Azure Functions CLI command and capture the output
        command = f'func init {projectName} --worker-runtime javascript --model V4'
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return output
    except subprocess.CalledProcessError as e:
        # Handle any errors that occurred during the command execution
        return f"Error occurred: {e.output}"
    

def navigateToProjectFolder (path):
    try:
        # Run the Azure Functions CLI command and capture the output
        command = 'cd {path}'
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return output
    except subprocess.CalledProcessError as e:
        # Handle any errors that occurred during the command execution
        return f"Error occurred: {e.output}"
    
def getFunctionCode (source, orchestratorName, activityName):
    with open(source, 'r') as file:
        code_template = Template(file.read())
        rendered_code = code_template.render(orchestratorName=orchestratorName, activityName=activityName)
        return rendered_code
    
def writeDestination(destination, text):
    with open(destination, 'a') as file:
        file.write(text)
    

def main():
    # Your main code logic goes here
    projectName = "PruebaFinal"
    orchestratorName = "OrquestadorDePrueba"
    activityName = "ActividadDePrueba"
    templateSources = 'templates/DurableOrchestratorTemplate.txt'
    destination = f'/Pruebas/src/functions/{orchestratorName}Function.ts'
    azure_function_code = getFunctionCode(templateSources, orchestratorName, activityName)
    writeDestination(destination, azure_function_code)

if __name__ == "__main__":
    # This block of code will be executed when the script is run
    main()

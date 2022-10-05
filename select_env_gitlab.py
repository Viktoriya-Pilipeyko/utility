import requests
import jmespath
import os
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

disable_warnings(InsecureRequestWarning)
# variables
CI_JOB_TOKEN = os.environ['CI_JOB_TOKEN']
# headers for requests
headers = {'PRIVATE-TOKEN': CI_JOB_TOKEN}

# this function selects the environment - with or without approvals
def select_env():
    GITLAB_USER_ID = os.environ['GITLAB_USER_ID']
    ENV = "<environment name with approvals rule>"
    url = "https://gitlab.example.ru/api/v4/projects/<project id>/protected_environments/"+ENV

    response = requests.get(url, headers=headers, verify=False)
    res = jmespath.search("approval_rules[*].user_id", response.json())

    if response.status_code == 200:
        if int(GITLAB_USER_ID) in res:
            ENV = "<environment name without approvals rule>"
            print("user is approver, so selected environment WITHOUT approval - "+ENV)
        else :
            print("user isn't approver, so selected environment WITH approval - "+ENV)
    else:
        print("couldn't choose an environment")
    return ENV

# update environment variable
def update_env(env):
    body = {'value': env}
    url = "https://gitlab.example.ru/api/v4/projects/<project id>/variables/ENV"
    response = requests.put(url, headers=headers, data=body, verify=False)

    if response.status_code == 200:
        print("environment has been updated")
    else:
        print("environment hasn't been updated")

update_env(select_env())

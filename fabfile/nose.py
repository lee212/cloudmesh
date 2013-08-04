from fabric.api import task, local
import shutil

@task
def json():
    """install nose-json"""
    print "UNINSTALL"
    r = int(local("pip freeze | fgrep nose-json | wc -l", capture=True))
    while r > 0:
        local('echo "y\n" | pip uninstall nose-json')
        r = int(local("pip freeze |fgrep cloudmesh | wc -l", capture=True))
    local("rm -rf /tmp/nose-json")
    local("cd /tmp; git clone https://github.com/dcramer/nose-json.git")
    print ("INSTALLING")
    local("cd /tmp/nose-json; python setup.py install", capture=True)
    

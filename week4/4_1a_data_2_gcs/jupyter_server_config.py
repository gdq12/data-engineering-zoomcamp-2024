import json
key_str = json.load(open('/home/ubuntu/:/home/ubuntu/.jupyter/jupyter_server_config.json'))['IdentityProvider']['hashed_password']
c.NotebookApp.certfile = u'/home/ubuntu/mycert.pem'
c.NotebookApp.keyfile = u'/home/ubuntu/mycert.pem'
c.NotebookApp.ip = '*'
c.NotebookApp.password = u'{}'.format(key_str)
c.NotebookApp.open_browser = False
c.NotebookApp.port = 8888
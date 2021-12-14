import yaml


with open('secrets.yml') as fp:
    secrets = yaml.load(fp, Loader=yaml.CLoader)
secrets['cloud_launcher_conf']

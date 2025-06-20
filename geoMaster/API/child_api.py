from geoMaster.BaseConfig.base_config import BaseConfig

# PREFIX='http://' + BaseConfig.PARENT_IP + ':' + str(BaseConfig.PARENT_PORT)

API = {
    'recv': "/parent/recvinfo",
    'frequency': "/parent/frequency",
    'drone': "/parent/drone",
    'frequency_child': "/parent/frequency/child",
}

for item in API:
    API[item] = API[item]


from start import construct_baseconfig,load_config,scan_and_register,start_front,construct_env

if __name__ == '__main__':
    load_config()
    scan_and_register()
    construct_baseconfig()
    construct_env()
    start_front()


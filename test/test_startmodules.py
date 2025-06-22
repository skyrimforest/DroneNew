
from start import construct_baseconfig,load_config,scan_and_register,start_uvicorn

if __name__ == '__main__':
    load_config()
    scan_and_register()
    construct_baseconfig()
    start_uvicorn()


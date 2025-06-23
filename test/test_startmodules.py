
from start import construct_baseconfig,load_config,scan_and_register,start_uvicorn,get_PC_info

if __name__ == '__main__':
    load_config()
    scan_and_register()
    construct_baseconfig()
    get_PC_info()
    start_uvicorn()


import pandas as pd
from datetime import datetime 
from utilities import files_system_funcs as fsf


def compose_path(*, subdirectory, category=None, name=None):
    
    path=subdirectory

    current_date=datetime.now().strftime("%Y%m%d_%H%M%S")
       
    if category:
        path=fsf.create_sub_directory(path_name=path, folder_name=category)
   
    
    if name:
        path=f"{path}/logs_{name}_{current_date}.csv"
    else:
        path=f"{path}/logs_{current_date}.csv"

    return path


def new_logs_handler(*, subdirectory, logs_keys, category=None, name=None):
   
    log_csv=compose_path(subdirectory=subdirectory, category=category, name=name)

    saved_logs_keys=logs_keys
    
    logs=[]
    
    def wrapper(fn):

        def create_logs_file():
            pd.DataFrame(logs).to_csv(log_csv, index=False)

        def insert_new_log(**kwargs):
            missing_keys={key:None for key in saved_logs_keys if key not in kwargs.keys()}
            logs.append({**missing_keys, **kwargs}) 

        def insert_new_logs(new_entries, saved_list=None):
            saved_list=new_entries.copy() if saved_list is None else saved_list

            if len(saved_list)>0:
                log_entry=saved_list.pop()
                missing_keys={key:None for key in saved_logs_keys if key not in log_entry.keys()}
                logs.append({**missing_keys, **log_entry}) 
                return insert_new_logs(new_entries, saved_list)

        def debug_logs():
            return print(f"""\033[0;31m
            {logs}
            """)

        return {
            'new_entry':insert_new_log,
            'new_entries':insert_new_logs,
            'save_logs':create_logs_file,
            'debug':debug_logs
        }.get(fn)

    return wrapper
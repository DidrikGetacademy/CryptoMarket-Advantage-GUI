import os
from datetime import datetime
def log(*args, file_name="logfile.txt", folder="logs", **kwargs):
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, file_name)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    message = " ".join(map(str, args))
    full_log = f"[{timestamp}] {message}"
    print(full_log, **kwargs)
    with open(file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(full_log + "\n")
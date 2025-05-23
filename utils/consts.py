CRAWLER_JOB_TYPE = "web_crawler"
import subprocess

def change_file_write_permissions(path: str):
    """grant write permission on files on Windows"""
    cmd = f'icacls "{path}" /grant Everyone:(W)'
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        if result.returncode == 0:
            return True
        return False
    except Exception:
        return False

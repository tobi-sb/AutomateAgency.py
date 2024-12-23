import subprocess
import time

# List of scripts to be executed sequentially
scripts = [
    '7_doawload_website.py',
    '7.3_nav-first-screen.py',
    '8_doawload_picture.py',
    '8.1_filter.py',
    '8.2_fav-icon-ban.py',
    '8.3_position_picture.py',
    '9_logo_generator.py',
    '9.1_edit_json.py',
    '9.2_update_logo.py',
    '9.9_nav-second-screen.py',
    '10_compare_image.py',
]

def run_scripts(script_list):
    for script in script_list:
        try:
            print(f"Running {script}...")
            subprocess.run(['python', script], check=True)
            print(f"Finished {script}\n")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running {script}: {e}\n")
        time.sleep(1)  # Optional delay between scripts

if __name__ == "__main__":
    run_scripts(scripts)
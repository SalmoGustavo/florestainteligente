from activitys import home

activitys_dict = {'home': home.Home()}
current = 'home'

def run_activity():
    if current in activitys_dict:
        activitys_dict[current].run()
    else:
        print(f"Error: Activity '{current}' not found.")

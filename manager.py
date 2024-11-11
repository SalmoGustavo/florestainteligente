from activitys import home

activitys_dict = {'home': home.Home()}
current = 'home'

def run_activity():
    activitys_dict[current].run()

import os
import traceback
from concurrent.futures import ThreadPoolExecutor

root_path = os.path.dirname(os.path.realpath(__file__))

profile_path = os.path.join(root_path, 'profiles')

if not os.path.isdir(profile_path):
    os.mkdir(profile_path)

existing_profiles = os.listdir(profile_path)
failed_profiles = []

executor = ThreadPoolExecutor(max_workers=5)


def get_insta_loader():
    try:
        os.system('pip3 install instaloader')
    except Exception as err:
        print('There was a problem while setting up instaloader. Is python3 added to the path? '
              'you can get more info below..')
        traceback.print_tb(err.__traceback__)


def refresh_profile(name):
    print('Updating {}'.format(name))
    try:
        os.chdir(profile_path)
        os.system('instaloader --fast-update {}'.format(profile))
        os.chdir(root_path)
    except Exception as err:
        print('Unable to run refresh on profile "{}"'.format(profile))
        traceback.print_tb(err.__traceback__)
        os.chdir(root_path)
        failed_profiles.append(profile)
    print('{} Update completed'.format(name))


def download_profile(name):
    print('Downloading {}'.format(name))
    try:
        os.chdir(profile_path)
        os.system('instaloader -profile {}'.format(profile))
        os.chdir(root_path)
    except Exception as err:
        print('Unable to run download on profile "{}"'.format(profile))
        traceback.print_tb(err.__traceback__)
        os.chdir(root_path)
        failed_profiles.append(profile)
    print('{} Download completed'.format(name))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_insta_loader()
    with open('profiles.txt', 'r') as profiles:
        for profile in profiles:
            if profile.strip() in existing_profiles:
                executor.submit(refresh_profile, profile.strip())
            else:
                executor.submit(download_profile, profile.strip())
    executor.shutdown(wait=True)

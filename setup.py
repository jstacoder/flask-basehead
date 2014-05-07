from setuptools import setup, find_packages

def get_description():
    return open('README.rst','r').read()

config = {
        'name':'flask-basehead',
        'version':'0.5.1',
        'description':'use basecamp in a flask site',
        'long_description': get_description(),
        'author': 'Kyle Roux',
        'author_email':'kyle@level2designs.com',
        'maintainer':'kyle@level2designs.com',
        'packages':find_packages(),
        # uncomment next line if packages not in top level dir
        #'package_dir':{'':'dir'}
        'include_package_data':True,
        'zip_safe':False,
        'install_requires':['Flask',],#,basehead]
}

setup(**config)


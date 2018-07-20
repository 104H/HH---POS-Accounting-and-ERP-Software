from distutils.core import setup

'''
setup(name='HH',
      version='0.0',
      packages=find_packages('sample'),
      install_requires=['pyinvoice', 'wxPython', 'pymysql'],
      package_data={'db':['data/db.txt'],},
      entry_points={
          'gui_scripts': [
              'sample = sample.__main__:main'
          ]
      },
      include_package_data=True,
      )
'''

setup(
    name='HH',
    version='0.1.1',
    author='Hunaid Hameed',
    author_email='hunaid95@outlook.com',
    packages=['hh'],
    #scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='github.com/HH95/Open-Source-Python-POS-and-Accounting-Software/',
    license='LICENSE.txt',
    description='Open Source POS, Accouting and ERP System for small to medium business needs',
    long_description=open('README.txt').read(),
    install_requires=[
        "wxPython==4.0.2a1.dev3699+c55bce4",
        "PyInvoice==0.1.0",
        "PyMySQL==0.8.0"
    ],
    package_data={'hh':['data/db.txt']}
)


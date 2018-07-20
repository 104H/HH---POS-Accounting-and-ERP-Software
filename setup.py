from distutils.core import setup
from cx_Freeze import setup, Executable
import os

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
'''
base = None
if sys.platform == "win32":
    base = "Win32GUI"
'''

build_exe_options = {"packages": ["wx",
        "pyinvoice",
        "pymysql",
        "escpos",
        "usb",
        "serial",
        "qrcode", "hh/loginScreen"], "excludes": ["tkinter"]}

#base = "Win32GUI"

execs = []

for filename in os.listdir("hh"):
    if filename.endswith(".py"):
        execs.append(Executable('hh/'+filename))


setup(
    name='HH',
    version='0.1.1',
    author='Hunaid Hameed',
    author_email='hunaid95@outlook.com',
    packages=['hh'],
    #packages=['hh', 'pyinvoice', 'wx', 'pymysql'],
    #package_dir = {'pyinvoice' : '/usr/lib/python3.6/site-packages/PyInvoice-0.1.0-py3.6.egg', 'wx' : '/usr/lib/python3.6/site-packages/wx', 'pymysql' : '/usr/lib/python3.6/site-packages/pymysql'},
    #scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='github.com/HH95/Open-Source-Python-POS-and-Accounting-Software/',
    license='LICENSE.txt',
    description='Open Source POS, Accouting and ERP System for small to medium business needs',
    long_description=open('README.txt').read(),
    package_data={'hh':['data/db.txt', 'data/recieptInfo.txt']},
    options = {"build_exe": build_exe_options},
    executables = execs,
    requires=[
        "wxPython",
        "PyInvoice",
        "PyMySQL",
        "escpos",
        "usb",
        "pyusb",
        "serial",
        "qrcode",
        "paramiko"
    ]
)


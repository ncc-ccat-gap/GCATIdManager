import setuptools

if __name__ == "__main__":
  setuptools.setup(
    name = 'gcat_id_manager',
    version = '0.0.1',
    author = 'Takayuki Kato',
    license = 'GPLv3',

    package_dir = {'': 'scripts'},
    packages = setuptools.find_packages("scripts"),
    entry_points = {
      'console_scripts': [
        'gcat_uuid = gcat_id_manager.gcat_uuid:main',
      ],
    },
    install_requires = [
      'pymysql',
    ],
  )


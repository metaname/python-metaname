from distutils.core import setup
setup(name='metaname',
      version='0.1.1',
      author='Metaname',
      author_email='support@metaname.co.nz',
      url='https://metaname.net/api/python',
      description='A python JSON-RPC client for the Metaname API',
      py_modules=['metaname'],
      requires=['requests'],
      )

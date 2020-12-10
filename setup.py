from setuptools import setup

setup(name='pptx-templater',
      version='0.0.0',
      description='When you need a template for your pptx-template',
      url='http://github.com/liamcryan/pptx-templater',
      author='Liam Cryan',
      author_email='cryan.liam@gmail.com',
      license='Apache-2.0',
      py_modules=['pptx_templater'],
      install_requires=['pptx-template==0.2.8', 'jinja2', 'click'],
      entry_points={"console_scripts": ["pptx-templater=pptx_templater:cli"]},
      )

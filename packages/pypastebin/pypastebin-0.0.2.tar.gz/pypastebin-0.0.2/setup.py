import setuptools
long_description = ""
setuptools.setup(
     name='pypastebin',
     version='0.0.2',
     scripts=[] ,
     author="sulincix",
     author_email="aa@aa.aa",
     description="python paste servivei",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://gitlab.com/sulincix/sitemaker",
     include_package_data=True,
     package_data={"pypastebin/static":["*"]},
     packages=['pypastebin', 'pypastebin/pages', 'pypastebin/static'],
 )

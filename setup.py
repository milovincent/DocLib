import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='doclib',
     version='0.1',
     scripts=['doclib'] ,
     author="Milo Szecket",
     author_email="miloszecket@gmail.com",
     description="A chatbot library for euphoria.io.",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://gitlab.com/DoctorNumberFour/DocLib",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: GNU General Public License",
         "Operating System :: OS Independent",
     ],
 )

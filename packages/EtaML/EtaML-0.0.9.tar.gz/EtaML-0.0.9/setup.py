import os
from setuptools import setup


required = [
'asttokens==2.0.5', 'atomicwrites==1.4.0', 'attrs==21.4.0', 'backcall==0.2.0', 'Brotli==1.0.9', 'category-encoders==2.4.1', 'certifi==2022.6.15', 'cffi==1.15.0', 'charset-normalizer==2.0.12', 'click==8.1.3', 'cloudpickle==2.1.0', 'colorama==0.4.4', 'colour==0.1.5', 'cycler==0.11.0', 'dash==2.4.1', 'dash-core-components==2.0.0', 'dash-cytoscape==0.3.0', 'dash-html-components==2.0.0', 'dash-table==5.0.0', 'debugpy==1.6.0', 'decorator==5.1.1', 'dill==0.3.5.1', 'dtreeviz==1.3.6', 'entrypoints==0.4', 'executing==0.8.3', 'Flask==2.1.2', 'Flask-Compress==1.12', 'fonttools==4.33.3', 'gevent==21.12.0', 'graphviz==0.20', 'greenlet==1.1.2', 'htmlmin==0.1.12', 'idna==3.3', 'ImageHash==4.2.1', 'imageio==2.19.2', 'imbalanced-learn==0.8.0', 'imblearn==0.0', 'importlib-metadata==4.11.4', 'iniconfig==1.1.1', 'install==1.3.5', 'interpret==0.2.7', 'interpret-core==0.2.7', 'ipykernel==6.13.0', 'ipython==8.3.0', 'itsdangerous==2.1.2', 'jedi==0.18.1', 'Jinja2==3.1.2', 'joblib==1.1.0', 'jupyter-client==7.3.1', 'jupyter-core==4.10.0', 'kiwisolver==1.4.2', 'lime==0.2.0.1', 'llvmlite==0.38.1', 'MarkupSafe==2.1.1', 'matplotlib==3.4.3', 'matplotlib-inline==0.1.3', 'miceforest==5.6.3', 'missingno==0.5.1', 'mrmr-selection==0.2.5', 'multimethod==1.8', 'multiprocess==0.70.13', 'nest-asyncio==1.5.5', 'networkx==2.8.2', 'numba==0.55.1', 'numpy==1.21.6', 'packaging==21.3', 'pandas==1.4.2', 'pandas-profiling==3.2.0', 'parso==0.8.3', 'pathos==0.2.9', 'patsy==0.5.2', 'pexpect==4.8.0', 'phik==0.12.2', 'pickleshare==0.7.5', 'Pillow==9.1.1', 'plotly==5.8.0', 'pluggy==1.0.0', 'pox==0.3.1', 'ppft==1.7.6.5', 'prompt-toolkit==3.0.29', 'psutil==5.9.1', 'ptyprocess==0.7.0', 'pure-eval==0.2.2', 'py==1.11.0', 'pycparser==2.21', 'pydantic==1.9.1', 'Pygments==2.12.0', 'pynndescent==0.5.7', 'pyparsing==3.0.9', 'pytest==7.1.2', 'python-dateutil==2.8.2', 'pytz==2022.1', 'PyWavelets==1.3.0', 'PyYAML==6.0', 'pyzmq==23.0.0', 'requests==2.27.1', 'SALib==1.4.5', 'scikit-image==0.19.2', 'scikit-learn==1.1.0', 'scipy==1.9.1', 'seaborn==0.11.2', 'shap==0.40.0', 'six==1.16.0', 'sklearn==0.0', 'skope-rules==1.0.1', 'slicer==0.0.7', 'stack-data==0.2.0', 'statsmodels==0.13.2', 'tangled-up-in-unicode==0.2.0', 'tenacity==8.0.1', 'threadpoolctl==3.1.0', 'tifffile==2022.5.4', 'tomli==2.0.1', 'tornado==6.1', 'tqdm==4.64.0', 'traitlets==5.2.1.post0', 'treeinterpreter==0.2.3', 'typing_extensions==4.2.0', 'umap-learn==0.5.3', 'urllib3==1.26.9', 'visions==0.7.4', 'wcwidth==0.2.5', 'Werkzeug==2.1.2', 'xgboost==1.6.1', 'zipp==3.8.0', 'zope.event==4.5.0', 'zope.interface==5.4.0']

setup(
   name='EtaML',
   version='0.0.9',
   description='Explainable Tabular AutoML',
   author='Clemens Spielvogel',
   author_email='clemens.spielvogel@gmail.com',
   package_dir={"": str("src")},
   packages=['etaml'],
   install_requires=required,
)

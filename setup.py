from setuptools import find_packages, setup

with open("requirements.txt", "r") as fh:
    install_requires = [req for req in fh.read().splitlines() if "==" in req]

setup(
    name='c4.avazu-ctr-prediction',
    version='0.1.0.dev0',
    description='Kaggle competition Click-Through Rate Prediction (Avazu).',
    author='Aymeric Flaisler',
    license='BSD-3',
    packages=find_packages(),
    install_requires=install_requires,
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov'],
    python_requires=">3.6.0, <3.9.0,",
    # package_data={"avazu-ctr-prediction": ["conf/*.*"]},
    # include_package_data=True,
    # entry_points={"console_scripts": ["avazu-ctr-prediction=avazu-ctr-prediction.__main__:cli"]}
)

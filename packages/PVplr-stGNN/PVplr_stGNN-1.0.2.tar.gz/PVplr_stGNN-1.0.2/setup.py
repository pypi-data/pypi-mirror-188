from setuptools import find_packages, setup

setup(name="PVplr_stGNN",
      version="1.0.2",
      description="PV Performance Loss Rate Estimation using Spatio-temporal Graph Neural Networks",
      author="Yangxin Fan, Xuanji Yu, Raymond Wieser, Yinghui Wu, Roger French",
      author_email="yxf451@case.edu, xxy530@case.edu, rxw497@case.edu, yxw1650@case.edu, rxf131@case.edu",
      platforms=["any"],  # or more specific, e.g. "win32", "cygwin", "osx"
      packages=find_packages(),
      install_requires=[
          "happybase",
          "pyarrow",
          "pandas",
          "numpy",
          "requests",
          "python-decouple",
          "hdfs",
          "paramiko"
      ],
      extras_require={
          "dev": [
              "setuptools",
              "wheel",
              "pytest"
          ]
      },
      entry_points={
          'console_scripts': [
              'pct3=PVplr_stGNN:hdfs',
          ],
      },
      include_package_data=True
      )
from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='scd2',
    version='1.0.0',
    description="slowly changing dimension type 2 with pandas or parquet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/liranc/pandas_scd",
    packages=find_packages(),
    keywords=['scd', 'slowly changing dimension', 'type 2', 'pandas', 'parquet'],
    py_modules=["scd2"],
    package_dir={'':'src'},
    python_requires='>=3.8',
    install_requires=[
          'pandas',
          'pyarrow',
          'duckdb'
      ],
)

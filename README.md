# etl_economic_indicator

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Contributing](../CONTRIBUTING.md)

## About <a name = "about"></a>

etl_economic_indicator is a a python program that download the economic data indicators in investing.com and upload it to a sql server database


## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

First, you need to create a conda virtual environment together with python version 3.9.5 and at the same time install the dependencies in the requirements.txt file.

### Windows CMD Terminal
```
conda create --name TypeYourVirtualEnvironmentHere python=3.9.5 --file requirements.txt

```
Next, activate the virtual environment that you just created now. In the windows terminal, type the following commands.

### Windows CMD Terminal
```
conda activate TypeYourVirtualEnvironmentHere

```
### Installing

Next, after you have created a conda virtual environment with python version 3.9.5 together with the dependencies in the requirements.txt, you need to pip install sqlconnection (the "Module"). In the windows terminal, type the following codes below.

### Windows CMD Terminal
```
pip install version pip install git+https://github.com/Iankfc/etl_economic_indicator.git@master
```

To use the module in a pythone terminal, import the module just like other python modules such as pandas or numpy.

### Python Terminal
```
from etl_economic_indicator import get_economic_data_from_investing_com as etl
str_date_filter_from = '1/1/1970'
str_date_filter_to = '9/6/2021'

ged = etl.class_get_economic_data_from_investing_com(   str_start_date = str_date_filter_from,
                                                    str_end_date = str_date_filter_to
                                                )

df_economic_data = ged.func_df_get_economic_data(bool_upload_data_to_sqlserver_True_or_False = True,
                                                    bool_sqlserver_upload_append_or_replace = 'append')
```


## Usage <a name = "usage"></a>

The module can be use to for extract transform and load (ETL) flow of data science.

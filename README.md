# DruidQ

Simple druid cli to query druid using sqlalchemy.


## Installation

```bash
pipx install git+https://github.com/mmngreco/druidq
```


## Usage

```bash
druidq "select 1"
druidq ./query.sql
# Define your URL
DRUIDQ_URL='druid://localhost:8887/' druidq ./query.sql
DRUIDQ_URL='druid://localhost:8082/druid/v2/sql/' druidq ./query.sql
```


### Examples

You can try the following:

```bash
mkdir /tmp/druidq/
cd /tmp/druidq/
echo "select 1" > query.sql
export DRUIDQ_URL='druid://localhost:8887/'

druidq ./query.sql
druidq ./query.sql -e "print(df.shape)"

echo "print(df.shape)" >> script.py
echo "print(df.T)" >> script.py
druidq ./query.sql -e ./script.py
```

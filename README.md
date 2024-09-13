# DruidQ

Simple druid cli to query druid using sqlalchemy.


## Installation


```bash
pipx install git+https://github.com/mmngreco/druidq
```

> [!Note]
> I you are on MacOS I recommend creating a new venv and avoid using `pipx`


## Usage

```bash
# String
druidq "select 1"

# send python code
druidq "select 1" -e "print(df)"

# silent mode
druidq "select 1" -e "print(df)" -q

# no cache
druidq "select 1" -e "print(df)" -f

# file
druidq ./query.sql
# customs URLs
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

# read query from a file
druidq ./query.sql
druidq ./query.sql -e "print(df.shape)"

# use python scrits
echo "print(df.shape)" >> script.py
echo "print(df.T)" >> script.py
druidq ./query.sql -e ./script.py
```

You can also use the `execute` function only

```python
from druidq import execute

execute("select 1")
```

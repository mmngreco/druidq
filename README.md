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

# IMC Prosperity 4 Dashboard
## Overview
Dashboard for IMC Prosperity 4 for analysing and visualising the historical data provided each round. Several parts were
inspired from the [Frankfurt Hedgehogs](https://github.com/TimoDiehm/imc-prosperity-3) repo (particularly the use of the
mid wall) so I would highly recommend reading their writeup. Note that this is not designed as a visualiser for your
logs after you submit an algorithm but for the historical data. If you are looking for a logs visualiser then Jasper may
release one soon similar to his [IMC Prosperity 3 Visualiser](https://jmerle.github.io/imc-prosperity-3-visualizer/).

The main components involve a [streamlit frontend](#streamlit-frontend) and a [data platform](#data-platform).
- Streamlit Frontend: Visualise the order book data and also the trades made. Use the sidebar to set any filters you
need.
- Data Platform: Stores the pipelines creating all the tables. You can then create your own notebooks to do your own
data exploration

I am aware this is an over-engineered project for what is actually needed but this was more for a learning experience
over what is most efficient. Please refer to the [Bugs section](#Bugs) if you are experiencing any problems.

Hopefully, this dashboard helps you get started with your journey in IMC Prosperity 4.

*This project is still in development and will be constantly changing throughout the competition (particularly to add
the new data from each round as they become available)*

---

## Quickstart
Install docker desktop from [here](https://docs.docker.com/desktop/) (or software to manage containers)
- Clone the repository
- From the root of the repository run `docker compose up -d`
- If you need to refresh the application, avoid using `docker compose stop` and `docker compose start` as the spark pipelines have bugs which mean the tables
will only create properly when fully refreshed by `docker compose down` and `docker compose up`

This will start to build the images and containers for the application (this may take a while to set up on your computer
for the first time). There may be delays for the data platform to set up as it needs to wait for the spark connect
server and then run pipelines. Therefore, the frontend won't work until this has completed.

User Interface Servers:
- Streamlit Frontend - http://localhost:8501/
- Unity Catalog UI - http://localhost:3000/

_Refer to the sections below for more in depth detail_

---

## Streamlit Frontend
Once the pipelines have completed (check the logs of the data platform container, and you should see that the API has
started) go to http://localhost:8501/ to see the dashboard.

The following image shows the main order book chart and all the filters that you can select in the sidebar.

![Image of the main dashboard](/assets/images/dashboard.png)

<br>

## Data Platform
Dependencies:
- Install Java 17 from [here](https://www.oracle.com/uk/java/technologies/downloads/) as this is required by pyspark.
  (Ensure JAVA_HOME env variable is set correctly)
- We will be using [uv](https://docs.astral.sh/uv/) as our package manager
- Also make sure the application is running as we need to connect to the spark-connect server

Go to the `data-platform` folder at the root of the repository and run `uv sync`. This should install all the required
packages and set up the virtual environment for you. Ensure you activate the environment before continuing (e.g. for Mac
users, run `source .venv/bin/activate`).

*This is a monorepo with multiple environments so please ensure you are using the correct one*

The pipelines in the data platform follow the medallion architecture (bronze, silver, gold) so use the bronze tables if
you want to look at the original data (the only change is that round and day columns have been added). The
catalogs, schemas and tables are managed by unity catalog so look through the Unity Catalog UI: http://localhost:3000/
to see what tables are available to you (ignore the default unity catalog)

Follow the example notebook located at `data-platform/notebooks/example_notebook.ipynb`. This will show you how to load
the spark table and also convert it into a pandas dataframe.

Always start your code like the following to connect to the server.
```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.remote("sc://localhost:15002")
```

You can then use SQL to query tables
```python
df = spark.sql("SELECT * FROM imc_prosperity.bronze.prices")
# Continue with spark if you prefer using SQL
```

You can also convert to a pandas dataframe if you prefer
```python
df = spark.sql("SELECT * FROM imc_prosperity.bronze.prices")
pandas_df = df.toPandas()
```

Several packages such as `matplotlib` and `scikit-learn` have already been installed but feel free to install any extra
packages that you need.

---

## Bugs
This is a solo project which may contain a lot of bugs. If your problem isn't listed then please feel free to contact me
and I will do my best to help.

**API Internal Error** - This can occur if you change filters too fast as it sends too many API calls, simply adjust a
filter (such as clicking the plus on trade quantity) to get the app to rerun or refresh the page

**Catalog not found** - This can occur if the unity catalog server takes too long to start, meaning the initial commands
to create the catalogs and schemas aren't run. The setup for this isn't ideal, but you can go into the unity catalog
docker compose file located in `infra/unity-catalog` and increase the sleep time seen in the command section.

**Table already exists (or doesn't support truncates)** - I am unsure of the exact reason this error occurs but the
pipelines seem to fail if the table already exists (instead of just refreshing them) so run `docker compose down` and
`docker compose up -d` again to refresh the table data (I have purposely not saved the table data in a volume due to
this error)

**API not running** - This is likely to be because the data platform hasn't finished setting up yet. Simply wait for the
pipelines to finish running. Go into the data platform container logs, and you should see `Running pipelines...` followed
by `Pipelines complete. Starting API...` when it is finished. This may also take some time as spark needs to wait for
the spark-connect server to start (takes longer as it is downloading the jars for unity catalog integration)


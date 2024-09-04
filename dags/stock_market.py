from airflow.decorators import dag, task
from datetime import datetime
from airflow.models.baseoperator import chain
from airflow.hooks.base import BaseHook
from airflow.sensors.base import PokeReturnValue
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.providers.slack.notifications.slack import SlackNotifier
from airflow.operators.python import PythonOperator
from include.stock_market.tasks import _get_stock_prices, _store_prices, _get_formatted_prices_from_minio
from astro import sql as aql
from astro.files import File
from astro.sql.table import Table, Metadata
import sqlalchemy
import requests

SYMBOL='AAPL'

@dag(
    start_date=datetime(2023, 1, 1),
    schedule='@daily',
    catchup=False,
    tags=['stock_market'],
    on_success_callback=SlackNotifier(
        text="{{ dag.dag_id }} DAG succeeded!", 
        channel="#monitoring", 
        slack_conn_id="slack"),
)
def stock_market():

    @task.sensor(poke_interval=30, timeout=3600, mode='poke')
    def is_api_available() -> PokeReturnValue:
        api = BaseHook.get_connection('stock_api')
        url = f"{api.host}{api.extra_dejson['endpoint']}"
        response = requests.get(url, headers=api.extra_dejson['headers'])
        condition = response.json()['finance']['result'] is None # <-- changed
        return PokeReturnValue(is_done=condition, xcom_value=url)

    get_stock_prices = PythonOperator(
        task_id='get_stock_prices',
        python_callable=_get_stock_prices,
        op_kwargs={'url': '{{ ti.xcom_pull(task_ids="is_api_available") }}', 'symbol': SYMBOL},
    )

    store_prices = PythonOperator(
        task_id='store_prices',
        python_callable=_store_prices,
        op_kwargs={'prices': '{{ ti.xcom_pull(task_ids="get_stock_prices") }}'},
    )

    format_prices = DockerOperator(
        task_id='format_prices',
        max_active_tis_per_dag=1,
        image='airflow/spark-app',
        container_name='trigger_job',
        environment={
            'SPARK_APPLICATION_ARGS': '{{ ti.xcom_pull(task_ids="store_prices")}}'
        },
        api_version='auto',
        auto_remove=True,
        docker_url='tcp://docker-proxy:2375',
        network_mode='container:spark-master',
        tty=True,
        xcom_all=False,
        mount_tmp_dir=False
    )

    get_formatted_csv = PythonOperator(
        task_id='get_formatted_csv',
        python_callable=_get_formatted_prices_from_minio, 
        op_kwargs={'location': '{{ ti.xcom_pull(task_ids="store_prices") }}'},
    )

    load_to_dw = aql.load_file(
        task_id='load_to_dw',
        input_file=File(path='{{ ti.xcom_pull(task_ids="get_formatted_csv") }}', conn_id='minio'),
        output_table=Table(
            name='stock_prices',
            conn_id='postgres',
            metadata=Metadata(schema='public'),
            columns=[ # the order matters!
                sqlalchemy.Column('timestamp', sqlalchemy.BigInteger, primary_key=True),
                sqlalchemy.Column('close', sqlalchemy.Float),
                sqlalchemy.Column('high', sqlalchemy.Float),
                sqlalchemy.Column('low', sqlalchemy.Float),
                sqlalchemy.Column('open', sqlalchemy.Float),
                sqlalchemy.Column('volume', sqlalchemy.Integer),
                sqlalchemy.Column('date', sqlalchemy.Date),
            ]
        )
    )

    chain(
        is_api_available(),
        get_stock_prices,
        store_prices,
        format_prices,
        get_formatted_csv,
        load_to_dw)

stock_market()
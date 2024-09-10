"""
docker exec -it spark-master /opt/bitnami/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  --deploy-mode client \
  app.py
"""

import pandas as pd

from pyspark.sql.types import StringType
from pyspark.sql.functions import pandas_udf

from utils.utils import init_spark_session, list_files


def main():
    spark = init_spark_session("elt-rides-fhvhv-py-berry")



if __name__ == "__main__":
    main()
import os
import random
import datetime
from sparkmeasure import StageMetrics
from pyspark.sql import SparkSession
from utils.utils import init_spark_session, list_files

def gerar_feedbacks(num_feedbacks):
    feedbacks = []
    for i in range(num_feedbacks):
        feedback = {
            "customer_id": random.randint(1000, 9999),
            "timestamp": datetime.datetime.now().isoformat(),
            "ip_address": f"192.168.1.{random.randint(1, 255)}",
            "os": random.choice(["Windows", "MacOS", "Linux"]),
            "os_version": "10.0" if random.choice(["Windows", "MacOS"]) == "Windows" else "18.04" if random.choice(["Linux"]) == "Linux" else "12.0"
        }
        feedbacks.append(feedback)
    return feedbacks

def main():
    spark = init_spark_session("elt-app")

    stage_metrics = StageMetrics(spark)
    stage_metrics.begin()

    num_feedbacks = 30
    dados_feedback = gerar_feedbacks(num_feedbacks)
    df = spark.createDataFrame(dados_feedback)
    df.show(truncate=False)

    # Encerrar a medição de estágios
    stage_metrics.end()
    stage_metrics.print_report()

    metrics = stage_metrics.aggregate_stagemetrics()
    print(f"metrics elapsedTime = {metrics.get('elapsedTime')}")

    # Corrigindo o erro de tipo na concatenação
    metrics_elapsed_time = metrics.get('elapsedTime')
    output_path = str(metrics_elapsed_time) + "_stagemetrics"

    df_stage_metrics = stage_metrics.create_stagemetrics_DF("PerfStageMetrics")
    df_stage_metrics.repartition(1).orderBy("jobId", "stageId").write.mode("overwrite").json(output_path)

    # Criar resumo das métricas de estágio
    df_stage_metrics_summary = stage_metrics.aggregate_stagemetrics_DF("PerfStageMetrics")
    df_stage_metrics_summary.write.mode("overwrite").json(str(metrics_elapsed_time) + "_stagemetrics_summary")

if __name__ == "__main__":
    main()

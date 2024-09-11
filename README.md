
# Execucao da aplicação

> docker exec -it $(docker ps -qf "name=spark-master") /opt/bitnami/spark/bin/spark-submit \
--master spark://spark-master:7077 \
--deploy-mode client \
/opt/bitnami/spark/jobs/app.py

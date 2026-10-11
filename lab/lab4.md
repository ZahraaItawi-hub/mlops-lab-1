Question 1: 

Without a volume, MLflow stores its database, experiments, and model artifacts inside the container.

If I stop and restart the same container, the data remains. However, if I remove the container and create a new one, the previous data is lost.

A new MLflow container would start with an empty database, so I would no longer see my previous experiments or registered models in the UI.



Question 2: 

A named volume is managed by Docker and keeps the MLflow data even when containers are removed. It is easier to manage because Docker handles the storage location.

A bind mount would also work, but I would need to choose and manage a folder on my computer and make sure the permissions are correct.

For this lab, a named volume is a simple way to keep the MLflow database and model artifacts safe.



Question 3: 

In Lab 4, Docker Compose automatically creates a private network connecting the three services.

Docker also provides DNS resolution, so containers can find each other using their service names.

This allows the inference container to communicate with MLflow using  http://mlflow:5000.

In Lab 3, MLflow was running on my computer outside Docker, so I needed  host.docker.internal  to reach it.



Question 4:



Using an environment variable makes the frontend more flexible.

Inside Docker Compose, the frontend uses  http://inference:8000  because  inference  is the service name.

If I run the frontend separately outside Compose, that hostname might not work. I can provide a different URL, such as  http://127.0.0.1:8000 , without changing the Python code.

This allows the same frontend image to work in different environments.



Question 5:



The inference service does not need a published port because users do not access it directly from their computers.

Instead, the frontend communicates with inference through Docker Compose's private network using  http://inference:8000 .

Only MLflow and Streamlit publish ports because we need to open their web interfaces in the browser.



Question 6: What happens if inference starts before MLflow is ready?



The  depends\_on  setting controls the order in which Docker starts containers, but it does not guarantee that MLflow is ready to accept requests.

If inference tries to load the model before MLflow is ready, the connection can fail and the inference application may exit.

We experienced startup problems during our lab because inference could not initially communicate with MLflow. We also encountered a 403 error caused by MLflow's hostname security settings.



After correcting the configuration and restarting inference, the model loaded successfully and the API started responding.

A better solution would be to add a health check or retry mechanism so inference waits until MLflow is ready.



Question 7:



When I ran  docker compose ps , I saw that:



\- MLflow published port  5000:5000 .

\- Frontend published port  8501:8501 .

\- Inference showed port  8000/tcp  without publishing it to the host.



This matches my  docker-compose.yml .

MLflow is available at  http://localhost:5000 , and Streamlit is available at  http://localhost:8501 .

The inference service is accessible to the frontend through the internal Docker network.



Question 8: 

Refreshing the frontend does not automatically load a new model version.

This is because my  serve.py  loads the registered model only once when the inference application starts.

Even if the model alias is changed in MLflow, the running inference service continues using the model already loaded in memory.

To load the newly selected model version, I can run:

&#x20;docker compose restart inference 

This restarts the inference application, which loads the model again from MLflow.

In my project, I use the  champion  model alias instead of the older  Staging  stage.



Question 9:

Restarting works because the trained model is not permanently stored inside the inference Docker image.

The image contains the application code and its dependencies.

When inference starts, it connects to MLflow and loads the model associated with the configured alias.

Therefore, restarting the container allows it to fetch the currently selected model version without rebuilding the image.

A rebuild would only be necessary if I changed something included in the image, such as the application code or dependencies.



Question 10: 

Running  docker compose down  stops and removes the containers and their Compose network, but it keeps named volumes.

When I run  docker compose up  again, MLflow can reuse the existing volume, so its experiments, registered models, and model aliases should still be available.

However,  docker compose down -v  also removes the named volume.

If I run Compose again afterward, Docker creates a new empty volume, and the previous MLflow database and artifacts are no longer available.

This shows why volumes are important for keeping data between container recreations.



Question 11:

Docker Compose is mainly designed to manage containers on one machine.

For a larger production application, I would need an orchestration platform such as Kubernetes.



Kubernetes can run multiple replicas of the inference service, distribute traffic through a Service and load balancer, restart failed containers, and schedule workloads across multiple machines.

For MLflow to survive a machine failure, I would also need reliable shared storage for model artifacts and a persistent external database instead of depending only on storage on one machine. This would make the system more scalable and reliable.


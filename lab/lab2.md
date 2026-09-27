Question 1



After adding the training libraries, pyproject.toml was updated with the new dependencies like MLflow, PyTorch, torchvision and scikit-learn. I also used the CPU-only version of PyTorch because I do not need CUDA for this lab. The uv.lock file was updated as well because it keeps the exact versions of the installed packages and their dependencies.



Question 2



The --backend-store-uri tells MLflow where to save the information about the experiments and runs. In my case, this information is stored in mlflow.db, which contains things like the parameters, metrics and run information.



The --default-artifact-root tells MLflow where to save the files created by the runs. In my case, these files are saved in the mlruns folder and can include the trained model.



So basically, the metadata is the information about the experiment, while the artifacts are the actual files produced by it.



Question 3



mlflow.db and the mlruns folder should not be tracked by Git because they are local MLflow files and they keep changing whenever experiments are run. They also do not need to be tracked by DVC because they are not part of the dataset. In this project, Git is used for the code, DVC is used for the dataset, and MLflow is used for the experiments and their results.



Question 4



The first time I used mlflow.set\_experiment("food11"), MLflow noticed that the food11 experiment did not exist yet, so it created it automatically. After running the code, I could see the new food11 experiment in the MLflow UI.



Question 5



mlflow.log\_param is used for values that are set before training and stay the same during the run, such as the learning rate, batch size and number of epochs. mlflow.log\_metric is used for results that change during training, such as the loss and accuracy.



The step argument is useful for metrics because it tells MLflow which epoch each value belongs to. This makes it possible to see how the results change from one epoch to another. Parameters do not need a step because they stay the same for the whole run.



Question 6



When I opened my run in the MLflow UI, I could see the parameters I used, such as the dataset, number of epochs, learning rate and batch size. I could also see the training loss, validation loss, validation accuracy and test accuracy. The trained model was also shown in the logged models section.



Since I started MLflow using --default-artifact-root ./mlruns, the model files are stored locally inside the mlruns folder in my project.



Question 7



After comparing the four runs, the best final validation accuracy came from the run with a learning rate of 0.0001 and a batch size of 32. It reached around 70.62% validation accuracy and 74.27% test accuracy.



In general, a higher validation accuracy is better because it means the model is correctly predicting more examples that it did not train on. However, I would also look at the validation loss to make sure the model is not overfitting.



Question 8



From the parallel coordinates plot, I noticed that changing the learning rate had a big effect on the results. A learning rate of 0.01 gave the lowest validation accuracy at around 16.88%, while 0.0001 with a batch size of 32 gave the highest result at around 70.62%.



I also noticed that with a learning rate of 0.001, a batch size of 64 performed better than a batch size of 32. Based on these experiments, the smaller learning rate worked better for this model.



Question 9



After sorting the runs by validation accuracy, the best run was clean-owl-287. It reached a final validation accuracy of around 70.62% using a learning rate of 0.0001 and a batch size of 32.



The Run ID of the best run is:

28c4e9798013413998f0679d61730af5


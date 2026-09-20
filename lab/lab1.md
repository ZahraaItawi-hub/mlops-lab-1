Question 1



After I used  uv init , I noticed that it created the basic files needed for the Python project. The  src  folder is where the Python code goes, while  pyproject.toml  contains the project information and dependencies. There is also  .python-version  which tells which Python version the project uses, and  README.md  which can be used to write information about the project.



Question 2



When I ran  dvc init , it created the  .dvc  folder and  .dvcignore . From what I understood, the  .dvc  folder contains the configuration that DVC needs to work in the project, while  .dvcignore  tells DVC what it should ignore. These files can be pushed to Git as long as they don't contain any secret information because they are part of the setup of the project.



Question 3



For my case I used a local DVC remote instead of DagsHub. I created it outside my Git repository at  C:\\Users\\Admin\\dvc-storage . Because it is a local folder on my computer, I didn't need a username or password for it. If I was using DagsHub, the credentials could be saved using different DVC configuration options like local or global configuration. Credentials should not be pushed to GitHub because they are private. The normal DVC configuration that doesn't contain secrets can be pushed.



Question 4



After running  dvc add data , I checked  .gitignore  and saw that  /data  was added to it. This means Git will not track all the images inside the data folder. Instead, DVC is responsible for tracking the data, while Git only needs to track the DVC pointer file. This makes more sense because the dataset is much bigger than the normal code files.



Question 5



After adding the data to DVC, a  data.dvc  file was created. When I opened it, I saw information such as the MD5 hash, size, number of files and the path  data . My raw dataset version had 16,643 files. I understood that this file is basically how DVC knows which version of the data belongs to the project, without Git having to store all the actual images.



Question 6



When I checked GitHub, I could see my project files and  data.dvc , but the actual food images were not there. The images are handled separately by DVC. Since I used a local remote, running  dvc push  stored the data in  C:\\Users\\Admin\\dvc-storage . So basically GitHub is keeping my code and the information about the data version, while DVC is keeping the actual dataset.



Question 7



I tested this by cloning the GitHub repository into another temporary folder. After cloning it, I noticed that the actual  data  folder was not there, even though  data.dvc  was there. I then ran  dvc pull  and DVC fetched the data from my local remote and restored the data folder with 16,643 files. This helped me understand that cloning Git alone doesn't download the actual DVC data, and  dvc pull  is needed for that.



Question 8



I tested the different data versions by going back to the older Git commit and then running  dvc checkout . When I did this,  food11\_processed  and  food11\_processed\_mini  disappeared and I only had  food11\_raw . Then I switched back to the  main  branch and ran  dvc checkout  again, and both processed folders came back. So I understood from this that Git can be used to select the project version and DVC can restore the data that belongs to that version.


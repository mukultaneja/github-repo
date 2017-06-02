# Github Repository Visualization

**Introduction :**
This is one of my personal project in which I am implementing my data visualization and scraping skills. This project has been developed using **D3.js, Python, Scrapy and sqlite database**.

The core idea behind this project is to create an interactive visualization of github server. Using the visualization, a normal user can get an idea about the following. 

1. Which is the most used language in the projects hosted over the github server?
2. Which is the most popular language used to create open source and personal projects?
3. Distribution of public repositories based on meta data such as number of forks / number of contributors / number of starred for a particular repository.

This project is currenlty under **developement**. I have written **scrappers and created sqlite DB structure** to store raw data so far. Apart from it, I have written a **tornado server** as well to run the default view where user can see the interactive visual of aggregate number of public repositories for the specific programming languages.

##### To run scrappers :

1. To scrap data from github v3 API, one has to register its own [application](https://github.com/settings/developers) and create [access token](https://gist.github.com/caspyin/2288960) as well to authenticate itself to github v3 API.
2. After step 1, run ``python build_schema.py`` from project directory to create a sqlite db named **repos.db** inside of **db directory**.
3. To start scrappers, go to **github-repo/scrappers/repovis/repovis** and run ```python download_repos.py```. It will internally create a new process which calls the **scrapy framework** to download all the public repositories data and store it into the sqlite db along with th required meta data information.
4. To load the default view, run ```python index.py``` and go to **localhost:8888 **on browser.
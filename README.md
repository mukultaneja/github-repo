# Github Repository Visualization

**Introduction :**
To the introduction, this project is to find out the most popular programming languages for open source projects. The idea is to scrap public repositories data from Github Server using its own public API and to align the repositories according to their used programming languages. Finally, I am representing this data information in the form of visualization which listed out most popluar languages which people are using while working on open source projects.

**Technologies :**
I have used multiple technologies to create this tool and it consists multiple steps from scrapping to visualization of the data. Primarily this project has been developed using **D3.js, Python Tornado Framework, Scrapy Framework and sqlite database**.

**Working :**
This is purely an open source proect, So I am sharing my code and all the processings behind the proect here (Ideas are always welcome to make it better :)). As I said earlier, this project consists multiple steps from scrapping data to visualization. So I would like to clear every step here,

**Init Process**
	To scrap data from github v3 API, one has to register its own [application](https://github.com/settings/developers) and create [access token](https://gist.github.com/caspyin/2288960) as well to authenticate itself to github v3 API.

**Stroing the Scrapped Data**
	Github Server returns a JSON structure corresponding to one repository. Firstly, I am loading this structure into the main memory using pandas library and then creating a relational structure between repositories, its owners and several other informations such as forks/ languages / contributors. Finally, I am using sqlite database to store this relational structure.

**Running Scrappers**
	I am running scrappers through cronjobs on my local machine. It is a continous process and Github allows 5000 requests per hour for authenticated users. So I am running this job in every 6 seconds on my local maching and fetching the data from Github Servers. 
	
**Visualizing Data**
	Apart from scrappers & relational database, I have written a tornado server to access all this data information in a clean and better manner using REST API and finally I am putting this data information into d3.js at the client side and creating an interactive visual.


Please visit the [link](https://mukultaneja.github.io/analysis/github-repos/) to find the implementation as of now.
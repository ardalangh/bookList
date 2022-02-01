### Reading List 
#### A reading list application powered using google books API.

**Live Demo:** 
https://googleapireadinglist.herokuapp.com/
---

**Technologies Used:**

Django Framework is being used Topower the backend

Django's Template system is used to generate HTML dynamically. 

<p align="center">
<img src="https://static.djangoproject.com/img/logos/django-logo-negative.svg" width="100px" >
</p>


**API Used:**
Google Books Api is used for querying book searches. 
<p align="center">
<img src="https://upload.wikimedia.org/wikipedia/commons/8/8d/Google_Play_Books_icon_%282016%29.svg" width="50px" >
</p>


**Requests: HTTP for Humans™ 2.26.0**
<p align="center">
<img src="https://docs.python-requests.org/en/latest/_static/requests-sidebar.png" width="50px" >
</p>


**python-dotenv 0.19.2** is used to load the api key from the env variables 


--- 

**Getting Started:**

```shell
    # AFTER ADDING YOUR GOOGLE API KEY TO THE ENV VARIABLE   
    # install pipenv if you haven't already    
    pip install pipenv 
    # activate the env     
    pipenv shell
    # run the server
    python manage.py runserver     
```

---
**Features:**

1. User can search for any books available on Google's database and add it to their reading list.
![title](readmeAssets/dash.png)
2. User can get more information on individual books. 
![title](readmeAssets/detail.png)
3. User can change their image
![title](readmeAssets/changeImg.png)




**Requirements**

*You can install the requirements using the command:*

```pip install -r requirements.txt``` 

*this will install the following needed packages :*

* Flask==1.1.2

* Flask-SQLAlchemy==2.5.1

* SQLAlchemy==1.4.15


**Start the code**

*You can start the code when you are in the directory of the files using the command:*

```python case.py```

**Post Request**

*To make a post request, which allows you to insert a url and a shortcode for that url, you can use the curl command with the following parameters in your shell, like in the following example :*

```curl localhost:5000/shorten -d "{\"url\": \"https;//www.energyworx.com\",\"shortcode\": \"en0001 \" }" -H 'Content-Type: application/json'```


*where https://www.energyworx.com is the url, and en0001 is the shortcode. It will return the shortcode value if valid.*

**Get Request**

*To make a get request returning the header to redirect you to the url you can use the following command:* 

```curl localhost:5000/<shortcode>```

**Get stats Request**

*To make a get request returning the header with statistics you can use the following command:*
 
```curl localhost:5000/<shortcode>/stats```

**Start Unit Tests**

*To run the unit tests you can use the following command in your shell:*

```python -m unittest unit_tests.py```


**Comment**

*If there had been more time available, I would have tried to create some additional unit tests and would have documented their functionality.*



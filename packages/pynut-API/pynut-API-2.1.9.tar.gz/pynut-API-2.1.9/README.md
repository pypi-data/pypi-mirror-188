# py2nut - Laurent Tupin

It provides various functions to simplify the users life. 


## Installation

You can install the package from [PyPI](https://pypi.org/project/pynut-API/):

    python -m pip install pynut-API

The package is supported on Python 3.7 and above.



## How to use


You can call a function as this example:

    $ ----------------------------------------------------
    >>> from pyNutApi import nutDate
    >>> nutDate.today()



This is the libraries I am using with the package

    $ ----------------------------------------------------
    >>> beautifulsoup4==4.7.1
    >>> pandas==1.1.3
    >>> selenium==3.141.0


To use nutApi / Selenium Functionnalities:
    
    #----------------------------------------------------
    # To use Chrome Driver
    #  Go to chromedriver.chromium.org || https://sites.google.com/a/chromium.org/chromedriver/downloads
    #  Chose an older version (like the 92 as of August 2021)
    #  download and UnZip the folder
    #  Move it to Users/local/bin
    #   or C:\ProgramData\Anaconda3\Library\bin (Windows)
    #   or ...\AppData\Local\Programs\Python\Python39
    #----------------------------------------------------



## Documentation


Temporary documentation for nutApi :

    from pyNutApi import nutApi as Api
        
    1. Class
    
    inst_getAPI = Api.C_API_simple( (str_uid, str_pwd) )
    inst_getAPI.api_connect_json( url )
    inst_getAPI.api_returnDataFrame( l_url_keyword = ['data', 'price'] )
    df_data = inst_getAPI.df_return
    """ The class inherit from C_API 
            allows the user to read an URL and get back a dataframe from JSON format
        Is decorated to be a singleton"""
    

***END***
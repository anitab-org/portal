Automated Testing 
=================

Documentation on running automated tests with selenium for systers/portal.

Setup Selenium (Unix)
---------------------

To run selenium test you would need to install (download) the standalone servers which implements WebDrivers' wire protocols : 
* geckodriver and
* chromedriver 

is used here not withstanding, other WebDriver servers may be used with a little tweaking (which entails adding the desired webdriver in the browsers dictionary in the conftest.py) 

### Installation 

1. Download chromedriver [here](https://sites.google.com/a/chromium.org/chromedriver/home)
1. Download geckodriver [here](https://github.com/mozilla/geckodriver/releases)

Get latest versions, and make sure the version downloaded is meant for your OS and is compatible (32/64 bits)

After downloading, extract both drivers and save in a directory (e.g webdrivers) in a location of choice, finally let selenium know where it can find the webdrivers by exporting the paths to the various executables, you would have to do this every time your (re)start you venv (or any enviroment for that matter) 

```bash
export PATH=$PATH:/path/to/directory/of/executable/downloaded/
```

That is quite boring you can just make each of them available globally once and for all 

```bash
sudo mv geckodriver /usr/local/bin 
sudo mv chromedriver /usr/local/bin
```

You can also write a .bashrc script and export, to avoid the repetition this method however has thesame effect as simply moving the files to ```/usr/local/bin``` above.

Note : Be sure to export only the directory(ies) containing the executables without including the executables to avoid the "NotADirectoryError: [Errno 20] Not a directory"

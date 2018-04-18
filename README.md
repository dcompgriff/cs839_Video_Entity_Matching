# 839 Project Stage 3: IMDB and Movie Numbers Web Page Movie Entity Matching.

## Introduction

This project follows the guidelines for AnHai's CS 839 Data Analysis course for project stage 3, and contains an entity matcher model (a random forrest), along with the blocking code, train and test data set, and extra corpus files used for performing featurization.

BONUS COMMENTS: 
0) I used conda install -c anaconda pyqt to install the pyqt5 dependencies with anaconda 2 on MacOS Sierra.
1) You should have some test script that checks to ensure everything is 
working correctly after installation of all of the packages. Right now, you install 
everything, but you don't know if everything is working until you start trying to 
run code. 
2) You might want to think about creating a "conda_install.sh" script that will install 
not only the py_entitymatcher, but also the necessary dependencies, rather than having 
a user download and install everything manually.
3) I would break the machine learning capability out of the py_entitymatcher tool, and 
focus the tool more on just the entity matching part, and feature generation. I think 
including the machine learning, while potentially beneficial to some people who don't 
know about ML (But if they use the tool, they probably know ML), it puts more to maintain 
in the py_entitymatcher and somewhat locks down the matcher to future changes in the 
field of ML, ML models, and other ML package capabilities. I think that the tool should 
maintain the Unix style philosophy, which is do 1 thing, do it well, and make it easy 
to compose the tool with other tools (aka things like stdinput pipe handling, and output 
that is clean, etc...). The more compact this tool, the simpler it will be to be able 
to use and maintain it, and the more likely it will be that the industry adopts the 
tool. The simpler to install, use, and compose with other tools it is, the more likely 
the chances of widespread adoption will be.
4) Your links on this web page: http://anhaidgroup.github.io/py_entitymatching/v0.3.x/singlepage.html, for 
running ipy notebooks indicates that the link is a .ipynb file. But it is actually an html web page, and 
in that web page there is a link to download a .json ipy notebook. So this can be a bit confusing.
5) Your ipy notebooks are specific to the user "pradap" that created the notebook, and are not generalized. I 
ran into errors when running one of the notebooks bc of this.
6) You should make a docker file that can be run for this package.
7) Current anaconda compiled package for anaconda2 on MacOS Sierra "10.13.4" runs into issues with error:
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/anaconda2/lib/python2.7/site-packages/py_entitymatching/__init__.py", line 42, in <module>
    from py_entitymatching.debugblocker.debugblocker import debug_blocker
  File "/anaconda2/lib/python2.7/site-packages/py_entitymatching/debugblocker/debugblocker.py", line 14, in <module>
    from py_entitymatching.debugblocker.debugblocker_cython import \
ImportError: dlopen(/anaconda2/lib/python2.7/site-packages/py_entitymatching/debugblocker/debugblocker_cython.so, 2): Symbol not found: __ZNSt11logic_errorC2EPKc
  Referenced from: /anaconda2/lib/python2.7/site-packages/py_entitymatching/debugblocker/debugblocker_cython.so
  Expected in: /usr/lib/libstdc++.6.0.9.dylib
 in /anaconda2/lib/python2.7/site-packages/py_entitymatching/debugblocker/debugblocker_cython.so
8) Error when installing using pip: "Cannot remove entries from nonexistent file /anaconda2/lib/python2.7/site-packages/easy-install.pth"
Fixed by echoing an empty string to easy-install.pth file, and installing through pip without the "-U" option, which caused 
PyPrind-2.11.1 to be upgraded to PyPrind-2.11.2, but caused the installation error:
Successfully installed PyPrind-2.11.2 backports.functools-lru-cache-1.5 kiwisolver-1.0.1 matplotlib-2.2.2 py-entitymatching-0.3.0 python-dateutil-2.7.2 pytz-2018.4
Traceback (most recent call last):
  File "/anaconda2/bin/pip", line 11, in <module>
    sys.exit(main())
  File "/anaconda2/lib/python2.7/site-packages/pip/__init__.py", line 248, in main
    return command.main(cmd_args)
  File "/anaconda2/lib/python2.7/site-packages/pip/basecommand.py", line 252, in main
    pip_version_check(session)
  File "/anaconda2/lib/python2.7/site-packages/pip/utils/outdated.py", line 102, in pip_version_check
    installed_version = get_installed_version("pip")
  File "/anaconda2/lib/python2.7/site-packages/pip/utils/__init__.py", line 838, in get_installed_version
    working_set = pkg_resources.WorkingSet()
  File "/anaconda2/lib/python2.7/site-packages/pip/_vendor/pkg_resources/__init__.py", line 644, in __init__
    self.add_entry(entry)
  File "/anaconda2/lib/python2.7/site-packages/pip/_vendor/pkg_resources/__init__.py", line 700, in add_entry
    for dist in find_distributions(entry, True):
  File "/anaconda2/lib/python2.7/site-packages/pip/_vendor/pkg_resources/__init__.py", line 1949, in find_eggs_in_zip
    if metadata.has_metadata('PKG-INFO'):
  File "/anaconda2/lib/python2.7/site-packages/pip/_vendor/pkg_resources/__init__.py", line 1463, in has_metadata
    return self.egg_info and self._has(self._fn(self.egg_info, name))
  File "/anaconda2/lib/python2.7/site-packages/pip/_vendor/pkg_resources/__init__.py", line 1823, in _has
    return zip_path in self.zipinfo or zip_path in self._index()
  File "/anaconda2/lib/python2.7/site-packages/pip/_vendor/pkg_resources/__init__.py", line 1703, in zipinfo
    return self._zip_manifests.load(self.loader.archive)
  File "/anaconda2/lib/python2.7/site-packages/pip/_vendor/pkg_resources/__init__.py", line 1643, in load
    mtime = os.stat(path).st_mtime
OSError: [Errno 2] No such file or directory: '/anaconda2/lib/python2.7/site-packages/PyPrind-2.11.1-py2.7.egg'
9) Your ipynb files have some simple deprecation warnings.
10) In the ipynb guides, you should use "predictions[predictions.predicted == 1].head()" to display results of predictions 
so that people can examine the potentially matching entities to understand that the matching has actually occurred. 
11) In the ipynb files, the notebooks say that the RF model has highest precision and recall, but I see 
the linear regression has highest precision and recall.
12) Giving an idea of the computational runtime of the debugger on some data set would be nice, or at least 
having a progress bar (like with the regular blocker) would be nice so that a user can gauge how long it will 
take to run the debugging phase. (We were running it initially with 10,956,134 tuple pairs)
13) The AttrEqBlocker doesn't seem to work for us on our tables when matching equivalence of years.
14) ADD AN OPTION TO LOAD A LIST OF LABELS FROM A FILE!!!!! Generate the metadata for the new column
automatically for the user so I don't have to use the UI tool for labeling a sample.





## Links

* [IMDB Website](http://www.imdb.com/list/ls032600534)
* [Movie Numbers Website](https://www.the-numbers.com/movies/\#tab=letter)
* [Data Folder](DATA/)- Generated .json and .csv data sets.
* [Code folder](CODE/) - Scripts for performing the parsing and generating the data sets.
* [Pdf Detailing The Project](839_Project_Stage_2.pdf) - Pdf describing the process of movie extraction in detail

## Running the Extractors

### Scraping the IMDB Website

Running the scraper to scrape the IMDB website is shown below. If you are running the scraper for the first time, then make sure to use the "--generate" optional argument. This optional argument tells the scraper to actually go to the web url to pull information for creating the .csv file, and generates a corresponding intermediate json file. If the json file has already been generated, then the optional --generate option can be dropped. However, this script assumes that the "imdb_movies.json" file has already been generated in that case, and that the file is in the same folder as the scraper script. Also note that if you already have a generated "imdb_movies.json" file generated and want to generate another file, you need to remove the original file first before generating a new file. If you don't, the parser will throw json parse errors.

```
cd CODE/
python scrapeIMDB.py --generate
```
### Scraping the Movie Numbers Website

Running this scraper is the same as running the previous scraper.

```
cd CODE/
python scrapeMovieNumbers.py --generate
```


## Built With

* [Python 3.4.3](https://www.python.org/)
* [Numpy 1.13.1](http://www.numpy.org/) - Numerical matrix lib
* [Pandas 0.21.0](https://pandas.pydata.org/) - Data manipulation lib
* [Scrapy 1.5.0](https://scrapy.org/) - Web scraping framework

## Authors

* **Daniel Griffin** - [dcompgriff](https://github.com/dcompgriff)






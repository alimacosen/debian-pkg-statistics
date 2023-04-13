# Debian Repository Contents File Packages Statistics

## 1. Description
Debian uses *.deb packages to deploy and upgrade software. The packages are stored in Debian repositories and each repository contains "Contents index". You can refer to [Debian mirror](http://ftp.uk.debian.org/debian/dists/stable/main/) to have an overall knowledge of the Contents indices.  

This application is a python command line tool that takes the architecture (amd64, arm64, mips etc.) as an argument and downloads the compressed gzip Contents file associated with it from a Debian mirror. Then the application parses the file and output the statistics of the top 10 (by default) packages that have the most files associated with them.  

You can refer to [Description of contents file format](https://wiki.debian.org/RepositoryFormat#A.22Contents.22_indices) and check `5.Development Thoughts` in this README file for more information.

## 2. Installation

### Option 1: Use the virtual environment provided
There is already a python virtual environment with all the dependencies needed under the root directory called `envdebian`. You can run the following command in the ternimal to activate the virtual environment.

```shell
source envdebian/bin/activate
```

### Option2 : Run in other python environments
If you prefer not to use the virtual environment provided, you can run the following command in any python3 (3.9 recommended) environment
```shell
python3 -m pip install -r requirements.txt
```

## 3. Usage
### Check the help manual
Run the following command in the root directory, and you will see the application's manual in detial:
```shell
python3 run.py -h
```

### Command format
There are another 3 parameters for this application, the command format is like this:

```
python3 run.py [-h] -a ARCH [-s SOURCE] [-k K]
```

- `-h`, `--help`:
    - (optional) Display the help manual.
- `-a`, `--arch`:
    -  (required) Target architecture of the contents indices file ( e.g. amd64, arm64, mips64el, i386 ).
- `-s`, `--source` :
    - (optional) Debian repository mirror source.
- `-k`, `--K`:
    - (optional) Top k packages information with most related files.

please use `-h` to see more information like optional parameters default values.

### Sample command
```shell
python3 run.py -a arm64
```

```shell
python3 run.py -a mips64el
```

```shell
python3 run.py -a all -s http://ftp.uk.debian.org/debian/dists/bullseye/main/ -k 20
```

## 4. Sample Output
```
Downloading Contents-arm64.gz from http://ftp.uk.debian.org/debian/dists/stable/main/Contents-arm64.gz ...

Parsing the contents ...

Top 10 packages with the most files for arm64:

    Package name                                       Num of files
1.  devel/piglit                                       51784     
2.  science/esys-particle                              18015     
3.  libdevel/libboost1.74-dev                          14332     
4.  math/acl2-books                                    12668     
5.  golang/golang-1.15-src                             9015      
6.  libdevel/liboce-modeling-dev                       7457      
7.  net/zoneminder                                     7002      
8.  libdevel/paraview-dev                              6178      
9.  localization/locales-all                           5956      
10. kernel/linux-headers-5.10.0-20-arm64               5860      

```


## 5. Development Thoughts
1. Investigation  
To understand the prerequisites of this assessment, I conducted research on the Debian repository and its contents file. Initially, I assumed that the link provided by Jon for the Debian mirror, http://ftp.uk.debian.org/debian/dists/stable/main/, was the location of the *.deb package repository that stores all the packages that package managers such as apt retrieve. However, I later discovered that the suffix was not .deb and the number of items on that page was limited, indicating that it couldn't be the package repository. Subsequently, I explored other directories such as http://ftp.uk.debian.org/debian/ and http://ftp.uk.debian.org/debian/pool/main/libr/libreoffice/ and conducted some online searches to develop a general understanding of the repository. (Please correct me if I'm wrong.)  
The repositories in Debian are hosted on official Debian servers or mirrors, and they are updated regularly to include the latest versions of software packages. Command-line tools like `apt-get` or `apt` download package using the metadata from the `"/debian/dists/"` directory to locate and download the required .deb files from the `"/debian/pool/`" directory, including information about available packages, their dependencies, and their version numbers.  
Paths like `"dists/$DIST/$COMP/Contents-$SARCH.gz"` and `"dists/$DIST/$COMP/Contents-udeb-$SARCH.gz"` stand for called `Contents indices`. Here `$DIST` means certain debian distribution, like `bullseye` and `bookworm`, `$COMP` means the component name (such as `main`, `contrib` or `non-free`), and `$SARCH` represents the architecture name (such as `amd64` or `arm64`).

2. Raw Data Inspection
In this assessment, I was asked to foucus on contents indices. Here's part of the Contents-i386.gz file from [here](http://ftp.uk.debian.org/debian/dists/stable/main/)
   ```
    bin/afio                                                utils/afio
    bin/bash                                                shells/bash
    bin/bash-static                                         shells/bash-static
    bin/brltty                                              admin/brltty
    bin/bsd-csh                                             shells/csh
    bin/btrfs                                               admin/btrfs-progs
    bin/btrfs-convert                                       admin/btrfs-progs
    bin/btrfs-find-root                                     admin/btrfs-progs
    bin/btrfs-image                                         admin/btrfs-progs
    bin/btrfs-map-logical                                   admin/btrfs-progs
    ...                                                     ...
    ```
    After reading [Description of contents file format](https://wiki.debian.org/RepositoryFormat#A.22Contents.22_indices) carefully, I knew that each contents file consist of 2 columns seperated by muiliple blank spaces, the first column represents for the filename, and the second column represents for the packages that provided this file, sepreated by comma and there's no blank spaces in or between package names.  


3. Main Task Break-down  
    My main task is
    > developing a python cli tool that takes the architecture as an argument and downloads the compressed Contents file associated with it from a Debian mirror. The program should parse the file and output the statistics of the top 10 packages that have the most files associated with them

    So the basic steps are:
    - Parsing the cli parameters
    - Downloading the corresponding contents file and decompressing it into processable format
    - Parsing the contents file based on the [Description of contents file format](https://wiki.debian.org/RepositoryFormat#A.22Contents.22_indices): count the total number of files that each package provides
    - Display the top 10 packages with most number of related files (the number of files provided by this package ranks top 10)


4. Application Design  
    I'm not sure if I'll be asked to develop this application further in the future, so I didn't write everything into a single python file, instead, I organized the app in a well-structureed way.  
    - `Argument parse`:  
    I leveraged built-in `argparse` package and do some little extension to the reqiurements in case in the future I'll be asked to make the app more flexible.
    I decided to allow the user to customize the mirror source and choose to display top k package statistics. If not explicted assigned, the application will follow the default requirements Jon offered.
    - `Singleton configuration`:  
    I realized the configuration would be used multiple times, but there's no need to create multiple instances which would cause a waste of resources and negatively effect the performance of the app, so I applied Singleton pattern to the Config class.
    The first time we create a Config instance, it will read `config.json` in the root directory to initilize the configureation. I exposed various methods like `get_mirror_src` and `set_mirror_src` to let other modules have access to the configureation safely.
    - `Downloader`:  
    The Downloader module is in charge of downloading and decompressing the target contents file. The downloader instance will conduct the job based on the configureation injected.  
    I used `try-except` blocks to capture potential exceptions in this process and make the program exit elegantly with readable error messages. 
    - `Parser`:  
    The Parser aims to do the statistics to the valid, decompressed, and decoded contents file as a string.  
    As it is described in [Description of contents file format](https://wiki.debian.org/RepositoryFormat#A.22Contents.22_indices):
        > Clients should ignore lines not conforming to this scheme.
    
        I process the contents file line by line, splitting each line into 2 columns, and ignoring lines which don't contains excat 2 columns. After that, I split the second column based on `","`, since the contents file guarantees there won't be white space in package names.  
        I leveraged nuilt-in `collections.Counter` to do the statistics, and passed the whole result to the next stage.
    - `Procedure of statistics`:  
    In this part, I defined a function to organize all the previous components in a pipe line and output the required results.  
    I hope the displayed statistics to be consistent in format no matter how many packages (top k) the user wants to see. So I used a indent calculator defined in `utils.py` to calculate the index indent to make the output column names align with the package names and file numbers.

   I tried to decouple components when designing the application and used proper design patterns and structure strategy to make the application iterable and safe to run. I hope you will like my work, and you are welcome to offer any suggestions.
## 6. Acknowledgments
**Author:** Fanglei Cai  
**Email:** [caifanglei1998@gmail.com](mailto:caifanglei1998@gmail.com)


  

# 2023_assignment1_urluckynum

  

*Software Development Process* course

Academic Year 2023-24

Master's degree course in Computer Science

University of Milan-Bicocca

  

  

## Group members

  

  

  

- Cristian Piacente 866020

  

  

- Marco Gherardi 869138

  

  

- Matteo Cavaleri 875050

  

  

  

## Application

  

  

  

This Python application shows the user's lucky number.

  

  

Through a database, it stores the lucky number associated with a certain user and returns it. If the user is not registered, it generates a number, saves it to the database, and returns it to the user.

  

  

## Pipeline

  

This CI/CD pipeline is based on the **python:slim** image, as our application was written in Python and the slim image is minimal.


---

  

### Global Variables

  

-  `PIP_CACHE_DIR`: Defines the pip cache directory. Specifying the location of the libraries is useful for the cache mechanism.

-  `MYSQL_USER`: A project-level variable containing the username of the desired MySQL user.

-  `MYSQL_PASSWORD`: A project-level variable containing the MySQL user password.

-  `TWINE_TOKEN`: A project-level variable containing the PyPI token, used for publishing the Python application in the release stage.

  

The project-level variables (`MYSQL_USER`, `MYSQL_PASSWORD`, and `TWINE_TOKEN`) are protected, making them accessible only from protected branches of the repository.

  

---

  

### Cached Paths

  

The following paths are stored in the global cache:

  

-  `venv/`: The Python virtual environment.

-  `.cache/pip`: The pip cache directory.

  

---

  

### before_script

  

Since every job requires Python, the following two commands are executed before each job:

  

-  `python -m venv venv`

-  `source venv/bin/activate`

  
  
  
  

---

  

### Build stage

  

#### Script

  

    pip install -r urluckynum/requirements.txt

  

#### Explanation

  

All the dependencies are stored in a file named **requirements.txt** (located in the urluckynum directory), and they are automatically installed by pip during this stage. Afterward, the cache mechanism is used to make the packages available for the next stages.

  

---

  

### Verify stage

Two distinct jobs, to perform the code quality checks and the security analysis separately, belong to this stage.

#### Scripts

  The first job's script invokes prospector, while the second job's script invokes bandit.
  
  
##### Prospector script

    prospector


##### Bandit script
    
    bandit -r urluckynum/

  

#### Explanation

  

This stage utilizes two libraries, **prospector** and **bandit**, for code quality checks and security analysis to ensure project quality.

  

Bandit, which performs security analysis on the code, takes the parameter `-r` to specify the path and check for security vulnerabilities in that directory and its subdirectories.

  

---

  

### Unit test stage

  

#### Script

  

    pytest -k "unit"

  
  

#### Explanation

  
  

This stage conducts a unit test using **pytest**.

  

Unit tests verify the functionality of individual code units, such as functions. In this case, the test focuses on the generation of a random number.

  

Pytest can distinguish between unit and integration tests by examining **markers** defined above the signature of a test function, and these markers are specified in the pytest.ini configuration file.

  

The `-k` parameter specifies the marker.

---

  

### Integration test stage


#### Services

-  **mysql**: Used for starting the MySQL server.

  

#### Job variables

 -  `MYSQL_ROOT_PASSWORD`: Required for the MySQL service; it stores the password for the MySQL root user, which is, by default, the same as the `$MYSQL_PASSWORD` variable.

-  `MYSQL_DATABASE`: Specifies the database name to use in the MySQL service; by default, it's *sys*.


It's also possible (in the script) to customize:

-   The MySQL hostname, specifying the host to connect to in the  `--db-host`  parameter. By default, it's set to  `mysql`  because this setting is required to connect to the GitLab MySQL service. However, our Python application also supports connections to external servers.
-   The MySQL port, by changing the  `--db-port`  parameter. By default, the value is set to 3306.

  

#### Script

  

    pytest -k "integration" --gitlab-user=$GITLAB_USER_LOGIN --db-name=$MYSQL_DATABASE --db-host=mysql --db-port=3306 --db-user=$MYSQL_USER --db-password=$MYSQL_PASSWORD

  
  

#### Explanation

  

This stage conducts integration tests using **pytest**. Integration tests verify that different parts of a system work together correctly, in this case, the **backend** and **database**. These tests are labeled with the integration marker, ensuring that pytest runs only those specific tests.

  

In addition, this stage provides the GitLab user and MySQL database credentials to the tests, enabling them to interact with these systems.

  

In this scenario, the application attempts to execute all the necessary tasks to display the user's lucky number. First, it connects to the database, then it executes queries to retrieve the user's lucky number (or stores it if the user is new). The user is identified by the `$GITLAB_USER_LOGIN` predefined variable, which contains the GitLab username.

  
  

---

  

### Package stage

  

#### Script

  

    python setup.py sdist bdist_wheel

  

#### Artifacts

  

-  `dist/*.whl`: Built Distribution

-  `dist/*.tar.gz`: Source Distribution

  

#### Explanation

  

In this stage, we used the libraries **setuptools** and **wheel**. We created a file, `setup.py`, to configure the package's structure correctly. The command `python setup.py sdist bdist_wheel` has two parameters because we need to create two artifacts: `sdist` is responsible for the creation of the source distribution (.tar.gz file), and `bdist_wheel` is responsible for the creation of the built distribution (.whl file). These two files are essential for the release stage.

  

---

  

### Release stage

  

The job that implements this stage can only be executed in the main branch ~~(we realize there is no need in our case, since `main` is the only possible branch, but it could turn out to be useful in the future)~~.

  

#### Script

  
  

    twine upload --username __token__ --password $TWINE_TOKEN dist/*

  

#### Explanation

  

The release stage exploits the **twine** library to publish the two artifacts produced in the previous stage (package) on **PyPI**, using a token (defined in a project-level variable).

  

The username must be `__token__` to specify a PyPI token is being used instead of credentials. Then, the $TWINE_TOKEN variable, used as the password, contains the secret needed to perform the upload.

  

---

  

### Docs stage

  

The job that implements this stage can only be executed in the main branch.
 
Instead of using MkDocs, which requires writing a Markdown file, we decided to use the **pdoc** library, which automatically generates the HTML without requiring any Markdown files.

#### Script

  

    pdoc -o public urluckynum/app

  

#### Artifacts

  

-  `public/`: This directory contains the static website generated by the pdoc library.

  
  

#### Explanation

  

The `docs` stage is implemented by the `pages` job. This job automatically generates a static website using the Python **pdoc** library, which retrieves information from the docstrings defined for each function in the `urluckynum/app` module. The command `pdoc -o public urluckynum/app` generates the website in the `public` folder using the `-o` parameter. The generated website is made available for the next automatic job, `pages:deploy`, which publishes the files on GitLab Pages based on the content in the `public` folder.

  
  

---

  



## Issues encountered

  
  

 - ### Testing
   
     
   
   #### Problem
   
     
   
   The tests, which are located in the ./tests folder, face the issue of
   not being able to access the app modules stored in ./urluckynum/app.
   For example, the unit test stage requires the use of the
   `generate_lucky_number` function defined in `urluckynum.app.lucky`.
   
     
   
   #### Solution
   
     
   
   To address this issue, we added the following line of code:
   
     
   
   >  `sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")`
   
     
   
   This code fixes the problem by adding the project root folder to the
   path variable, allowing the test files to access the "urluckynum"
   package and consequently, the app module that contains `lucky.py` and
   other essential Python source code files.




## Changelog for the 2nd submission

This section lists the changes that were made to optimize the pipeline execution for the 2nd submission, reducing the time taken by the 7 stages.


- Changed the Docker image from python:3.8 to **python:slim**.
- **Removed** the 'echo' commands, to avoid having useless output on the console.
- **Removed** the python service (it wasn't needed).
- Made the mysql service **local** to the integration test job, instead of using it globally.
- Added a **PIP_CACHE_DIR** global variable.
- Made the variables MYSQL_ROOT_PASSWORD and MYSQL_DATABASE **local** to the integration test job.
- **Removed** the Python bytecode files path from the cache.
- Added the **pip cache** directory to the cache.
- Splitted the verify job into **two jobs**.
- **Replaced** the DB_HOST and DB_PORT local variables in the integration test job **with their values**.
- **Replaced** the .pypirc configuration file in the release job **with two twine parameters** (--username and --password).
- Even though it doesn't affect the pipeline, **deleted** the **.gitignore** file.
# nflPlayerPerformance
collaborators: Long Chen, Melaku Dubie, Rich Lee and Kivan Polimis

To install and run:
Windows and OSX install instructions (Maverick & Yosemite):


Download and install Python 2.7 from [`here`](http://continuum.io/downloads#all)


2. Obtaining the files<br>
    Go to
3. Starting a Python virtual environment
 <br>
   For OSX:
   ~~~bash
   cd Python_venv
   conda create -n venv python=2.7
   source activate venv
   cd..
   ~~~
 <br>
   For Windows (use command prompt, not Git Bash):
   ~~~bash
   cd Python_venv
   conda create -n venv python=2.7
   activate venv
   cd..
   ~~~
   Now you are in the virtual environment!


5. Installing the required packages
    ~~~bash
    pip install -r Python_venv/requirements.txt
    ~~~

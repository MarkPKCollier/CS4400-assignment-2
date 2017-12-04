FROM ubuntu:14.04

# Update packages
RUN apt-get update -y

# Install Python Setuptools
RUN apt-get install -y python-setuptools

# Install pip
RUN easy_install pip

# Add and install Python modules
ADD requirements.txt /src/requirements.txt
RUN cd /src; pip install -r requirements.txt

# Bundle app source
COPY api.py /src/api.py
COPY work_stealing.py /src/work_stealing.py
COPY work_pushing.py /src/work_pushing.py
COPY utils.py /src/utils.py

EXPOSE  8000
CMD ["python", "/src/api.py", "-port_num=8000"]

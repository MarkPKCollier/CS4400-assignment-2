FROM nlknguyen/alpine-mpich

RUN sudo apk add --no-cache valgrind gdb

# Update packages
# RUN apt-get update -y

# Install Python Setuptools
# RUN apt-get install -y python-setuptools
RUN sudo apk add --no-cache py-setuptools

# Install pip
# RUN easy_install pip
RUN sudo apk add --no-cache py-pip python-dev

# Install MPI
# RUN sudo apt-get install libcr-dev mpich2 mpich2-doc

# Add and install Python modules
ADD requirements.txt /src/requirements.txt
# RUN cd /src; pip install -r requirements.txt
RUN cd /src; sudo pip install -r requirements.txt

# Bundle app source
COPY api.py /src/api.py
COPY work_stealing.py /src/work_stealing.py
COPY work_pushing.py /src/work_pushing.py
COPY utils.py /src/utils.py

EXPOSE  8000
CMD ["python", "/src/api.py", "-port_num=8000"]

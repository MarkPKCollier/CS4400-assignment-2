FROM nlknguyen/alpine-mpich

RUN sudo apk add --no-cache valgrind gdb

# Install Python Setuptools
RUN sudo apk add --no-cache py-setuptools

# Install pip
RUN sudo apk add --no-cache py-pip python-dev

# Add and install Python modules
ADD requirements.txt /src/requirements.txt
RUN cd /src; sudo pip install -r requirements.txt

# Bundle app source
COPY api.py /src/api.py
COPY work_stealing.py /src/work_stealing.py
COPY work_pushing.py /src/work_pushing.py
COPY utils.py /src/utils.py

EXPOSE  8080
CMD ["python", "/src/api.py", "--port_num=8080"]

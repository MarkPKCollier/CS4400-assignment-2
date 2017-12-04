FROM alpine:3.1

# Update
RUN apk add --update python py-pip

# Install app dependencies
RUN pip install -r requirements.txt

# Bundle app source
COPY api.py /src/api.py
COPY work_stealing.py /src/work_stealing.py
COPY work_pushing.py /src/work_pushing.py
COPY utils.py /src/utils.py

EXPOSE  8000
CMD ["python", "/src/api.py", "-p 8000"]

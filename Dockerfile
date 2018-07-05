FROM continuumio/anaconda3:5.2.0
RUN apt-get update && \
    apt-get -y install g++ mono-mcs && \
    rm -rf /var/lib/apt/lists/*
RUN pip install bs4
RUN pip install -U spacy
ADD ./Classify.py /
CMD [ "python", "./Classify.py" ]
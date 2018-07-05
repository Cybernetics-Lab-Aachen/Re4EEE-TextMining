FROM continuumio/anaconda3:5.2.0
RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    apt-get -y install g++-4.8 && \
    rm -rf /var/lib/apt/lists/*
RUN pip install bs4
RUN pip install -U spacy
ADD ./Classify.py /
CMD [ "python", "./Classify.py" ]
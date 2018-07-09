FROM continuumio/anaconda3:5.2.0
RUN apt-get update && \
    apt-get -y install g++ mono-mcs && \
    apt-get install -y python-qt4 && \
    apt install -y libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*
RUN pip install bs4
RUN pip install -U spacy
RUN spacy download en
ADD ./Classify.py /
CMD [ "python", "./Classify.py" ]
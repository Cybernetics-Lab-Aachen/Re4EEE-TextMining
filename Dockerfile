FROM continuumio/anaconda3:5.2.0
RUN pip install bs4
ADD ./Classify.py /
ADD ./tweets.json /
CMD [ "python", "./Classify.py" ]
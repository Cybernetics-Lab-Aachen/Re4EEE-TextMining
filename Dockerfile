FROM continuumio/anaconda3:5.2.0
RUN pip install bs4
ADD ./Classify.py /
CMD [ "python", "./Classify.py" ]
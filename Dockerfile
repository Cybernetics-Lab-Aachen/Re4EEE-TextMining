FROM continuumio/anaconda3:5.2.0
RUN pip install bs4
ADD ./wikipedia_files/DownloadArticlesMultiThread.py /
ADD ./sample_set/ /sample_set/
CMD [ "python", "./DownloadArticlesMultiThread.py" ]
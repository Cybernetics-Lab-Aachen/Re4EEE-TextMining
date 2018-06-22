FROM continuumio/anaconda3:5.2.0
RUN pip install bs4
ADD ./wikipedia_files/DownloadArticlesMultiThread.py /
CMD [ "python", "./DownloadArticlesMultiThread.py" ]
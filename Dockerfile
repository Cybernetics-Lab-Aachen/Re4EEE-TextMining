FROM continuumio/anaconda3:5.2.0
RUN pip install bs4
RUN pip install lxml
RUN pip install requests
ADD ./wikipedia_files/DownloadArticlesMultiThread.py /
ADD ./index.txt /
ADD ./sample_set/ /sample_set/
CMD [ "python", "./DownloadArticlesMultiThread.py" ]
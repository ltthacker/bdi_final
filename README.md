# Implementation of Fake new detection system

## Big data integration course

## Contribution

* Multiprocess crawler, retrieve multiple news.
* The crawler contain the url retriever module, which retrieve all news source started from baomoi.com/covid-19. (done)
* After that, multiple html source retriever module run in different process retrieve the html source in parallel. (done the singlethreaded, can be scaled to run faster)
* Html source retriever module cut the html into url and sentences. (done)
* The retriever module then send the {url, sentence} json to SparkStreaming. (done)
* SparkStreaming process batch of data
    * Map {url, sentence} to {url, sentence, flag} where flag=0 is no information, flag=1 is truth, flag=2 mean fake sentence (done)
    * Filter url with sentence that in our domain
    * Reduce count the number of no information, truth, fake sentences {url, sentences}
    * Update the statistic to database per each batch


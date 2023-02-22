# RuSentRel Leaderboard 


**Dataset description**: RuSentRel collection consisted of analytical articles from Internet-portal `inosmi.ru`. 
These are translated into Russian texts in the domain of international politics obtained from foreign authoritative sources.
The collected articles contain both the author's opinion on the subject matter 
of the article and a large number of references mentioned between the participants of the described situations. 
In total, 73 large analytical texts were labeled with about 2000 relations.

This repository is an official results benchmark for automatic
*sentiment attitude extraction* task within *RuSentRel* collection.
Let's follow the [task](#task) section for greater details.

**Contributing**: Please feel free to make pull requests, and at 
[awesome-sentiment-attitude-extraction](https://github.com/nicolay-r/awesome-sentiment-attitude-extraction) 
especially!

> For more details about RuSentRel please proceed with the related [repository](https://github.com/nicolay-r/RuSentRel).

## Contents
* [Task](#task)
* [Approaches](#approaches)
* [Submission Evaluation](#submission-evaluation)
* [Leaderboard](#leaderboard)
    * [Neural Networks Optimization](#neural-networks-optimization)
    * [Evaluator](#evaluator)
* [Related works](#related-works)
* [References](#references)

## Task 

Given a subset of documents in the RuSentRel collection, where each document is
presented by a pair: (1) text, (2) a list of selected named entities.
For each document, it is required to complete a list of such entity pairs (e<sub>s</sub>, e<sub>o</sub>), 
for which text conveys the presence of sentiment relation from the *e<sub>s</sub>* (subject) towards an *e<sub>o</sub>* (object).
Label assignation can be *neg* or *pos*. 

| Example                                                                                                                                                                                                                                                     |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ... При этом <ins>Москва</ins> неоднократно подчеркивала, что ее активность на <ins>балтике</ins> является ответом именно на действия **<ins>НАТО</ins>** и эскалацию враждебного подхода к **<ins>Росcии</ins>** вблизи ее восточных границ ... *(... Meanwhile <ins>Moscow</ins> has repeatedly emphasized that its activity in the <ins>Baltic Sea</ins> is a response precisely to actions of **<ins>NATO</ins>** and the escalation of the hostile approach to **<ins>Russia</ins>** near its eastern borders ...)*
| (NATO->Russia, neg), (Russia->NATO, neg)                                                                                                                                                                                                                    |

Task paper: https://arxiv.org/pdf/1808.08932.pdf

## Approaches

The task is considered as a context classification problem, in which *context* is a text region with mentioned pair (attitude participants) in it.
Then classified context-level attitudes transfers onto document-level by averaging context labels of the related pair (using the voting method).

We implement [AREkit](https://github.com/nicolay-r/AREkit) toolkit which becomes a framework for the following applications:
* BERT-based language models [[code]](https://github.com/nicolay-r/bert-for-attitude-extraction-with-ds);
* Neural Networks with (and w/o) Attention mechanism [[code]](https://github.com/nicolay-r/neural-networks-for-attitude-extraction);
* Conventional Machine Learning methods [[code]](https://github.com/nicolay-r/sentiment-relation-classifiers);

[Back to Top](#contents)

## Submission Evaluation

Please use `evaluate.py` script. 
For example, for the ChatGPT submission results:
```python
python3 evaluate.py --input data/chatgpt-avg.zip --mode classification --split cv3
```

[Back to Top](#contents)
 
## Leaderboard 

Results ordered from the latest to the oldest. We measure `F1` (scaled by 100) across the following foldings (see [evaluator](#evaluator) section for greater details):
* F1<sub>cv</sub> - the average `F1` of a 3-fold CV check; 
foldings carried out by preserving the same number of sentences in each of them;
* F<sub>t</sub> -- `F1` over the predefined TEST set;

The result assessment organized in experiments:
* `3l` -- subject-object pairs extraction.
* `2l` -- classification of already given subject-object pairs on document level;

|Methods       |F1<sub>cv</sub> (3l)  |F1<sub>t</sub> (3l)                    |F1<sub>cv</sub> (2l)   |F1<sub>t</sub> (2l)    |
|--------------|------------|-----------------------------|-------------|-------------|
|              |            |                             |             |             |
|Expert Agreement<sup>[\**](#footnote2)</sup> [[1]](#link1)                      | 55.0       |55.0                         |-            |-            |
|                        |            |                             |             |             |
|ChatGPT zero-shot with promptings<sup>[\***](#footnote2)</sup> [[7]](#link7)  |            |                             |             |             |
|                        |            |                             |             |             |
|ChatGPT<sub>avg</sub> [50 words distance]  |            |                              |66.19       |**74.47**         |
|ChatGPT<sub>first</sub> [50 words distance]  |            |                              |69.23       |74.09         |
|                        |            |                             |             |             |
|*Distant Supervision*<sub>RA-2.0-large</sub> for Language Models (BERT-based) [[6]](#link6)  |            |                             |             |             |
|[<sub>pt</sub> -- pretrained, <sub>ft</sub> -- fine-tunded]  |            |                             |             |             |
|SentenceRuBERT (NLI<sub>pt</sub> + NLI<sub>ft</sub>) |**39.0**    |38.0                     |70.2         |67.7         |
|SentenceRuBERT (NLI<sub>pt</sub> + QA<sub>ft</sub>)  |38.4       |**41.9**                     |69.6         |64.2         |
|SentenceRuBERT (NLI<sub>pt</sub> + C<sub>ft</sub>)  |37.9        |39.8                         |70.0         |**69.8**         |
|RuBERT (NLI<sub>pt</sub> + NLI<sub>ft</sub>)|36.8        |39.9                         |**71.0**         |68.6         |
|RuBERT (NLI<sub>pt</sub> + QA<sub>ft</sub>) |34.8        |37.0                         |69.6         |68.2         |
|RuBERT (NLI<sub>pt</sub> + C<sub>ft</sub>)  |35.6        |35.4                         |70.0         |69.8         |
|mBase (NLI<sub>pt</sub> + NLI<sub>ft</sub>) |33.6        |36.0                         |69.4         |68.2         |
|mBase (NLI<sub>pt</sub> + QA<sub>ft</sub>) |30.1        |35.5                         |69.6         |65.2         |
|mBase (NLI<sub>pt</sub> + C<sub>ft</sub>)  |30.5        |31.1                         |68.9         |67.7         |
|                        |            |                             |             |             |
|*Distant Supervision*<sub>RA-2.0-large</sub> for *(Attentive) Neural Networks* + Frames annotation [Joined Training] [[6]](#link6)<sub>reproduced</sub>, [[4]](#link4)<sub>original</sub>     |            |                             |             |             |
|PCNN<sub>ends</sub>      |**32.2**        |**39.9**                         |70.2         |67.8         |
|BiLSTM        |32.0        |38.8                         |**71.2**     |68.4         |
|PCNN          |31.6        |39.7                         |69.5         |70.5         |
|LSTM          |31.6        |39.5                         |68.0         |**75.4**         |
|Att-BiLSTM [[P.Zhou et. al]](https://aclanthology.org/P16-2034.pdf)   |31.0        |37.3                         |66.2         |71.2         |
|AttCNN<sub>ends</sub>    |30.9        |**39.9**                         |66.8         |72.7         |
|IAN<sub>ends</sub>       |30.7        |36.7                         |69.1         |72.6         |
|                        |            |                             |             |             |
|*Distant Supervision*<sub>RA-1.0</sub> for Multi-Instance *Neural Networks* [Joined Training] [[5]](#link5)     |            |                             |             |             |
|                        |            |                             |             |             |
|MI-PCNN                                    |            |                             |             |**68.0**         |
|MI-CNN                                    |            |                             |             |62.0         |
|PCNN                                       |            |                             |            |67.0         |
|CNN                                       |            |                             |             |63.0         |
|*Language Models (BERT-based)* [[6]](#link6)|            |                             |             |             |
|SentenceRuBERT (NLI)                                    |33.4        |32.7                         |69.8         |67.6         |
|SentenceRuBERT (QA)                                     |34.3        |**38.9**                         |**70.2**      |67.1         |
|SentenceRuBERT (C)                                     |34.0        |35.2                         |69.3         |65.5         |
|RuBERT (NLI)                                   |29.4        |39.6                         |68.9         |66.4         |
|RuBERT (QA)                                       |32.0        |35.3                         |69.5         |66.2         |
|RuBERT (C)                                     |**36.8**        |37.6                         |67.8         |66.2         |
|mBase (NLI)                                    |29.2        |37.0                         |67.8         |58.4         |
|mBase (QA)    |28.6        |33.8                         |66.5         |65.4         |
|mBase (C)     |26.9        |30.0                         |67.0         |**68.9**     |
|                        |            |                             |             |             |
|*(Attentive) Neural Networks* + Frames annotation ([[6]](#link6)<sub>reproduced</sub>, [[3]](#referces)<sub>original</sub>)       |            |                             |             |             |
|IAN<sub>ends</sub>       |**30.8**        |32.2                         |60.8         |63.5         |
|AttPCNN<sub>ends</sub>      |29.9        |**32.6**                         |64.3         |63.3         |
|PCNN          |29.6        |32.5                         |64.4         |63.3         |
|CNN                                               |28.7        |31.4                         |63.6         |65.9         |
|BILSTM        |28.6        |32.4                         |62.3         |**71.2**         |
|LSTM          |27.9        |31.6                         |61.9         |65.3         |
|AttCNN<sub>ends</sub>       |27.6        |29.7                         |65.0         |66.2         |
|Att-BiLSTM [[P.Zhou et. al]](https://aclanthology.org/P16-2034.pdf)   |27.5        |32.3                         |**65.7**         |68.2         |
|                        |            |                             |             |             |
|*Convolutional networks* [[2]](#link2)           |            |                             |             |             |
|PCNN [[code]](https://github.com/nicolay-r/sentiment-pcnn)                                   |            | **0.31**                    |             |             |
|CNN                                               |            | **0.30**                    |             |             |
|                        |            |                             |             |             |
|*Conventional methods* [[1]](#link1) [[code]](https://github.com/nicolay-r/sentiment-relation-classifiers)             |            |                             |             |             |
|Gradient Boosting (Grid search)                        |**20.3**<sup>[\*](#footnote)    |**28.0**                     |             |             |
|Random Forest (Grid search)                        |19.1<sup>[\*](#footnote)</sup>        |27.0                     |             |             |
|Random Forest                                      |15.7<sup>[\*](#footnote)</sup>        |27.0                     |             |             |
|Naive Bayes (Bernoulli)                            |15.2<sup>[\*](#footnote)</sup>        |16.0                          |             |             |
|SVM                                               |15.1<sup>[\*](#footnote)</sup>        |15.0                          |             |             |
|Gradient Boosting                                 |14.4<sup>[\*](#footnote)</sup>        |27.0                     |             |             |
|SVM (Grid search)                                 |14.3<sup>[\*](#footnote)</sup>        |15.0                          |             |             |
|NaiveBayes (Gauss)                                |9.2<sup>[\*](#footnote)</sup>         |11.0                          |             |             |
|KNN                                               |7.0<sup>[\*](#footnote)</sup>         |9.0                          |             |             |
|                                                  |            |                             |             |             |
|Baseline (School) [[link]](https://miem.hse.ru/clschool/)|            |**12.0**                         |             |             |
|Baseline (Distr)                                  |            |8.0                          |             |             |
|Baseline (Random)                                 |7.4<sup>[\*](#footnote)</sup>         |8.0                          |             |             |
|Baseline (Pos)                                    |3.9<sup>[\*](#footnote)</sup>         |4.0                          |             |             |
|Baseline (Neg)                                    |5.2<sup>[\*](#footnote)</sup>         |5.0                          |             |             |

<a name="footnote">*</a>: Results that were not mentioned in papers.

<a name="footnote2">**</a>: We asked another super-annotator to label the collection, and compared her annotation with our gold standard using average F-measure of positive and negative classes in the same way as for
automatic approaches. In such a way, we can reveal the upper border for automatic
algorithms. We obtained that F-measure of human labeling. [[1]](#link1)

<a name="footnote3">***</a>: We consider translation into english samples via the [arekit-sampler](arekit-sources-sampler) by translating texts into 
english first, and then wrapping them into prompts. We consider a `k`-words distance (`50` by default, in english) between words as a upper bound for pairs organization;
because of the latter and prior standards, results might be lower (translation increases distance in words). 

[Back to Top](#contents)

### Neural Networks Optimization

The training process is described in [Rusnachenko et. al., 2020](https://arxiv.org/abs/2006.13730) (section 7.1) and 
relies on the *Multi-Instance learning* approach, originally proposed in  [Zeng et. al., 2015](https://www.aclweb.org/anthology/D15-1203.pdf) paper. 
(SGD application, bags terminology, instances selection within bags).
All the batch context samples are gathered into *bags*.
Authors propose to select the best instance in every bag as follows: 
calculate the `max` value of p(y<sub>i</sub>|m<sub>i</sub>,j) across i'th values within a particular j'th bag. 
The latter allows them to adopt `loss` function on bags level.

In our works, we adopt bags for synonymous context gathering.
Therefore, for gradients calculation within bags, we choose `avg` function instead. 
The assumption here is to consider other synonymous attitudes during the gradients calculation procedure.
We use `BagSize > 1` in earlier work [Rusnachenko, 2018](https://github.com/nicolay-r/sentiment-pcnn/tree/clls-2018)
In the latest experiments, we consider `BagSize = 1` and therefore don't exploit bag values averaging.

[Back to Top](#contents)

### Evaluator

![](https://img.shields.io/badge/Python-3.6-brightgreen.svg)

Source code exported from AREkit-0.21.1 library and yields of: 
* [Evaluation](evaluation) directory for details of the evaluator implementation and the related dependencies;
* [Test](test) directory, which includes test scripts that allow applying evaluator for the archived [results](test/data).

[Back to Top](#contents)

## Related works
[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[Awesome Sentiment Attitude Extraction](https://github.com/nicolay-r/awesome-sentiment-attitude-extraction)

[Back to Top](#contents)

## References

<a name="link1">[1]</a>
**Natalia Loukachevitch, Nicolay Rusnachenko**
*Extracting Sentiment Attitudes from Analytical Texts*
Proceedings of International Conference on Computational Linguistics and Intellectual Technologies Dialogue-2018 (arXiv:1808.08932)
[[paper]](https://arxiv.org/pdf/1808.08932.pdf)
[[code]](https://github.com/nicolay-r/sentiment-relation-classifiers)

<a name="link2">[2]</a>
**Nicolay Rusnachenko, Natalia Loukachevitch**
*Using Convolutional Neural Networks for Sentiment Attitude Extraction from Analytical Texts,*
EPiC Series in Language and Linguistics 4, 1-10, 2019 
[[paper]](https://wwww.easychair.org/publications/download/pQrC)
[[code]](https://github.com/nicolay-r/sentiment-pcnn)

<a name="link3">[3]</a>
**Nicolay Rusnachenko, Natalia Loukachevitch**
*Studying Attention Models in Sentiment Attitude Extraction Task*
Métais E., Meziane F., Horacek H., Cimiano P. (eds) Natural Language Processing and Information Systems. NLDB 2020. Lecture Notes in Computer Science, vol 12089. Springer, Cham
[[paper]](https://arxiv.org/abs/2006.11605)
[[code]](https://github.com/nicolay-r/attitude-extraction-with-attention)

<a name="link4">[4]</a>
**Nicolay Rusnachenko, Natalia Loukachevitch**
*Attention-Based Neural Networks for Sentiment Attitude Extraction using Distant Supervision*
The 10th International Conference on Web Intelligence, Mining and Semantics (WIMS 2020), June 30-July 3 (arXiv:2006.13730)
[[paper]](https://dl.acm.org/doi/10.1145/3405962.3405985)
[[code]](https://github.com/nicolay-r/attitude-extraction-with-attention-and-ds)

<a name="link5">[5]</a>
**Nicolay Rusnachenko, Natalia Loukachevitch, Elena Tutubalina**
*Distant Supervision for Sentiment Attitude Extraction*
Proceedings of the International Conference on Recent Advances in Natural Language Processing (RANLP 2019)
[[paper]](https://aclanthology.org/R19-1118.pdf) 
[[code]](https://github.com/nicolay-r/attitudes-extraction-ds)

<a name="link6">[6]</a>
**Nicolay Rusnachenko**
*Language Models Application in Sentiment Attitude Extraction Task*
Proceedings of the Institute for System Programming of the RAS (Proceedings of ISP RAS). 2021;33(3):199-222. (In Russ.)
[[paper]](https://nicolay-r.github.io/website/data/rusnachenko2021language.pdf)
[[code-networks]](https://github.com/nicolay-r/neural-networks-for-attitude-extraction)
[[code-bert]](https://github.com/nicolay-r/bert-for-attitude-extraction-with-ds)

<a name="link7">[7]</a>
**Bowen Zhang, Daijun Ding, Liwen Jing**
*How would Stance Detection Techniques Evolve after the Launch of ChatGPT?*
[[paper]](https://arxiv.org/pdf/2212.14548.pdf)


[Back to Top](#contents)

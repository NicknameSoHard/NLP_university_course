# NLP_university_course
This is NLP repository for university NLP course.

### NewsParser
NewsParser собирает новости с meduza.io, vesti.ru and lenta.ru.

**Using NewsParser directory as source root!**  
Запускается по команде:  
<code>python3 assignment1/app.py -n 5 -f news.csv </code>

Arguments:  
<code>-n</code> - Количество новостей, которые в равной степени будет распределены между тремя источниками.   
<code>-f</code> - Файл, в которой сохранить все новости (csv формат).

### Semester 1 IR-NLP
Проекты:
1. Content-based ranking - использование VSM и BM25 для ранжирования текстов.
2. Deep text models - нейросетевые модели текста, реализация FastText и сравнение  документов, получаемых с помощью Word2Vec и FastText
3. Link-based ranking - ранжирование страниц из википедии по запросу через собственную реализацию PageRank и HITS.
4. Morphology - Реализация морфологического анализатора - оригинал задания: https://stepik.org/lesson/37845/step/1?unit=18887
5. Near-duplicate detection - реализация поиска дупликатов новосткей через метод шинглов, миншинглов. 
6. Query processing - реализация корректора опечаток на основе триграмм с выдачей N-рекомендаций исправления.
7. Vector space models - эксперименты со взвешиваем признаков через TF-IDF, PMI и LSA, добавление лемминга и стемминга и обучение на этом простой нейронной сети для работы с текстом. 

### Semester 1 BERT
Проекты:
1. Fine Tuning Sentence Classification - Использование pytorch-transformers и обучение BERT для определения эмоциональной окраски твиттов.
2. News tag Classification - обучение BERT определению тегов новостей на основе парсера из предыдущего семестра.
3. IMDB Dataset - эксперименты с подсчетом точности при обучении на различном размере тренировочной выборки.

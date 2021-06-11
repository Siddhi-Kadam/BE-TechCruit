import pyautogui
from django.http import HttpResponse
from django.shortcuts import render
from candidate.models import Selection2, PersonalInfo, Coding
import csv
import random
import time

import matplotlib.pyplot as plt
import PyPDF2
import os
from io import StringIO
import pandas as pd
from collections import Counter
import en_core_web_sm
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nlp = en_core_web_sm.load()
from spacy.matcher import PhraseMatcher

# Create your views here.
from check.models import Upload


def check(request):
    fin = {}
    r = 1
    p = PersonalInfo.objects.all()
    c = Coding.objects.all()
    s = Selection2.objects.all()
    for i in p:
        for j in c:
            if i.id == j.uid_id:
                for k in s:
                    if i.id == k.uid_id:
                        if k.status == 'Selected':
                            fin[r] = {'id': r, 'username': i.username, 'fullname': i.name, 'language': j.language,
                                      'company': k.compName, 'salary': k.salary, 'status': 1}
                        else:
                            fin[r] = {'id': r, 'username': i.username, 'fullname': i.name, 'language': j.language,
                                      'company': k.compName, 'salary': k.salary, 'status': 0}
                        r += 1
    return render(request, 'eligibilityAnalysis/tables.html', {'s': fin})


def writeCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="csv_simple_write.csv"'
    writer = csv.writer(response)
    # writer.writerow(['uid', 'fullname', 'username', 'ssc', 'hsc', 'grad', 'course', 'scores', 'compName', 'salary',
    #                  'jobTitle', 'status'])
    # s = Selection2.objects.all()
    # for i in s:
    #     writer.writerow([i.uid, i.fullname, i.username, i.ssc, i.hsc, i.grad, i.course, i.scores, i.compName, i.salary,
    #                      i.jobTitle, i.status])
    writer.writerow(['id', 'username', 'fullname', 'language', 'company', 'salary', 'status'])
    p = PersonalInfo.objects.all()
    c = Coding.objects.all()
    s = Selection2.objects.all()
    r = 1
    for i in p:
        for j in c:
            if i.id == j.uid_id:
                for k in s:
                    if i.id == k.uid_id:
                        if k.status == 'Selected':
                            writer.writerow([r, i.username, i.name, j.language, k.compName, k.salary, 1])
                        else:
                            writer.writerow([r, i.username, i.name, j.language, k.compName, k.salary, 0])
                        r += 1
    return response


def resumeUpload(request):
    return render(request, 'eligibilityAnalysis/resumeUpload.html')


def resumeUploaded(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if request.FILES['myfile']:
            m = request.FILES['myfile']
            o = Upload(name=name, resume=m)
            o.save()
            c = Upload.objects.get(name=name)
            pyautogui.alert("Upload Done")
            print(m)
            return render(request, 'eligibilityAnalysis/evaluate.html', {'c': c})


def pdfextract(file):
    fileReader = PyPDF2.PdfFileReader(open(file, 'rb'))
    countpage = fileReader.getNumPages()
    count = 0
    text = []
    while count < countpage:
        pageObj = fileReader.getPage(count)
        count += 1
        t = pageObj.extractText()
        # print(t)
        text.append(t)
    return text


# function to read resume ends


# function that does phrase matching and builds a candidate profile
def create_profile(file, savage):
    text = pdfextract(file)
    text = str(text)
    text = text.replace("\\n", "")
    text = text.lower()
    savage = savage + text
    # below is the csv where we have all the keywords, you can customize your own
    keyword_dict = pd.read_csv('D:/BE-TechCruit/BE-TechCruit/techcruit/extra/template_new.csv')
    stats_words = [nlp(text) for text in keyword_dict['Statistics'].dropna(axis=0)]
    NLP_words = [nlp(text) for text in keyword_dict['NLP'].dropna(axis=0)]
    ML_words = [nlp(text) for text in keyword_dict['Machine Learning'].dropna(axis=0)]
    DL_words = [nlp(text) for text in keyword_dict['Deep Learning'].dropna(axis=0)]
    R_words = [nlp(text) for text in keyword_dict['R Language'].dropna(axis=0)]
    python_words = [nlp(text) for text in keyword_dict['Python Language'].dropna(axis=0)]
    Data_Engineering_words = [nlp(text) for text in keyword_dict['Data Engineering'].dropna(axis=0)]
    Web_Development_words = [nlp(text) for text in keyword_dict['Web Development'].dropna(axis=0)]

    matcher = PhraseMatcher(nlp.vocab)
    matcher.add('Statistics', None, *stats_words)
    matcher.add('NLP', None, *NLP_words)
    matcher.add('MachineLearning', None, *ML_words)
    matcher.add('DeepLearning', None, *DL_words)
    matcher.add('R', None, *R_words)
    matcher.add('Python', None, *python_words)
    matcher.add('DataEngineering', None, *Data_Engineering_words)
    matcher.add('WebDevelopment', None, *Web_Development_words)

    doc = nlp(text)

    d = []
    matches = matcher(doc)
    subjects = []
    keywords = []
    for match_id, start, end in matches:
        rule_id = nlp.vocab.strings[match_id]  # get the unicode ID, i.e. 'COLOR'
        span = doc[start: end]  # get the matched slice of the doc
        print(span)
        keywords.append(span)
        subjects.append(rule_id)

        d.append((rule_id, span.text))

    keywords = "\n".join(f'{i[0]} {i[1]} ({j})' for i, j in Counter(d).items())

    ## converting string of keywords to dataframe
    df = pd.read_csv(StringIO(keywords), names=['Keywords_List'])
    df1 = pd.DataFrame(df.Keywords_List.str.split(' ', 1).tolist(), columns=['Subject', 'Keyword'])
    df2 = pd.DataFrame(df1.Keyword.str.split('(', 1).tolist(), columns=['Keyword', 'Count'])
    df3 = pd.concat([df1['Subject'], df2['Keyword'], df2['Count']], axis=1)
    df3['Count'] = df3['Count'].apply(lambda x: x.rstrip(")"))

    base = os.path.basename(file)
    filename = os.path.splitext(base)[0]

    name = filename.split('_')
    name2 = name[0]
    name2 = name2.lower()
    ## converting str to dataframe
    name3 = pd.read_csv(StringIO(name2), names=['Candidate Name'])

    dataf = pd.concat([name3['Candidate Name'], df3['Subject'], df3['Keyword'], df3['Count']], axis=1)
    dataf['Candidate Name'].fillna(dataf['Candidate Name'].iloc[0], inplace=True)

    return dataf, subjects, keywords, savage


def analyse(resume):
    final_database = pd.DataFrame()
    file = 'D:/BE-TechCruit/BE-TechCruit/techcruit/media/' + str(resume)
    savage = ''
    dat, subjects, keywords, savage = create_profile(file, savage)
    final_database = final_database.append(dat)

    print(final_database)
    print(type(final_database))
    return final_database, subjects, keywords


def evaluate(request):
    if request.method == 'POST':
        ids = request.POST.get('ids')
        u = Upload.objects.get(id=ids)
        final_database, subjects, keywords = analyse(u.resume)
        subjects = set(subjects)
        subjects = list(subjects)
        print(keywords)
        print(type(keywords))
        key = keywords.split('\n')
        final_database2 = final_database['Keyword'].groupby(
            [final_database['Candidate Name'], final_database['Subject']]).count().unstack()
        final_database2.reset_index(inplace=True)
        final_database2.fillna(0, inplace=True)
        new_data = final_database2.iloc[:, 1:]
        new_data.index = final_database2['Candidate Name']
        # execute the below line if you want to see the candidate profile in a csv format
        sample2 = new_data.to_csv('D:/BE-TechCruit/BE-TechCruit/techcruit/extra/sample.csv')

        plt.rcParams.update({'font.size': 10})
        ax = new_data.plot.barh(title="Resume keywords by category", legend=False, figsize=(25, 7), stacked=True)
        labels = []
        for j in new_data.columns:
            for i in new_data.index:
                label = str(j) + ": " + str(new_data.loc[i][j])
                labels.append(label)
        patches = ax.patches
        for label, rect in zip(labels, patches):
            width = rect.get_width()
            if width > 0:
                x = rect.get_x()
                y = rect.get_y()
                height = rect.get_height()
                ax.text(x + width / 2., y + height / 2., label, ha='center', va='center')
        plt.plot()
        link = 'media/' + str(u.name) + '.png'

        plt.savefig(link)
        link = './' + link
        print(link)
        return render(request, 'eligibilityAnalysis/eval.html',
                      {'id': ids, 'u': u, 'datas': final_database, 'subjects': subjects,
                       'keywords': key, 'score': len(key), 'link': link})


def resumeAnalysis(request):
    mypath = 'D:/BE-TechCruit/BE-TechCruit/techcruit/media/resumes'  # enter your path here where you saved the resumes
    onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    final_database = pd.DataFrame()
    i = 0
    savage = ''
    while i < len(onlyfiles):
        file = onlyfiles[i]
        dat, subjects, keywords, savage = create_profile(file, savage)
        final_database = final_database.append(dat)
        i += 1
    print(final_database)
    print(type(final_database))
    final_database2 = final_database['Keyword'].groupby(
        [final_database['Candidate Name'], final_database['Subject']]).count().unstack()
    final_database2.reset_index(inplace=True)
    final_database2.fillna(0, inplace=True)
    new_data = final_database2.iloc[:, 1:]
    new_data.index = final_database2['Candidate Name']
    # execute the below line if you want to see the candidate profile in a csv format
    sample2 = new_data.to_csv('D:/BE-TechCruit/BE-TechCruit/techcruit/extra/sample.csv')
    import matplotlib.pyplot as plt

    plt.rcParams.update({'font.size': 10})
    ax = new_data.plot.barh(title="Resume keywords by category", legend=False, figsize=(50, 7), stacked=True)
    labels = []
    for j in new_data.columns:
        for i in new_data.index:
            label = str(j) + ": " + str(new_data.loc[i][j])
            labels.append(label)
    patches = ax.patches
    for label, rect in zip(labels, patches):
        width = rect.get_width()
        if width > 0:
            x = rect.get_x()
            y = rect.get_y()
            height = rect.get_height()
            ax.text(x + width / 2., y + height / 2., label, ha='center', va='center')
    plt.plot()
    link = 'media/' + str(random.randint(0, 1000000000000000000000000000)) + '.png'
    plt.savefig(link)
    link = './' + link
    print(link)
    d = {}
    with open("D:/BE-TechCruit/BE-TechCruit/techcruit/extra/sample.csv", 'r') as f:
        rowReader = csv.reader(f, delimiter=',')
        # next(rowReader)  -use this if your txt file has a header strings as column names
        d = {}
        i = 0
        for values in rowReader:
            # print(values[0],', Points:',values[1],', Diff:',values[2],',Goals:',values[3])
            if i == 0:
                d[i] = {'name': values[0], 'DE': values[1], 'DL': values[2], 'ML': values[3], 'NLP': values[4],
                        'Python': values[5], 'WDL': values[6], 'scores': 'Scores'}
            else:
                score = float(values[1]) + float(values[2]) + float(values[3]) + float(values[4]) + float(
                    values[5]) + float(values[6])
                d[i] = {'name': values[0], 'DE': values[1], 'DL': values[2], 'ML': values[3], 'NLP': values[4],
                        'Python': values[5], 'WDL': values[6], 'scores': score}
            i += 1
            print(values[0], values[1], values[2], values[3], values[4], values[5], values[6])
    return render(request, 'eligibilityAnalysis/resumeAnalysis.html',
                  {'datas': d, 'link': link})


def resumeScreening(request):
    mypath = 'D:/BE-TechCruit/BE-TechCruit/techcruit/media/resumes'  # enter your path here where you saved the resumes
    onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    savage = ''
    final_database = pd.DataFrame()
    i = 0
    while i < len(onlyfiles):
        file = onlyfiles[i]
        savage = create_profile2(file, savage)
        i += 1
    print(savage)
    words = word_tokenize(savage)
    print('Word Tokenize: \n', words)
    NLTK_stop_words_list = stopwords.words('english')
    sentence_without_stopword = [k for k in words if not k in NLTK_stop_words_list]
    print("After removing Stopwords:\n", sentence_without_stopword)
    # Remove Punctuation marks
    punctuation = '''!()-[]{};:'"\|,<>./?@#$%^&*_~'''
    final = [k for k in sentence_without_stopword if k not in punctuation]
    print("After removing Stopwords & punctuations:\n", final)
    remove = ['date', 'birth', 'may', 'known', 'hindi', 'english', 'front', 'end', 'smart', 'farming', 'thingspeak',
              'painting', 'breast', 'cancer',
              'campus', 'address', 'vit', 'chennai', 'awarded', 'class', 'user', 'info', 'developed', 'also', 'used',
              'free',
              'email', 'usage', 'guidelines', 'description', 'deliverables', 'developerphone', 'mapreduce', 'hive',
              'pig',
              'sqoop', 'new', 'oak', 'street', 'old', 'forge', 'york', 'spanish', 'club', 'technovit', 'key', 'good',
              'females', 'women', 'health', 'safety', 'emergency', 'mode', 'using', 'modules', 'safest', 'route',
              'disease',
              'face', 'detection', 'openmp', 'made', 'based', 'tools', 'activities', 'reading', 'novels', 'bachelor',
              'cgpa', 'college', 'agra', 'xii', 'oriented', 'monitoring', 'created', 'years', 'view', 'create',
              'january',
              'designed', 'client', 'environment', 'corporation', 'hdfs', 'hbase', 'custom', 'reports', 'bhilai',
              'secondary', 'school', 'linear', 'experience', 'coordinator', 'computer', 'architecture', 'knowledge',
              'templates',
              'scripts', 'high', 'control', 'developerabc', 'documents', 'maintaining', 'l', 'management',
              'entertainer',
              'friends', 'permanent', 'tamil', 'nadu', 'objective', 'company', 'vellore', 'institute', 'till',
              'semester',
              'patricks', 'junior', 'hsc', 'icse', 'percentage', 'ssc', 'object', 'engineer', 'beginner', 'two',
              'provides',
              'views', 'present', 'requirements', 'like', 'files', 'make', 'campaigns', 'forms', 'saved',
              'transmitting',
              'objects', 'dummy', 'replace', 'job', 'relevant', 'current', 'role', 'case', 'dont', 'need', 'delete',
              'connector', 'package', 'retrieve', 'wrote', 'load', 'put', 'time', 'series', 'tabular', 'format', 'east',
              'timestamp', 'manipulation', 'involved', 'installation', 'well', 'svn', 'processed', 'spending',
              'maneuverable', 'within', 'specific', 'formats', 'excel', 'quality', 'collection', 'integrity',
              'internal', 'convert', 'feedback', 'meaningful', 'improved', 'university', 'smithhadoop', 'expertise',
              'ecosystem', 'experienced', 'presentkey', 'text', 'phases', 'life', 'cycle', 'run', 'mar', 'princeton',
              'microsoftresearchindia', 'chhattisgarh', 'senior', 'cbse', 'novel']
    m = []
    for i in final:
        if i.isalpha():
            m.append(i)
    d = {}
    for j in m:
        if j in d:
            d[j] += 1
        else:
            d[j] = 1
    s = {}
    li = []
    cleanedSentences = ''
    for i, j in d.items():
        if j >= 2:
            if i not in remove:
                li.append(i + ': ' + str(j))
                cleanedSentences += i + ' '
    print(li)
    from wordcloud import WordCloud
    wc = WordCloud(background_color='white', max_font_size=50).generate(cleanedSentences)
    plt.figure(figsize=(50, 7))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")

    plt.plot()
    link = 'media/' + str(random.randint(0, 1000000000000000000000000)) + '.png'
    plt.savefig(link)
    link = './' + link
    print(link)
    return render(request, 'eligibilityAnalysis/resumeScreening.html', {'datas': li, 'link': link})


def create_profile2(file, savage):
    text = pdfextract(file)
    text = str(text)

    text = text.replace("\\n", "")
    text = text.lower()
    savage = savage + text

    return savage


########################################################################################################################


def plotting():
    import seaborn as sns

    df = pd.read_csv('C:/Users/abhisiddhi/Downloads/csv_simple_write.csv')
    print(df.head())

    print(df['status'].unique())
    print(df.isnull().values.any())

    df['status'] = df['status'].map({'Rejected': 0, 'Selected': 1}).astype(int)  # mapping numbers
    print(df.head())

    sns.set_style('whitegrid')
    sns.FacetGrid(df, hue='status', height=10).map(plt.scatter, 'language', 'company').add_legend()
    # plt.show()
    plt.plot()
    link = 'media/' + str(random.randint(0, 100000000000000000000000000)) + '.png'
    plt.savefig(link)
    link = './' + link

    l = df['language'].unique()
    lang = {}
    c1 = 1
    for i in l:
        lang[i] = c1
        c1 += 1
    print(lang)
    df['language'] = df['language'].map(lang).astype(int)
    print(df.head())

    c = df['company'].unique()
    comp = {}
    c1 = 1
    for i in c:
        comp[i] = c1
        c1 += 1
    print(comp)
    df['company'] = df['company'].map(comp).astype(int)
    print(df.head())

    u = df['username'].unique()
    user = {}
    c1 = 1
    for i in u:
        user[i] = c1
        c1 += 1
    print(user)
    df['username'] = df['username'].map(user).astype(int)
    print(df.head())

    plt.close()
    sns.set_style("whitegrid")
    sns.pairplot(df, hue='status', height=2)
    # plt.show()
    plt.plot()
    link1 = 'media/' + str(random.randint(0, 1000000000000000000000000000)) + '.png'
    plt.savefig(link1)
    link1 = './' + link1
    return link, link1


def languages():
    import plotly.express as px

    data = pd.read_csv("C:/Users/abhisiddhi/Downloads/csv_simple_write.csv")
    print(data.head())
    print(type(data))

    fig1 = px.bar(data["language"].value_counts(ascending=False),
                  orientation="v",
                  color=data["language"].value_counts(ascending=False),
                  labels={'value': 'Count', 'index': 'Languages', 'color': 'Meter'})
    fig1.update_layout(title_text="Exploring coding languages used")
    fig1.show()


def mlAnalysis(request):

    link, link1 = plotting()
    languages()

    return render(request, 'eligibilityAnalysis/mlAnalysis.html', {'link': link, 'link1': link1})


def knn(request):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    plt.style.use('ggplot')

    df = pd.read_csv('C:/Users/abhisiddhi/Downloads/csv_simple_write.csv')
    print(df.head())

    # Let's observe the shape of the dataframe.
    print(df.shape)

    df.status = [1 if each == 'Selected' else 0 for each in df.status]
    # Let's create numpy arrays for features and target
    X = df.drop(['status', 'id', 'fullname'], axis=1).values
    y = df['status'].values
    print(X, y)
    xx = X
    yy = ['Selected' if each == 1 else 'Rejected' for each in y]
    print(xx, yy)

    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    X[:, 0] = le.fit_transform(X[:, 0])
    X[:, 1] = le.fit_transform(X[:, 1])
    X[:, 2] = le.fit_transform(X[:, 2])
    print('X:\n', X)

    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42, stratify=y)

    from sklearn.neighbors import KNeighborsClassifier

    # Setup arrays to store training and test accuracies
    neighbors = np.arange(1, 9)
    train_accuracy = np.empty(len(neighbors))
    test_accuracy = np.empty(len(neighbors))

    for i, k in enumerate(neighbors):
        # Setup a knn classifier with k neighbors
        knn = KNeighborsClassifier(n_neighbors=k)

        # Fit the model
        knn.fit(X_train, y_train)

        # Compute accuracy on the training set
        train_accuracy[i] = knn.score(X_train, y_train)

        # Compute accuracy on the test set
        test_accuracy[i] = knn.score(X_test, y_test)

    # Generate plot
    plt.title('k-NN Varying number of neighbors')
    plt.plot(neighbors, test_accuracy, label='Testing Accuracy')
    plt.plot(neighbors, train_accuracy, label='Training accuracy')
    plt.legend()
    plt.xlabel('Number of neighbors')
    plt.ylabel('Accuracy')
    plt.plot()
    link = 'media/' + str(random.randint(0, 10000000000000000000000000000000)) + '.png'
    plt.savefig(link)
    link = './' + link

    # Setup a knn classifier with k neighbors
    knn = KNeighborsClassifier(n_neighbors=5)
    # Fit the model
    knn.fit(X_train, y_train)
    # Get accuracy. Note: In case of classification algorithms score method represents accuracy.
    print(knn.score(X_test, y_test))
    x1 = knn.score(X_test, y_test)
    # import confusion_matrix
    from sklearn.metrics import confusion_matrix
    # let us get the predictions using the classifier we had fit above
    y_pred = knn.predict(X_test)
    print(confusion_matrix(y_test, y_pred))
    x2 = confusion_matrix(y_test, y_pred)
    pd.crosstab(y_test, y_pred, rownames=['True'], colnames=['Predicted'], margins=True)

    # import classification_report
    from sklearn.metrics import classification_report

    print(classification_report(y_test, y_pred))
    x3 = classification_report(y_test, y_pred)
    print('x3 type: ', type(x3))
    y_pred_proba = knn.predict_proba(X_test)[:, 1]
    from sklearn.metrics import roc_curve
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.plot(fpr, tpr, label='Knn')
    plt.xlabel('fpr')
    plt.ylabel('tpr')
    plt.title('Knn(n_neighbors=5) ROC curve')
    plt.plot()
    link1 = 'media/' + str(random.randint(0, 100000000000000000000000000)) + '.png'
    plt.savefig(link1)
    link1 = './' + link1

    # Area under ROC curve
    from sklearn.metrics import roc_auc_score
    print(roc_auc_score(y_test, y_pred_proba))
    x4 = roc_auc_score(y_test, y_pred_proba)
    # import GridSearchCV
    from sklearn.model_selection import GridSearchCV
    # In case of classifier like knn the parameter to be tuned is n_neighbors
    param_grid = {'n_neighbors': np.arange(1, 20)}

    knn = KNeighborsClassifier()
    knn_cv = GridSearchCV(knn, param_grid, cv=5)
    knn_cv.fit(X, y)

    print(knn_cv.best_score_)
    x5 = knn_cv.best_score_
    print(knn_cv.best_params_)
    x6 = knn_cv.best_params_

    return render(request, 'eligibilityAnalysis/knn.html', {'link': link, 'link1': link1, 'x1': x1*100, 'x2': x2,
                                                            'x3': x3, 'x4': x4*100, 'x5': x5*100, 'x6': x6})
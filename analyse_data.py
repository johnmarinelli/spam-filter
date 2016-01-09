import glob, os
import sqlite3

conn = sqlite3.connect('spam_ham.sqlite3')
c = conn.cursor()

class MessageModel:
    columns = {
        'subject': 1,
        'body': 2,
        'spam': 3,
        'table_id': 4
    }
    
    def __init__(self, ary):
        self.subject = ary[self.columns['subject']]
        self.body = ary[self.columns['body']]
        self.spam = ary[self.columns['spam']]
        self.table_id = ary[self.columns['table_id']]

select_statements = []

for i in range(1, 10):
    select_all_from_table = "SELECT * FROM part%s" % i
    select_statements.append(select_all_from_table)

statement = ' UNION '.join([s for s in select_statements])

training_msgs = c.execute(statement).fetchall()

training_content = []
training_target = []

for msg in training_msgs:
    mm = MessageModel(msg)
    training_content.append("%s %s" % (mm.subject, mm.body))
    training_target.append(mm.spam)

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
count_vect = CountVectorizer()
x_train_counts = count_vect.fit_transform(training_content)

tfidf_transformer = TfidfTransformer()
x_train_tfidf = tfidf_transformer.fit_transform(x_train_counts)
clf = MultinomialNB().fit(x_train_tfidf, training_target)

validation_msgs = c.execute('SELECT * FROM part10').fetchall()

validation_content = []
validation_target = []

for msg in validation_msgs:
    mm = MessageModel(msg)
    validation_content.append("%s %s" % (mm.subject, mm.body))
    validation_target.append(mm.spam)

x_validation_counts = count_vect.transform(validation_content)
x_validation_tfidf = tfidf_transformer.transform(x_validation_counts)

predicted = clf.predict(x_validation_tfidf)

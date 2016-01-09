import glob, os
import sqlite3

conn = sqlite3.connect('spam_ham.sqlite3')
c = conn.cursor()

# initialize tables
for i in range(1, 11):
    conn.execute("DROP TABLE IF EXISTS part%s" % i)
    conn.execute('''CREATE TABLE part%s
        (  
            id integer primary key autoincrement, 
            subject text, 
            body text, 
            spam boolean default false,
            parent_id int default %s
        );
        ''' % (i, i))

# go through each part of data
for i in range(1, 11):

    path = "/home/john/Documents/python/spam-ham/data/pu1_encoded/lemm_stop/part%s" % i

    os.chdir(path)
    print "cwd: %s" % path

    for file in glob.glob("*legit*.txt"):
        f = open(file)

        print "Processing %s..." % file
        
        subj = f.readline().split('Subject: ')[1]
        f.readline()
        body = f.readline()
        c.execute("INSERT INTO part%s (subject, body, spam) VALUES ('%s', '%s', 0)" % (i, subj, body))
        conn.commit()

    for file in glob.glob("*spmsg*.txt"):
        f = open(file)

        print "Processing %s..." % file

        subj = f.readline().split('Subject: ')[1]
        f.readline()
        body = f.readline()
        c.execute("INSERT INTO part%s (subject, body, spam) VALUES ('%s', '%s', 1)" % (i, subj, body))
        conn.commit()

conn.close()


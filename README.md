##This is the production code for www.prepubmed.org.
An article discussing how PrePubMed works is available at http://www.omnesres.com/research/prepubmed/.

PrePubMed runs on Django 1.8, and update.py needs BeautifulSoup and requests.

The GRIM test plot function needs NumPy and Matplotlib.

I am currently using sqlite3 as the database engine.  If I need to I could switch to either MySQL or PostreSQL, but query speed seems fine for now.

Despite the fact that I have a static folder I'm just relying on AWS S3 right now to serve the static files.  The main site is in the "mysite" directory.  Yes, I know the SECRET_KEY is visible, but nothing currently is getting encrypted.  A new key will be made and stored in a file when needed.  The only app is the "papers" directory, which contains the models logic along with some needed files.

The update.py file runs once a day on its own and updates the database.

Each preprint server has its own folder.  In each folder is code for the initial indexing (these might be outdated), and a text file that contains the articles that get indexed.  There are also update and error logs for update.py.

If you want to get this running locally you'll need to change the settings file, namely the host settings.  GitHub doesn't want the sqlite3 database in the repository so you will have to generate the database by making migrations and running "final_populate.py".  This could take time.  If you want it to go faster only make the database for a fraction of the articles.

###This is the current to do list:
Index Winnower (I'll do this)

Improve indexing code (I'll do this)

Saved searches and email notifications (I can do this, need to figure out best way to authenticate email addresses)


If you want to contribute to PrePubMed fork the repository and try to limit your changes to what is necessary.

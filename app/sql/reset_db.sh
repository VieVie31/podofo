cd $HOME/podofo/app/sql
rm pdf.db
rm users.db
sqlite3 pdf.db < pdf.sql
sqlite3 users.db < users.sql

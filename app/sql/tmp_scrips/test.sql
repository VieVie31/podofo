/* Select 10 random words */
SELECT * FROM FREQ ORDER BY RANDOM() LIMIT 10;;

/*
6249|7|whether|0.00050547598989
2284|5|accurately|9.19371150133e-05
3145|5|well|0.000735496920107
4214|6|vincent|0.000100321027287
1935|5|keywords|9.19371150133e-05
3574|6|ahc|0.000100321027287
5835|7|kluwer|0.00016849199663
1408|4|combines|0.000280741156654
6232|7|additional|0.00101095197978
4689|6|descriptions|0.000100321027287
*/

/*  */
SELECT PDF_ID, WORD, W_FREQ FROM FREQ ORDER BY PDF_ID LIMIT 10;;


/* Count how many pdf countain the word 'the' */
SELECT PDF_ID, WORD, COUNT(PDF_ID) FROM FREQ WHERE WORD = 'the';;

/* Count how many pdf contain each word */
SELECT WORD, COUNT(PDF_ID) FROM FREQ GROUP BY WORD;;

/* Count how many pdf countain a set of word for each word */
SELECT PDF_ID, WORD, COUNT(PDF_ID) FROM FREQ WHERE WORD IN ('the', 'yahoo') GROUP BY WORD;;

/* Count the number of pdfs in the database */
SELECT COUNT(*) FROM PDF;;

/* */
SELECT PDF_ID, WORD, W_FREQ FROM FREQ WHERE WORD in ('the', 'yahoo')


/* Select return pdfs selected by id */
SELECT ID, NAME, DATE FROM PDF WHERE ID IN (2, 3);;



/* Get for each word the frequency by pdf and almost idf (not passed in the log function) */
SELECT PDF_ID, WORD, W_FREQ, TIDF AS IDF
FROM (SELECT PDF_ID, WORD, W_FREQ 
      FROM FREQ
      WHERE WORD IN ('tweets', 'social', 'hadoop'))
  INNER JOIN
     (SELECT PDF_ID AS P2, WORD AS W2, 72.0 / COUNT(PDF_ID) AS TIDF
      FROM FREQ WHERE W2 IN ('tweets', 'social', 'hadoop')
      GROUP BY W2) ON WORD = W2
;;




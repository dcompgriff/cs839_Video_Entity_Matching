The two tables with the IDs for tuples are stored in the files imdb3_neg_nan.csv (Table A) and thenumbers3_neg_nan.csv (Table B). As the names suggest, "Empty" attributes were filled with a "-1" to indicate that the feature was "empty". Most of the empty entries occur in "thenumbers3_neg_nan.csv".
<p>
<b>[imdb3_neg_nan.csv](imdb3_neg_nan.csv)</b>
<ul>
  <li>The number of tuples are 4291.</li>
  <li>The attributes store movie information are
  <ul>
        <li>id</li>
      <li>the title of the movie,</li>
      <li> year of release</li>
      <li> mpaa column refers to the rating by Motion Pictures Association of America</li>
       <li> the length of the movie</li>
       <li> genre it belongs to</li>
       <li> director for the film</li>
       <li> the stars or the leading actors in the movie</li>
       <li> the total earnings worldwide</li>
   </ul>
   </li>
</ul>
</p>
<p>
<b>[thenumbers3_neg_nan.csv](thenumbers3_neg_nan.csv)</b>
<ul>
  <li>The number of tuples are 31006.</li>
  <li>The attributes store the same information as in imdb3_neg_nan.csv</li>
</ul>
</p>
 
<b>[AllTuplePairs.csv](AllTuplePairs.csv)</b> - This file contains all tuple pairs that remain after the blocking step.<br>
<b>[G.csv](G.csv)</b> - file that lists all tuple pairs in the sample taken, together with the labels, one label per each tuple pair<br>
<b>[I.csv](I.csv)</b> - This file contains training set partition of G.<br>
<b>[J.csv](J.csv)</b> - This file contains test set partition of G.<br>

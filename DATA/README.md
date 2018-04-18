The two tables with the IDs for tuples are stored in the files imdb2.csv and thenumbers2.csv. 
<p>
<b>[imdb2.csv](DATA/imdb2.csv)</b>
<ul>
  <li>The number of tuples are 4291.</li>
  <li>The attributes store movie information are
  <ul>
      <li>the title of the movie,</li>
      <li> year of release,</li>
      <li> mpaa column refers to the rating by Motion Pictures Association of America,</li>
       <li> the length of the movie,</li>
       <li> genre it belongs to,</li>
       <li> star rating in IMDB,</li>
       <li> metascore rating which is indicative of the reviews of critics,</li>
       <li> a short description of the movie,</li>
       <li> director for the film,</li>
       <li> the stars or the leading actors in the movie, and</li>
       <li> the total earnings worldwide.</li>
   </ul>
   </li>
</ul>
</p>
<p>
<b>[thenumbers2.csv](DATA/thenumbers2.csv)</b>
<ul>
  <li>The number of tuples are 31006.</li>
  <li>The attributes store the same information as in imdb2.csv except missing values for columns like stars(i.e actors) , description etc</li>
</ul>
</p>
 
<b>[AllTuplePairs.csv](DATA/AllTuplePairs.csv)</b> - This file contains all tuple pairs that remain after the blocking step.
<b>[G.csv](DATA/G.csv)</b> - file that lists all tuple pairs in the sample taken, together with the labels, one label per each tuple pair
<b>[I.csv](DATA/I.csv)</b> - This file contains training set partition of G.
<b>[J.csv](DATA/J.csv)</b> - This file contains test set partition of G.

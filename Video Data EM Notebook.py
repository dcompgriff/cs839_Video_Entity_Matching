
# coding: utf-8

# # Video Data EM Notebook

# In[3]:


import sys
import py_entitymatching as em
import pandas as pd
import os
import time

###################################################################
#KEY!!!! VARIABLE PREVENTS OVERWRITING LABELED SAMPLED DATA
###################################################################
GENERATE_NEW_LABELED_DATA = False



# In[4]:


# Display the versions
print('python version: ' + sys.version )
print('pandas version: ' + pd.__version__ )
print('magellan version: ' + em.__version__ )


# Matching two tables typically consists of the following three steps:
# 
# ** 1. Reading the input tables **
# 
# ** 2. Blocking the input tables to get a candidate set **
# 
# ** 3. Matching the tuple pairs in the candidate set **

# # Read input tables

# In[5]:


# Get the paths
path_A = os.getcwd() + '/DATA/imdb3_neg_nan.csv'
path_B = os.getcwd() + '/DATA/thenumbers3_neg_nan.csv'
print(path_A)


# In[6]:


# Load csv files as dataframes and set the key attribute in the dataframe
A = em.read_csv_metadata(path_A, key='id')
B = em.read_csv_metadata(path_B, key='id')
A.head()


# In[7]:


B.head()


# ### Check for null entries

# In[8]:


B.isnull().sum()


# In[9]:


A.isnull().sum()


# ### Check the data size

# In[10]:


print('Number of tuples in A: ' + str(len(A)))
print('Number of tuples in B: ' + str(len(B)))
print('Number of tuples in A X B (i.e the cartesian product): ' + str(len(A)*len(B)))


# In[11]:


# Display the keys of the input tables
em.get_key(A), em.get_key(B)


# In[12]:


# If the tables are large we can downsample the tables like this
A1, B1 = em.down_sample(A, B, 200, 1, show_progress=False)
len(A1), len(B1)

# But for the purposes of this notebook, we will use the entire table A and B


# # Block tables to get candidate set
# 
# Before we do the matching, we would like to remove the obviously non-matching tuple pairs from the input tables. This would reduce the number of tuple pairs considered for matching.
# *py_entitymatching* provides four different blockers: (1) attribute equivalence, (2) overlap, (3) rule-based, and (4) black-box. The user can mix and match these blockers to form a blocking sequence applied to input tables.
# 
# For the matching problem at hand, we know that two restaurants with different city names will not match. So we decide the apply blocking over names:

# In[13]:


# Blocking plan

# A, B -- overlap blocker [title] --------------------|---> candidate set


# In[14]:


# Create attribute equivalence blocker
ab = em.OverlapBlocker()

# Block using city attribute
C1 = ab.block_tables(A, B, 'title', 'title', 
                    l_output_attrs=['title', 'year', 'mpaa', 'runtime', 'genres', 'director', 'stars', 'gross'], 
                    r_output_attrs=['title', 'year', 'mpaa', 'runtime', 'genres', 'director', 'stars', 'gross'],
                    overlap_size=1
                    )


# In[15]:


len(C1)


# ## Debug blocker output

# The number of tuple pairs considered for matching is reduced to 10,956,134 (from 133,046,746), but we would want to make sure that the blocker did not drop any potential matches. We could debug the blocker output in *py_entitymatching* as follows:

# In[16]:


# Debug blocker output
startTime = time.time()
dbg = em.debug_blocker(C1, A, B, output_size=200, attr_corres=[('title','title'), ('year', 'year')])
endTime = time.time()
print("Total time: %.2f seconds."%(endTime-startTime))


# In[17]:


# Display first few tuple pairs from the debug_blocker's output
dbg.head(50)


# From the debug blocker's output we observe that the current blocker drops quite a few potential matches. We would want to update the blocking sequence to avoid dropping these potential matches.
# 
# For the considered dataset, we know that for the restaurants to match the  names must overlap between them. We could use overlap blocker for this purpose. Finally, we would want to union the outputs from the attribute equivalence blocker and the overlap blocker to get a consolidated candidate set.

# In[18]:


# Updated blocking sequence
# A, B ------ overlap blocker [title] -----> C1--
#                                                     
# C1 ------ overlap blocker [year] --------> C2--


# In[19]:


# Create overlap blocker
ob = em.OverlapBlocker()

# Block tables using 'name' attribute 
C2 = ob.block_candset(C1, 'year', 'year' 
                    )
len(C2)


# In[20]:


# Display first two rows from C2
C2.head(2)


# In[21]:


# Updated blocking sequence
# A, B ------ overlap blocker [title] -----> C1--
#                                                     
# C1 ------ overlap blocker [year] --------> C2--
#
# C2 ------ overlap blocker [mpaa] --------> C3--


# In[22]:


# Create overlap blocker
ob = em.OverlapBlocker()

# Block tables using 'name' attribute 
C3 = ob.block_candset(C2, 'mpaa', 'mpaa' 
                    )
len(C3)


# In[23]:


# Display first two rows from C3
C3.head(2)


# In[24]:


# Create blocker to block tuples that only match based on 'the'.
def overlap_ignoring_words(ltuple, rtuple):
    words = set(['the'])
    # Remove ignore words set from strings.
    lostring = ltuple['title'].lower().split()
    rostring = rtuple['title'].lower().split()
    l_tokens = []
    r_tokens = []
    for word in lostring:
        if word.strip() not in words:
            l_tokens.append(word)
    for word in rostring:
        if word.strip() not in words:
            r_tokens.append(word)
    l_tokens = set(l_tokens)
    r_tokens = set(r_tokens)
        
    # Compute overlap.
    #l_tokens = set(list(map(lambda item: item.strip(), lstring.split())))
    #r_tokens = set(list(map(lambda item: item.strip(), rstring.split())))
    intersection = l_tokens.intersection(r_tokens)
    if len(intersection) >= 1:
        return False
    else:
        return True
    
# Create and apply blocker.
bb = em.BlackBoxBlocker()
bb.set_black_box_function(overlap_ignoring_words)
C4 = bb.block_candset(C3)    
C4.head()
    


# In[25]:


len(C4)


# We observe that the current blocker sequence does not drop obvious potential matches, and we can proceed with the matching step now. A subtle point to note here is, debugging blocker output practically provides a stopping criteria for modifying the blocker sequence.
# 

# # Matching tuple pairs in the candidate set

# In this step, we would want to match the tuple pairs in the candidate set. Specifically, we use learning-based method for matching purposes.
# This typically involves the following five steps:
# 1. Sampling and labeling the candidate set
# 2. Splitting the labeled data into development and evaluation set
# 3. Selecting the best learning based matcher using the development set
# 4. Evaluating the selected matcher using the evaluation set

# ## Sampling and labeling the candidate set

# First, we randomly sample 600 tuple pairs for labeling purposes.

# In[26]:


# Sample  candidate set
S = em.sample_table(C4, 600)
S.head()


# In[27]:


if GENERATE_NEW_LABELED_DATA:
    # Label S interactively. 
    G = em.label_table(S, 'gold')
    # SAVE! TIS A BITCH TO LABEL S AGAIN, AND IT NEEDS TO BE LABELED WITHIN THE UI!
    em.to_csv_metadata(G, './DATA/G.csv')
else:
    # Load the dataset.
    G = em.read_csv_metadata('./DATA/G.csv', 
                         key='_id',
                         ltable=A, rtable=B, 
                         fk_ltable='ltable_id', fk_rtable='rtable_id')


# ## Splitting the labeled data into development and evaluation set

# In this step, we split the labeled data into two sets: development (I) and evaluation (J). Specifically, the development set is used to come up with the best learning-based matcher and the evaluation set used to evaluate the selected matcher on unseen data.

# In[28]:


# Split S into development set (I) and evaluation set (J)
IJ = em.split_train_test(G, train_proportion=0.7, random_state=5)
I = IJ['train']
J = IJ['test']
print(len(I[I['gold']==1]))
print(len(J[J['gold']==1]))


# ## Selecting the best learning-based matcher 

# Selecting the best learning-based matcher typically involves the following steps:
# 
# 1. Creating a set of learning-based matchers
# 2. Creating features
# 3. Converting the development set into feature vectors
# 4. Selecting the best learning-based matcher using k-fold cross validation

# ### Creating a set of learning-based matchers

# In[29]:


# Create a set of ML-matchers
dt = em.DTMatcher(name='DecisionTree', random_state=0)
svm = em.SVMMatcher(name='SVM', random_state=0)
rf = em.RFMatcher(name='RF', random_state=0)
lg = em.LogRegMatcher(name='LogReg', random_state=0)
ln = em.LinRegMatcher(name='LinReg')
nb = em.NBMatcher(name='NaiveBayes')


# ### Creating features

# Next, we need to create a set of features for the development set. *py_entitymatching* provides a way to automatically generate features based on the attributes in the input tables. For the purposes of this guide, we use the automatically generated features.

# In[30]:


# Generate features
feature_table = em.get_features_for_matching(A, B, validate_inferred_attr_types=False)


# In[31]:


# List the names of the features generated
feature_table['feature_name']


# ### Converting the development set to feature vectors

# In[32]:


# Convert the I into a set of feature vectors using F
H = em.extract_feature_vecs(I, 
                            feature_table=feature_table, 
                            attrs_after='gold',
                            show_progress=False)


# In[33]:


# Display first few rows
H.head(3)


# ### Selecting the best matcher using cross-validation

# Now, we select the best matcher using k-fold cross-validation. For the purposes of this guide, we use five fold cross validation and use 'precision' and 'recall' metric to select the best matcher.

# In[34]:


# Select the best ML matcher using CV
result = em.select_matcher([dt, rf, svm, ln, lg, nb], table=H, 
        exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'gold'],
        k=5,
        target_attr='gold', metric_to_select_matcher='f1', random_state=0)
result['cv_stats']


# ### Debugging matcher

# In[35]:


#  Split feature vectors into train and test
UV = em.split_train_test(H, train_proportion=0.5)
U = UV['train']
V = UV['test']


# Next, we debug the matcher using GUI. For the purposes of this guide, we use random forest matcher for debugging purposes.

# In[36]:


# Debug decision tree using GUI
# em.vis_debug_rf(rf, U, V, 
#        exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'gold'],
#        target_attr='gold')


# ##  Evaluating the matching output

# Evaluating the matching outputs for the evaluation set typically involves the following four steps:
# 1. Converting the evaluation set to feature vectors
# 2. Training matcher using the feature vectors extracted from the development set
# 3. Predicting the evaluation set using the trained matcher
# 4. Evaluating the predicted matches

# ### Converting the evaluation set to  feature vectors

# As before, we convert to the feature vectors (using the feature table and the evaluation set)

# In[37]:


# Convert J into a set of feature vectors using feature table
L = em.extract_feature_vecs(J, feature_table=feature_table,
                            attrs_after='gold', show_progress=False)


# ### Training the selected matcher

# Now, we train the matcher using all of the feature vectors from the development set. For the purposes of this guide we use random forest as the selected matcher.

# In[38]:


# Train using feature vectors from I 
rf.fit(table=H, 
       exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'gold'], 
       target_attr='gold')


# ### Predicting the matches

# Next, we predict the matches for the evaluation set (using the feature vectors extracted from it).

# In[39]:


# Predict on L 
predictions = rf.predict(table=L, exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'gold'], 
              append=True, target_attr='predicted', inplace=False)


# ### Evaluating the predictions

# Finally, we evaluate the accuracy of predicted outputs

# In[40]:


# Evaluate the predictions
eval_result = em.eval_matches(predictions, 'gold', 'predicted')
em.print_eval_summary(eval_result)


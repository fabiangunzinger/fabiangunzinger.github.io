---
title: Tree based methods
---

-   hide: true

-   toc: true

-   comments: true

-   categories: \[python, ml, stats\]

-   Trees

    -   Are an easy and intuitive way to split data within a sample. 
    -   Problem, they are not good at predicting out-of-sample (with different datasets)  

-   Random Forests 

    -   Random forests remedy this by combining the simplicity of decision trees with flexibility, which leads to a large improvement in predictive accuracy. 
    -   How to make a random forest: 
        -   Create bootstrapped sample from data (i.e. sample observations of the original sample with replacement) 
        -   Create a decision tree using only a subset of randomly selected variables at each step (e.g. only 2 out of 4 for root, then 2 out of remaining 3 at next node, ect.) 
        -   Repeat above two steps many times (e.g. 1000) to build many trees (and build a random forest) 
    -   To predict outcome for new observation, do the following: 
        -   Feed data into each tree in the forest and keep score of the predictions (either Yes or No for each tree). The outcome with the most scores is the prediction. 
    -   The process is called "Bagging" because we Bootstrap the data and rely on the AGGregate to make a decision. 
    -   How can we test how good a tree is at out-of sample prediction without having another sample? 
        -   Bootstrapping relies on randomly sampling from data with replacement, hence, not all observations will be used to create a tree. 
        -   The unused observations are called the "Out-of-bag Dataset". We can use these test whether our Forest is any good at predicting. 
        -   We simply take the out-of-bag dataset from each tree, run through the entire Forest and check whether the Forest accurately classifies the observation. We then repeat this for each out-of-bag dataset. 
        -   The proportion of incorrectly classified out-of-bag samples is called the "out-of-bag error". 
    -   The out-of-bag error is what helps us determine how many variables to use when building our random trees above. The algorithm builds different forests with different numbers of variables (typically starting with the square-root of the total number of variables -- e.g. 2 if we have 4 variables -- and then calculating a few above and below that) and then picks the one with the smallest out-of-bag error.  

-   Ada boosts 

    -   When building random forests, trees vary in their depth. 
    -   When using Ada boost to create a Random Forest, each tree is usually just one node and two leaves. (A tree with one node and two leaves is a "stump"). So, Ada boost produces a Forest of Stumps. 
    -   Because a stump only makes use of a single variable, they are generally poor predictors. 
    -   Main ideas of ada boost 
        -   Take Forest of Stumps 
        -   Stumps have different weights (mounts of say) in the calculation of the out-of-bag error (with the weights being proportional to the gravity of the prediction errors they make. Loosely speaking, for how many observations they get the prediction wrong).  
        -   Each stump takes the errors of the previous stump into account (it does this by treating as more important those observations that the previous stump misclassified).  
    -   Process 
        -   Create first Stump using the variable that best classifies outcomes 
        -   Then calculate classification error 
        -   The size of that error determines the weight this stump gets in the overall classification (i.e. in the Forest of Stumps). 
        -   The next stump will be build using the variable that best classifies outcomes in a dataset that over-emphasizes the observations that the previous stump misclassified. 
        -   As in a Random Forst, we run all obseravtions through all Stumps and keep track of the classification. Instead of adding up the Yes and No, we add up the amount of say of the Yes Stumps and No Stumps and classify as Yes if total amount of say of yes Stumps is larger. 

-   Gradient boosting (most used configuration) 

    -   Comparison to Ada boost 
        -   Like Ada boost builds fixed size trees, but they can be larger than a Stump (in our specification, we use trees with a depth of 5) 
        -   GB also scales trees, but all by same amount 
        -   Also builds tree based on error of previous tree 
    -   Algorithm 
        -   Predict based on average and calculate (pseudo residuals) 
        -   Then build a tree to predict residuals 
        -   Scale predicted residual by the learning rate (we use 0.1) and add to original prediction. 
        -   Calculate new pseudo residuals and build new tree to predict. 
        -   Add scaled predictions to the previous prediction (i.e. to the original prediction and the previous scaled prediction). 
        -   Keep going like this until additional trees no longer improve prediction or hit number of max trees. 

-   Initial prediction is log of odds: log(number in HE/number not in HE) and convert to a probability using the logistic function (e^logodds / 1 + e^logodds). If probability \> 0.5, prediction is "Yes" for all observations. Else is no 

-   Calculate pseudo residuals as actual - predicted (e.g. 1 - 0.7) 

-   Build tree to predict residuals

## Sources

-   [Brilliant series of videos on StatQuest](https://www.youtube.com/c/joshstarmer)

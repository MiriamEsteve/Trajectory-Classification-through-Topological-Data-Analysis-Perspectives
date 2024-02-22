import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def classification_persim(imgs_array):
    N = len(imgs_array)
    labels = np.zeros(N)
    N_per_class = int(N / 2)
    labels[N_per_class:] = 1
    '''
    for i in range(N):
        var = imgs_array[i].var()
        if var < 1:
            labels[i] = 0
        else:
            labels[i] = 1
    '''
    X_train, X_test, y_train, y_test = train_test_split(imgs_array, labels, test_size=0.40, random_state=42)
    lr = LogisticRegression()
    lr.fit(X_train, y_train)
    return lr.score(X_test, y_test)




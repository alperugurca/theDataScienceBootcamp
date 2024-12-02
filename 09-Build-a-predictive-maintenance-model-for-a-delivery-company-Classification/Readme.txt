In the last session, we will host a private Kaggle competition amongst the students.
Students will be grouped into teams and will showcase their group project at the end of class.
This will also be a career day, where we will assess students on their presentation skills, as well as their business skills in terms of the project.
Please be advised that the dataset is highly imbalanced.
So, use the link below to apply the techniques to handle imbalanced datasets.

# transform the dataset
from imblearn.over_sampling import SMOTE

oversample = SMOTE()
x, y = oversample.fit_resample(x, y)
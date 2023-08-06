<div align="center">
<h1>SIMPLYSKLEARN</h1>
<br>

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

<br>

<p>Time to even automate your machine learning process!

<br>
<br>
</div>

## Description

As Bill Gates once said, “I choose a lazy person to do a hard job. Because a lazy person will find an easy way to do it.”.

After numerous hours, days, weeks and months spent on Kaggle, I was inspired to sum up all the repetitive and tedious process to one single package. 
For any machine learning projects, the user must perform data manipulations, check the dataset is all set for models.
After that, they must fit it into models and take note of how the model performs. 

With this package, I want to eliminate that tedious stage for any user. 
This package would mainly be beneficial to those recently starting out in the field of machine learning or intermediate users. 
It is probably unsuitable for highly complex models or datasets. 

The main usage should be to assist the user by assessing the performances of myriad of models.

## What it provides

* Prepares datatset by takeing care of categorical feature by one-hot-encoding and numerical feature by scaling.
* Fits the engineered dataset on myriad of Scikit-Learn models. 
* Depending on what metric you want to observe, will plot you a colorful comparison of metrics of different models. 

## Future Improvements 

* Automated hyperparameter tuning process
* Option to display feature importances 

## Getting Started

### Dependencies

* Programming Language: Python
* License: MIT
* Operating System: Independent
* [Dependencies](https://github.com/vanilladucky/simplysklearn/blob/main/requirements.txt)

### Installing

```
pip install simplysklearn
```
The python package website can be accessed [here](https://pypi.org/project/simplysklearn/) 

### Executing program

```
from simplysklearn.model import ExploreModel
```

## Classification Example 
```
import pandas as pd
df = pd.read_csv('titanic.csv')
model = ExploreModel(df, feature_columns_list, 'Survived', PredictProba = False, EnsembleBoolean=True, NeuralBoolean=True, SplitRatio=0.3, OutputType='classification')
model.fit()
model.calculate_accuracy()
model.plot('accuracy_score')
print(model.outlier_values)
```
![image](https://user-images.githubusercontent.com/77542415/215261264-a14ed13e-9bdc-4d76-b280-b1040c7ab74c.png)

## Regression Example
```
import pandas as pd
df = pd.read_csv('housing_prices.csv')
model = ExploreModel(df, feature_columns_list, 'SalePrice', PredictProba = False, EnsembleBoolean=True, NeuralBoolean=True, SplitRatio=0.3, OutputType='regression')
model.fit()
model.calculate_accuracy()
model.plot('mean_squared_error')
print(model.outlier_values)
```


## Documentation

Documentation coming soon.

## Authors

* Kim Hyun Bin 
* [Email](KIMH0004@e.ntu.edu.sg)
* [Kaggle](https://www.kaggle.com/kimmik123)

## Version History

* 0.0.1
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE file for details

# lazyeval

Python package to automate machine learning process to showcase metric values for nearly all Scikit-Learn's models. 

## Description

As Bill Gates once said, “I choose a lazy person to do a hard job. Because a lazy person will find an easy way to do it.”.

After numerous hours, days, weeks and months spent on Kaggle, I was inspired to sum up all the repetitive and tedious process to one single package. 
For any machine learning projects, the user must perform data manipulations, check the dataset is all set for models.
After that, they must fit it into models and take note of how the model performs. 

With this package, I want to eliminate that tedious stage for any user. 
This package would mainly be beneficial to those recently starting out in the field of machine learning or intermediate users. 
It is probably unsuitable for highly complex models or datasets. 

The main usage should be to assist the user by assessing the performances of myriad of models.

## Getting Started

### Dependencies

* Programming Language: Python
* License: MIT
* Operating System: Independent
* Libraries: [link]

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders
```
pip install lazyeval==0.0.9
```
The python package website can be accessed [here](https://pypi.org/project/lazyeval/0.0.9/) 

### Executing program

To run the program, it is mostly like any other machine learning libraries out there. 
```
from lazyeval.model import ExploreModel
```
## Example 
```
import pandas as pd
df = pd.read_csv('classification.csv')
model = ExploreModel(df, df.columns.tolist()[2:], 'Survived', PredictProba = False, EnsembleBoolean=True, NeuralBoolean=True, SplitRatio=0.3, OutputType='classification')
model.fit()
model.calculate_accuracy()
model.plot('accuracy_score')
print(model.outlier_values)
```
![image](https://user-images.githubusercontent.com/77542415/215261264-a14ed13e-9bdc-4d76-b280-b1040c7ab74c.png)


## Documentation

Documentation coming soon.

## Authors

* Kim Hyun Bin 
* KIMH0004@e.ntu.edu.sg
* [Kaggle](https://www.kaggle.com/kimmik123)

## Version History

* 0.0.9
    * Various bug fixes and logic corrections
* 0.0.1
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

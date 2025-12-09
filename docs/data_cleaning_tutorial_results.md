# Data Cleaning Tutorial (Notebook-Free Summary)

This page captures the executed results of `test/data_cleaning_tutorial.ipynb` so you can review the workflow without opening the notebook. Each code cell is shown alongside its output.

## Setup
```python
import sys
import pandas as pd
from pathlib import Path
from Fixmydata import DataCleaner, DataValidator, OutlierDetector

ROOT = Path().resolve()
DATA_DIR = ROOT / 'datasets'
```

## 1) Titanic-style passenger data

### Load data
```python
from pathlib import Path
import pandas as pd

titanic_path = DATA_DIR / 'tested.csv'
titanic_df = pd.read_csv(titanic_path)
print(titanic_df.shape)
titanic_df.head()
```

Output:
```
(418, 12)
   PassengerId  Survived  Pclass                                          Name     Sex  SibSp  Parch   Ticket     Fare Cabin  Embarked
0          892         0       3                              Kelly, Mr. James    male      0      0   330911   7.8292   NaN         Q
1          893         1       3              Wilkes, Mrs. James (Ellen Needs)  female      0      0   363272   7.0000   NaN         S
2          894         0       2                     Myles, Mr. Thomas Francis    male      0      0   240276   9.6875   NaN         Q
3          895         0       3                              Wirz, Mr. Albert    male      0      0   315154   8.6625   NaN         S
4          896         1       3  Hirvonen, Mrs. Alexander (Helga E Lindqvist)  female      1      1  3101298  12.2875   NaN         S

[418 rows x 12 columns]
```

### Inspect missing values
```python
titanic_df.isnull().sum().to_frame("missing_values")
```

Output:
```
             missing_values
PassengerId               0
Survived                  0
Pclass                    0
Name                      0
Sex                       0
Age                      86
SibSp                     0
Parch                     0
Ticket                    0
Fare                      1
Cabin                   327
Embarked                  0
```

### Clean
```python
cleaning = DataCleaner(titanic_df)

age_median = cleaning.data['Age'].median()
fare_median = cleaning.data['Fare'].median()
cleaning.fill_missing('Age', age_median)
cleaning.fill_missing('Fare', fare_median)
cleaning.fill_missing('Cabin', 'Unknown')

titanic_clean = cleaning.remove_duplicates()
titanic_clean.head()
```

Output:
```
   PassengerId  Survived  Pclass                                          Name  SibSp  Parch   Ticket     Fare    Cabin  Embarked
0          892         0       3                              Kelly, Mr. James      0      0   330911   7.8292  Unknown         Q
1          893         1       3              Wilkes, Mrs. James (Ellen Needs)      0      0   363272   7.0000  Unknown         S
2          894         0       2                     Myles, Mr. Thomas Francis      0      0   240276   9.6875  Unknown         Q
3          895         0       3                              Wirz, Mr. Albert      0      0   315154   8.6625  Unknown         S
4          896         1       3  Hirvonen, Mrs. Alexander (Helga E Lindqvist)      1      1  3101298  12.2875  Unknown         S

[418 rows x 12 columns]
```

### Validate
```python
validator = DataValidator(titanic_clean)
validator.validate_non_empty()
validator.validate_range('Age', 0, 90)

titanic_clean[['Age', 'Fare']].describe()
```

Output:
```
              Age        Fare
count  418.000000  418.000000
mean    29.599282   35.576535
std     12.703770   55.850103
min      0.170000    0.000000
25%     23.000000    7.895800
50%     27.000000   14.454200
75%     35.750000   31.471875
max     76.000000  512.329200
```

### Detect outliers
```python
detector = OutlierDetector(titanic_clean)
titanic_iqr = detector.iqr_outliers()

print('Original rows:', len(titanic_clean))
print('Rows after IQR filtering:', len(titanic_iqr))

titanic_iqr[['Age', 'Fare']].describe()
```

Output:
```
Original rows: 418
Rows after IQR filtering: 281
              Age        Fare
count  281.000000  281.000000
mean    28.272242   15.618090
std      7.876031   12.818909
min     12.000000    0.000000
25%     24.000000    7.775000
50%     27.000000    8.662500
75%     30.000000   21.000000
max     54.000000   65.000000
```

## 2) USA housing data

### Load data
```python
housing_path = DATA_DIR / 'USA Housing Dataset.csv'
housing_df = pd.read_csv(housing_path)
housing_df.head()
```

Output:
```
                  date      price  bedrooms  bathrooms     sqft_living    sqft_lot  floors  waterfront         view  condition  grade  sqft_above  sqft_basement  yr_built  yr_renovated        street       city  statezip country
0  2014-05-09 00:00:00   376000.0       3.0       2.00          1340.0    7912.00     1.5         0.0    46.534953        4.0     7.0      1340.0            0.0      1955           0.0  9245-9249 Fremont Ave N    Seattle  WA 98103     USA
1  2014-05-09 00:00:00   800000.0       4.0       3.25          3650.0  110642.00     2.0         0.0  1015.101546        3.0    10.0      3370.0          280.0      1964        2013.0         33001 NE 24th St  Carnation  WA 98014     USA
2  2014-05-09 00:00:00  2238888.0       5.0       6.50          4980.0   36920.00     2.0         1.0  1015.101546        3.0    12.0      4450.0          530.0      2001           0.0         7070 270th Pl SE   Issaquah  WA 98029     USA
3  2014-05-09 00:00:00   324000.0       3.0       2.25          2150.0    6380.00     1.0         0.0   145.604088        4.0     7.0      1330.0          820.0      1912           0.0           820 NW 95th St    Seattle  WA 98117     USA
4  2014-05-10 00:00:00   549900.0       5.0       2.75          1890.0    4160.00     1.0         0.0    46.534953        3.0     7.0      1890.0            0.0      1976           0.0        10834 31st Ave SW    Seattle  WA 98146     USA

[4140 rows x 18 columns]
```

### Clean, filter outliers, and summarize
```python
housing_cleaner = DataCleaner(housing_df)
housing_base = housing_cleaner.remove_duplicates()

housing_detector = OutlierDetector(housing_base)
housing_no_outliers = housing_detector.z_score_outliers(threshold=3)

price_sqft_corr = housing_no_outliers['price'].corr(housing_no_outliers['sqft_living'])
print(f'Correlation between price and square footage: {price_sqft_corr:.3f}')

housing_no_outliers[['price', 'sqft_living', 'bedrooms', 'bathrooms']].describe()
```

Output:
```
Correlation between price and square footage: 0.611
              price  sqft_living     bedrooms   bathrooms
count  3.805000e+03  3805.000000  3805.000000  3805.00000
mean   4.991892e+05  2019.579763     3.349803     2.09159
std    2.716459e+05   786.018440     0.855091     0.70747
min    0.000000e+00   370.000000     1.000000     0.75000
25%    3.128910e+05  1430.000000     3.000000     1.75000
50%    4.448450e+05  1910.000000     3.000000     2.25000
75%    6.200000e+05  2500.000000     4.000000     2.50000
max    2.300000e+06  4960.000000     6.000000     4.50000
```

---
For quick orientation during presentations, pair these results with the visual pipeline and walkthrough in `docs/fixmydata_presentation.md`.

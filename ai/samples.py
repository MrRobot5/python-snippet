import pandas as pd

if __name__ == '__main__':
    s = pd.Series(['a', 'a', 'b', 'c'])
    s.describe()

    data = pd.read_csv('https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv')
    data.describe()

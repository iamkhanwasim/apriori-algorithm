import pandas as pd

def generate_one_hot_encoding(df):
    """
        This method generates one hot encoding for pandas dataframe
        Output to this method is also pandas dataframe
        This method utlizes in-built method from pandas to return one-hot encoding
    """
    basket = df.groupby(['Transactions'])['Item']
    return basket



if __name__ == "__main__":
    df = pd.DataFrame({
        'Transactions': ['T1','T1','T1','T2','T3','T3','T3','T3','T4','T4','T4','T5','T5','T6','T6','T6','T6','T7','T7','T8','T8','T9','T9','T9','T9','T10','T10'], 
        'Item': ['bread','butter','milk','milk','bread','milk','sugar','tea','bread','butter','milk','milk','cereals','milk','coffee','sugar','tea','milk','bread','cereals','butter','bread','cereals','sugar','tea','bread','coffee']})
    # print(df)
    print(generate_one_hot_encoding(df))
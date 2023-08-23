import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from sklearn.feature_extraction import DictVectorizer

# Read data in various formats, including CSV, Excel, and SQL databases.
def user():
    def process_csv(file_path):
        df = pd.read_csv(file_path)
        return df

    def process_excel(file_path):
        df = pd.read_excel(file_path)
        return df

    def process_sql(database_path):
        # Create your connection.
        conn = sqlite3.connect(database_path, table_name)
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, conn)
        conn.commit()
        conn.close()
        return df
    
    try:
        print("Please, Enter the path of the file")
        print("Make sure the file extension is 'csv', 'xlsx' or 'db'")
        file_path = input()
        if file_path.split('.')[1] == 'csv':
            return process_csv(file_path)
        elif file_path.split('.')[1] == 'xlsx':
            return process_excel(file_path)
        elif file_path.split('.')[1] == 'db':
            table_name = input("Please, Enter the table name: ")
            return process_sql(database_path, table_name)
    except:
        print("Opps, you input something error")


# identifying the data types of each column
def identifying_column(df):
    print("\n")
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print("Dataframe:")
    print("\n")
    print(df)
    print("\n")
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print("identifying the data types of each column:")
    print("\n")
    print(pd.DataFrame(df.dtypes))
    print("\n")
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print("identifying the data types of each column:")
    print("\n")
    print(df.info())


# handling duplicates and nulls values
def handle_duplicates_and_nulls(df):
    # print(df.duplicated())
    df = df.drop_duplicates()
    print("\n")
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print("\n")
    print("The duplicated rows had handled")
    print("\n")
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print("Sum of null values:")
    print("\n")
    print(df.isna().sum())
    print("\n")
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print("\n")
    lst_of_columns_name = list (df.columns)
    lst_of_types = list(dict(pd.DataFrame(df.dtypes))[0])
    lst_of_null_values =  list(df.isna().sum())
    for i in range(0, len(lst_of_null_values)):
        if lst_of_null_values[i] != 0:
            print(f"A column named '{lst_of_columns_name[i]}' and type '{lst_of_types[i]}' contains ({lst_of_null_values[i]}) null values")
            if lst_of_types[i] != "object":
                print("Please, Enter the number of your choice to handle missing data")
                print("1) Dropping rows with missing values")
                print("2) Imputing missing values with the median")
                print("3) Imputing missing values with the mean")
                print("4) Imputing missing values a constant")
                print("5) None")
                answer = input()
                if answer == "1":
                    # Handling missing data (dropping rows with missing values)
                    df = df.dropna()
                elif answer == "2": 
                    # Handling missing data (imputing missing values with the median)
                    df = df.fillna(df.median())
                elif answer == "3":
                    # Handling missing data (imputing missing values with the mean)
                    df = df.fillna(df.mean())
                elif answer == "4":
                    # Handling missing data (imputing missing values with a constant)
                    constant = input('Please, Enter the constant ')
                    df = df.fillna(constant)
                elif answer == "5":
                    print("Ok")
                    print("The nulls values had not handled")
                else:
                    print(f"You made the wrong choice --> {answer}")
                    print("The nulls values had handled by dropping rows with missing values")
                    df = df.dropna()
            else:
                print("Please, Enter the number of your choice to handle missing data")
                print("1) Dropping rows with missing values")
                print("2) Imputing missing values a constant")
                print("3) None")
                answer = input()
                if answer == "1":
                    # Handling missing data (dropping rows with missing values)
                    df = df.dropna()
                elif answer == "2":
                    # Handling missing data (imputing missing values with a constant)
                    constant = input('Please, Enter the constant ')
                    df = df.fillna(constant)
                elif answer == "3":
                    print("Ok")
                    print("The nulls values had not handled")
                else:
                    print(f"You made the wrong choice --> {answer}")
                    print("The nulls values had handled by dropping rows with missing values")
                    df = df.dropna()
    return df

# ncoding categorical features
def encode_categorical_features(df):
    # turn df into dict
    df_dict = df.to_dict(orient='records') 
    # instantiate a Dictvectorizer object for X
    dv_X = DictVectorizer(sparse=False)  # sparse = False makes the output is not a sparse matrix
    # apply dv_X on df_dict
    X_encoded = dv_X.fit_transform(df_dict)
    return X_encoded

# Scaling numerical features
def normalize_dataframe(df):
    lst_of_columns_name = list (df.columns)
    lst_of_types = list(dict(pd.DataFrame(df.dtypes))[0])
    for index in range(0, len(lst_of_types)):
        if lst_of_types[index] == "object":
            df = df.drop(lst_of_columns_name[index], axis=1)
    
    # Pandas Normalize using Mean Normalization
    normalized_df=df.apply(lambda x: (x-x.mean())/ x.std(), axis=0)
    return normalized_df

def data_visualization(df):
    def Plot_details(columns):
        plt.figure(figsize=(10,7))
        plt.plot(df[columns], df[columns] , label = columns)
        # add label in x-axis and y-axis
        plt.xlabel(columns)
        plt.ylabel(columns)
        # add title for graph
        plt.title(f'plot for {columns}')
        plt.legend()
        plt.grid(True)
        plt.show()
        
    def Bar_chart(columns):
        count = df[columns].value_counts()
        count = pd.DataFrame(count)
        plt.bar(count.T.columns, count[columns], label = columns)
        plt.xlabel(columns)
        plt.title(f'Bar chart for {columns}')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    def histogram(columns):
        plt.figure(figsize=(10,7))
        plt.hist(df[columns], bins= 100, color='red', label = columns)
        # add label in x-axis and y-axis
        plt.xlabel(columns)
        # add title for graph
        plt.title(f'plot for {columns}')
        plt.grid()
        plt.legend()
        plt.show()
    
    def Scatter_plot(columns_1, columns_2):
        plt.scatter(df[columns_1], df[columns_2], color='red', label= f'{columns_1} vs {columns_2}')

        plt.legend()
        plt.grid(True)
        plt.show()

    def Pie_chart(columns):
        count = df[columns].value_counts()
        print(count)
        plt.figure(figsize=(10,10))
        plt.pie(count, labels=count.index.values.tolist(), rotatelabels=True)
        plt.title(columns)
        plt.show()
    
    
    lst_of_columns_name = list (df.columns)
    lst_of_types = list(dict(pd.DataFrame(df.dtypes))[0])
    
    for index in range(0, len(lst_of_types)):
        if lst_of_types[index] != "object":
            print(f'Any graphical relations you want to apply to {lst_of_columns_name[index]}?')
            print("Please, Enter the numbers of your choices separated by ','")
            print("1) Plot Details")
            print("2) Bar Chart")
            print("3) Histogram")
            print("4) Pie Chart")
            print("5) None")
            answer = input()
            answer = answer.split(',')
            for i in answer:
                if i == "1":
                    Plot_details(lst_of_columns_name[index])
                elif i == "2": 
                    Bar_chart(lst_of_columns_name[index])
                elif i == "3":
                    histogram(lst_of_columns_name[index])
                elif i == "4":
                    Pie_chart(lst_of_columns_name[index])
                elif i == "5":
                    print("Ok") 
                else:
                    print(f"You made the wrong choice --> {i}")
    
        else:
            print(f'Any graphical relations you want to apply to {lst_of_columns_name[index]}?')
            print("Please, Enter the numbers of your choices separated by ','")
            print("1) Bar Chart")
            print("2) Pie Chart")
            print("3) None")
            answer = input()
            answer = answer.split(',')
            for i in answer:
                if i == "1":
                    Bar_chart(lst_of_columns_name[index])
                elif i == "2": 
                    Pie_chart(lst_of_columns_name[index])
                elif i == "3":
                    print("Ok")
                else:
                    print(f"You made the wrong choice --> {i}")   

flag = True
while flag:
    try:
        df = user()
        #df = df.head(100)
        identifying_column(df)
        df = handle_duplicates_and_nulls(df)
        encode_df = encode_categorical_features(df)
        print("\n")
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print("Encode df")
        print("\n")
        print(encode_df)
        print("\n")
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        normalized_df = normalize_dataframe(df)
        print("Normalized df")
        print("\n")
        print(normalized_df)
        print("\n")
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print("\n")
        data_visualization(df)
        flag = False
    except:
        print('Do you want to enter the path of the file again?')
        print("Please, Enter the number of your choice")
        print("Please note that if you enter a wrong choice, it will be charged 'no'.")
        print("1) YES")
        print("2) NO")
        answer = input()
        if answer != "1":
            flag = False






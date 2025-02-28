# Required Libraries
import pandas as pd

# Section 0: Setup - Function Definitions

def import_data(file_name):
    """Read relevant data from DOE High School Directory CSV file."""
    cols = [
        "dbn", "school_name", "borocode", "NTA", "graduation_rate",
        "pct_stu_safe", "attendance_rate", "college_career_rate",
        "language_classes", "advancedplacement_courses"
    ]
    df = pd.read_csv(file_name, usecols=cols)
    df = df.dropna(subset=['graduation_rate'])
    return df

def impute_numeric_cols_median(df):
    """Impute missing numeric values with column median."""
    numeric_cols = ['pct_stu_safe', 'attendance_rate', 'college_career_rate']
    for col in numeric_cols:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
    return df

def compute_item_count(df, col):
    """Count the number of items separated by commas in each entry."""
    return df[col].fillna('').apply(lambda x: len([i for i in x.split(',') if i.strip() != '']))

def encode_categorical_col(x):
    """One-hot encode a categorical column using pandas get_dummies."""
    return pd.get_dummies(x)

def split_test_train(df, x_col_names, y_col_name, frac=0.25, random_state=922):
    """Split data into train and test subsets."""
    test_df = df.sample(frac=frac, random_state=random_state)
    train_df = df.drop(test_df.index)
    x_train = train_df[x_col_names]
    x_test = test_df[x_col_names]
    y_train = train_df[y_col_name]
    y_test = test_df[y_col_name]
    return (x_train, x_test, y_train, y_test)

# Section 1: Data Ingestion and Feature Engineering

# Example usage for Section 1
if False:  # Change to True to test with sample data
    file_name = '2021_DOE_High_School_Directory_SI.csv'
    si_df = import_data(file_name)
    print(si_df.columns)
    print(si_df)

    file_name = '2020_DOE_High_School_Directory_late_start.csv'
    late_df = import_data(file_name)
    late_df = impute_numeric_cols_median(late_df)
    print(late_df[['dbn','pct_stu_safe','attendance_rate','college_career_rate']])

    late_df['language_count'] = compute_item_count(late_df, 'language_classes')
    late_df['ap_count'] = compute_item_count(late_df, 'advancedplacement_courses')
    print(late_df[['dbn','language_count','ap_count']])

    boros_df = encode_categorical_col(late_df['borocode'])
    print(boros_df.sum(axis=0))

    x_cols = ['language_count','ap_count','pct_stu_safe','attendance_rate','college_career_rate']
    y_col = 'graduation_rate'
    x_train, x_test, y_train, y_test = split_test_train(late_df, x_cols, y_col)
    print(f'Train rows: {len(x_train)}, Test rows: {len(x_test)}')

# Section 2: Training a Linear Regressor

def compute_lin_reg(x, y):
    """Compute slope and intercept for 1D linear regression."""
    sd_x = x.std()
    sd_y = y.std()
    r = x.corr(y)
    theta_1 = r * (sd_y / sd_x)
    theta_0 = y.mean() - theta_1 * x.mean()
    return (theta_0, theta_1)

# Example usage for Section 2
if False:
    x_cols = ['language_count', 'ap_count', 'pct_stu_safe', 'attendance_rate', 'college_career_rate']
    coeff = {}
    for col in x_cols:
        coeff[col] = compute_lin_reg(x_train[col], y_train)
        print(f'For {col}, theta_0 = {coeff[col][0]}, theta_1 = {coeff[col][1]}')

# Section 3: Model Evaluation

def predict(x, theta_0, theta_1):
    """Make predictions using linear model."""
    return theta_0 + theta_1 * x

def mse_loss(y_actual, y_estimate):
    """Compute Mean Squared Error."""
    return ((y_actual - y_estimate) ** 2).mean()

def rmse_loss(y_actual, y_estimate):
    """Compute Root Mean Squared Error."""
    return mse_loss(y_actual, y_estimate) ** 0.5

def compute_loss(y_actual, y_estimate, loss_fnc=mse_loss):
    """Compute specified loss function."""
    return loss_fnc(y_actual, y_estimate)

# Example usage for Section 3
if False:
    y_train_predictions = {}
    y_test_predictions = {}
    train_losses = {}
    test_losses = {}
    for col in x_cols:
        theta_0, theta_1 = coeff[col]
        y_train_predictions[col] = predict(x_train[col], theta_0, theta_1)
        y_test_predictions[col] = predict(x_test[col], theta_0, theta_1)
        train_losses[col] = compute_loss(y_train, y_train_predictions[col])
        test_losses[col] = compute_loss(y_test, y_test_predictions[col])
    losses_df = pd.DataFrame({'train_loss': train_losses, 'test_loss': test_losses})
    print(losses_df)

#Optional Graphing (requires matplotlib, not for submission)

import matplotlib.pyplot as plt
def graph_data(df, col, coeff):

    plt.scatter(df[col], df['graduation_rate'], label='Actual')
    predict_grad = predict(df[col], coeff[col][0], coeff[col][1])
    plt.scatter(df[col], predict_grad, label='Predicted')
    plt.title(f'{col} vs graduation_rate')
    plt.ylabel('graduation_rate')
    plt.xlabel(f'{col}')
    plt.legend()
    plt.show()


graph_data(late_df, 'college_career_rate', coeff)
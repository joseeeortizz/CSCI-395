"""
test for assignment1.py
"""

# Section 1: Data loading and exploration

# Task 1.1: Read in the data
raw_df = pd.read_csv("NYCHA_Development_Data_Book_snapshot.csv")

# Task 1.2: Display columns
print(raw_df.columns)

# Task 1.3: Show dataframe head
print(raw_df.head())


# Tasks 1.6 and 1.7: Transform data and create new columns
def read_and_transform_nycha_data(filepath: str) -> pd.DataFrame:
    """Reads and transforms NYCHA data from a CSV file.

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Transformed DataFrame with selected and derived columns.
    """
    raw_df = pd.read_csv(filepath)

    # Process columns
    raw_df["development"] = raw_df["DEVELOPMENT"]
    raw_df["boro"] = raw_df["BOROUGH"]

    # Convert numeric columns
    raw_df["total_pop"] = (
        raw_df["TOTAL POPULATION"]
        .replace(',', '', regex=True)
        .replace('[\$,]', '', regex=True)
        .astype(float)
    )
    raw_df["num_apts"] = (
        raw_df["NUMBER OF CURRENT APARTMENTS"]
        .replace(',', '', regex=True)
        .astype(float)
    )
    raw_df["avg_monthly_rent"] = (
        raw_df["AVG MONTHLY GROSS RENT"]
        .replace('[\$,]', '', regex=True)
        .astype(float)
    )
    raw_df["net_sqft"] = (
        raw_df["NET DEV AREA SQ FT"]
        .replace(',', '', regex=True)
        .astype(float)
    )

    # Compute derived columns
    raw_df['ppl_per_apt'] = raw_df['total_pop'] / raw_df['num_apts']
    raw_df['sqft_per_apt'] = raw_df['net_sqft'] / raw_df['num_apts']
    raw_df['sqft_per_person'] = raw_df['net_sqft'] / raw_df['total_pop']
    raw_df['rent_per_sqft'] = raw_df['avg_monthly_rent'] / raw_df['net_sqft']

    # Select columns
    df = raw_df[[
        "development", "boro", "total_pop", "num_apts",
        "avg_monthly_rent", "net_sqft",
        "ppl_per_apt", "sqft_per_apt", "sqft_per_person", "rent_per_sqft"
    ]]

    return df


# Task 1.9: Load and transform data
nycha_df = read_and_transform_nycha_data("NYCHA_Development_Data_Book_snapshot.csv")
print(nycha_df.head())

# Section 2: Exploratory Data Analysis

# Task 2.1: Summary statistics
print(nycha_df.describe())

# Task 2.3: Pair plots
sns.pairplot(nycha_df)
plt.show()

# Task 2.5: Correlation matrix
print(nycha_df.corr())

# Section 3: Constant Models

# Task 3.1: Histogram of sqft_per_person
sns.displot(nycha_df['sqft_per_person'].dropna(), kde=False)
plt.show()

# Task 3.3: Compute mean and median models
cm_mean = nycha_df['sqft_per_person'].mean()
cm_median = nycha_df['sqft_per_person'].median()
print(f"Mean sqft per person: {cm_mean}")
print(f"Median sqft per person: {cm_median}")


# Task 3.5: Define loss functions
def mae_loss(y_pred, y_true):
    return np.mean(np.abs(y_pred - y_true))


def rmse_loss(y_pred, y_true):
    return np.sqrt(np.mean((y_pred - y_true) ** 2))


# Task 3.6: Compute losses
y_true = nycha_df['sqft_per_person'].dropna()
cm_mean_mae = mae_loss(cm_mean, y_true)
cm_mean_rmse = rmse_loss(cm_mean, y_true)
cm_median_mae = mae_loss(cm_median, y_true)
cm_median_rmse = rmse_loss(cm_median, y_true)

print(f"Mean model MAE: {cm_mean_mae}")
print(f"Mean model RMSE: {cm_mean_rmse}")
print(f"Median model MAE: {cm_median_mae}")
print(f"Median model RMSE: {cm_median_rmse}")


# Task 3.7: Compute losses over thetas
def compute_losses(y_true: pd.Series):
    thetas = np.linspace(0, 1000, 1001)
    mae = [mae_loss(theta, y_true) for theta in thetas]
    rmse = [rmse_loss(theta, y_true) for theta in thetas]
    return pd.DataFrame({'theta': thetas, 'mae': mae, 'rmse': rmse})


losses_df = compute_losses(y_true)
print(losses_df.head())

# Task 3.9: Plot losses
sns.lineplot(x='theta', y='mae', data=losses_df, label='MAE')
sns.lineplot(x='theta', y='rmse', data=losses_df, label='RMSE')
plt.ylabel('loss')
plt.show()

# Task 3.10 and 3.11: Find optimal thetas
min_mae_row = losses_df.loc[losses_df['mae'].idxmin()]
min_rmse_row = losses_df.loc[losses_df['rmse'].idxmin()]

print("Optimal theta for MAE:", min_mae_row)
print("Optimal theta for RMSE:", min_rmse_row)
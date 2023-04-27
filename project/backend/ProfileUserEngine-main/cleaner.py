import parameters
import pandas as pd


def copy_results(df, num_copies):

    for i in range(num_copies):
        df = df.sample(frac=1).reset_index(drop=True)
        df.to_csv('results_long.csv', mode='a', header=False, index=False)

    return df

def results_long(num_copies):
    f = parameters.FILE_NAME
    df = pd.read_csv(f)
    df.to_csv('results_long.csv', mode='w', header=True, index=False)
    df = copy_results(df, num_copies)
    print('Success')


# Create dummy file with 22 * num_copies rows
num_copies = 1000
results_long(num_copies)

# remove duplicates
df = pd.read_csv('results_long.csv')
df = df.drop_duplicates(subset='profile_url', keep="first")

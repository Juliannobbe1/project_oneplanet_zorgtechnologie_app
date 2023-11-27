import pandas as pd
import time
import luigi


# Function to read different types of data files
def read_data(file_path):
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.xml'):
        return pd.read_xml(file_path)
    elif file_path.endswith('.json'):
        return pd.read_json(file_path)
    else:
        print("Unsupported file format.")
        return None


# Function to validate data
def validate_data(data):
    if 'naam' in data.columns and 'prijs' in data.columns:
        if data[['naam', 'prijs']].isnull().values.any():
            print("Invalid data: Missing values found.")
            return False
        else:
            return True
    else:
        print("Invalid data: Required columns not found.")
        return False


# Function to modify data in the data files
def modify_data(data):
    print('before: ', data['prijs'])
    data['prijs'] = data['prijs'] + 100
    print('after: ', data['prijs'])
    return data


# POC for a specific tool
class PerformPOCTask(luigi.Task):
    file_path = luigi.Parameter()

    def requires(self):
        return []

    def output(self):
        return luigi.LocalTarget(self.file_path)

    def run(self):
        # Read the data from the file
        data = read_data(self.file_path)

        if data is not None:
            # Validate the data
            if validate_data(data):
                print("Data validation successful.")

                # Modify the data
                modified_data = modify_data(data)
                print("Data modification successful.")

                # Write the modified data to the output file
                modified_data.to_csv(self.output().path, index=False)
            else:
                print("Data validation failed.")
        else:
            print("Failed to read data from file.")


if __name__ == "__main__":
    # Start timer
    start_time = time.time()

    file_paths = ['python/etl_pipeline/poc/testdata/testproducts.csv',
                  'python/etl_pipeline/poc/testdata/testproducts.json',
                  'python/etl_pipeline/poc/testdata/testproducts.xml']

    tasks = [PerformPOCTask(file_path=path) for path in file_paths]
    luigi.build(tasks, local_scheduler=True)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Elapsed time: {:.2f} seconds".format(elapsed_time))

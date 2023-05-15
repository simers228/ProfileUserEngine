import pandas as pd
import openai
import re
import requests
class FilterClass:
    def __init__(self, data_object, jobPosition, location, jobDescription, domain):
        self.data_object = data_object
        self.jobPosition = jobPosition
        self.location = location
        self.jobDescription = jobDescription
        self.domain = domain
        openai.organization = "org-5jL307O6H0zk9xntse9BR1sl"
        openai.api_key = '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'
        self.df = pd.DataFrame(self.data_object)
    def filter(self):
        def extract_company_name(url):
            company_name = re.findall(r'company/(\w+)', url)
            if company_name:
                return company_name[0]
            return ""
        for index, row in self.df.iterrows():
            for idx, item in enumerate(row['experience']):
                company_name = extract_company_name(item['organisation_profile'])
                del item['organisation_profile']
                
                if idx == 0:
                    item = {'MOST_RECENT_ORGANISATION': company_name, **item}
                else:
                    item['organisation_profile'] = company_name
                
                row['experience'][idx] = item
        self.df['experience'] = self.df['experience'].apply(lambda dicts: [{k: v for k, v in d.items() if (k != 'location' and k!= 'start_time' and k!= 'end_time')} for d in dicts])
        self.df['education'] = self.df['education'].apply(lambda dicts: [{k: v for k, v in d.items() if (k != 'organisation')} for d in dicts])

        if self.location != "":
            df_location = self.df[self.df['location'].str.contains(self.location, case=False)]
        else:
            df_location = self.df
        if df_location.empty:
            print("Empty Dataframe")
            return '0 results'
        df_location_role= df_location[df_location['description'].str.contains(self.jobPosition, case=False)]
        if df_location_role.empty:
            print("Empty Dataframe")
            return '0 results'
        print(self.df)
        print(df_location)
        print(df_location_role)
        def generate_response(row):
            prompt = (f"Background: \nDesc: {row['description']}\nAbout: {row['about']}\nExp: {row['experience']}\nEdu: {row['education']}\n\n"
                    f"Given the background, rate the match for the following job critically:\n\n{self.jobDescription}\n\n"
                    f"Rate the match using a score out of 10, considering the most important qualifications and requirements. Please be critical in your evaluation. "
                    f"Format your response as 'Match Score: X/10': ")

            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=50,
                n=1,
                stop=None,
                temperature=0.8,  # Adjust the temperature value
            )
            response_text = response.choices[0].text.strip()
            match = re.search(r"Match Score: (\d+(\.\d+)?)/10", response_text)
            if match:
                score = float(match.group(1))  # Change this line
            else:
                score = None
            return score

        # Generate scores and create a new column with the scores
        df_location_role["score"] = df_location_role.apply(lambda row: generate_response(row), axis=1)
        sorted_df = df_location_role.sort_values(by='score', ascending=False)
        filtered_df = sorted_df[sorted_df['score'] >= 8]
        print(filtered_df)
        # Split the full_name column into first_name and last_name
        filtered_df[['first_name', 'last_name']] = self.df['name'].str.split(' ', n=1, expand=True)
        columns = filtered_df.columns.tolist()

        # Find the index of the 'full_name' column
        full_name_index = columns.index('name')

        # Reorder the columns toa place first_name and last_name to the left of full_name
        new_columns = columns[:full_name_index] + columns[-2:] + columns[full_name_index:-2]
        filtered_df = filtered_df[new_columns]
        filtered_df['email'] = None
        filtered_df_10= filtered_df.head(10)
        # Function to find the email address using the hunter.io API
        def find_email(row):
            url = 'https://api.hunter.io/v2/email-finder'
            params = {
                'domain': self.domain,
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'api_key': 'c07cbe91891dc8eab36fe2b00b8be21b0a474319',  # Replace with your actual API key
            }
            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                return data['data']['email']
            else:
                print(f'Request failed with status code {response.status_code}: {response.text}')
                return None

        # Apply the function to each row in the DataFrame
        filtered_df_10['email'] = filtered_df_10.apply(find_email, axis=1)

        # Display the updated DataFrame
        filtered_df_10
        def verify_email_sample(email):
            url = 'https://api.hunter.io/v2/email-verifier'
            params = {
                'api_key': 'c07cbe91891dc8eab36fe2b00b8be21b0a474319',  # Replace with your actual API key
                'email': email
            }
            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                return data['data']['result']
            else:
                print(f'Request failed with status code {response.status_code}: {response.text}')
                return None

        # Apply the functions to each row in the DataFrame
        filtered_df_10['email_verification'] = filtered_df_10['email'].apply(verify_email_sample)
        filtered_df_10
        def extract_domain(email):
            if email is None:
                return None

            match = re.match(r'[^\s@]+@([^\s@]+\.[^\s@]+)', email)
            if match:
                return match.group(1)
            else:
                return None

        # Extract domain from the existing emails
        filtered_df_10['domain'] = filtered_df_10['email'].map(extract_domain)

        # Determine the most common domain
        mode_domains = filtered_df_10['domain'].mode()

        if not mode_domains.empty:
            most_common_domain = mode_domains.iloc[0]
        else:
            most_common_domain = 'example.com'  # Use a default domain if there's no mode

        # Function to fill in missing emails using the pattern
        def fill_missing_email(row):
            if row['email'] is None:
                first_name, last_name = row['first_name'], row['last_name']

                # Split the last name into parts
                last_name_parts = last_name.split(' ')

                # Check if the last name has only one character or more than two parts
                if len(last_name_parts[0]) <= 1 or len(last_name_parts) >= 2:
                    return None

                # Extract the first part of the last name
                first_part_of_last_name = last_name_parts[0]

                email_pattern = f'{first_name}.{first_part_of_last_name}'
                return f'{email_pattern}@{most_common_domain}'.lower()  # Ensure the generated email is lowercase
            else:
                return row['email']
            
        # Fill in the missing emails in filtered_df
        filtered_df['email'] = filtered_df.apply(fill_missing_email, axis=1)

        # Convert all emails in filtered_df to lowercase
        filtered_df['email'] = filtered_df['email'].str.lower()

        # Drop the unnecessary columns from filtered_df_10
        filtered_df_10 = filtered_df_10.drop(columns=['domain'])

        # Display the updated DataFrames
        filtered_df	
        filtered_df['email'] = filtered_df['email'].str.strip()
        def verify_email(email):
            url = 'https://api.hunter.io/v2/email-verifier'
            params = {
                'api_key': 'c07cbe91891dc8eab36fe2b00b8be21b0a474319',  # Replace with your actual API key
                'email': email
            }
            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                return data['data']['result']
            else:
                print(f'Request failed with status code {response.status_code}: {response.text}')
                return None

        # Apply the functions to each row in the DataFrame
        filtered_df['email_verification'] = filtered_df['email'].apply(verify_email)
        filtered_df
        def generate_email(row, job_desc):
            prompt = (f"Background:\nName: {row['name']}\nDesc: {row['description']}\nAbout: {row['about']}\nExp: {row['experience']}\nEdu: {row['education']}\n\n"
                    f"Using the candidate's background and {job_desc}, compose an email from recruiter Simer Singh at Sequoia Recruitment Partners. The role is based in the Greater Omaha area. Do not mention the name of the company or client in the email. Use a slightly informal language style. In the email, emphasize the benefits of the role and explain why the client is a good fit for the candidate. Please avoid using any placeholder information.\n\n")
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=300,
                n=1,
                stop=None,
                temperature=0.8,  # Adjust the temperature value
            )
            response_text = response.choices[0].text.strip()

            return response_text

        # Generate emails and create a new column with the emails
        filtered_df["email"] = filtered_df.apply(lambda row: generate_email(row, self.jobDescription), axis=1)
        return filtered_df
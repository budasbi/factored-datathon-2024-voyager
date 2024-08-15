# %%
import requests
from bs4 import BeautifulSoup
import boto3

url = "https://data.gdeltproject.org/events/index.html"
s3_bucket_name = 'factored-datathon-2024-voyager-test'  
s3_region = 'us-east-1'   

# %%
# Get the file list to download
response = requests.get(url, verify=False)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    a_elements = soup.find_all('a')

    links = [a.get('href') for a in a_elements if a.get('href')]

else:
    print(f"Error al obtener la página: {response.status_code}")



# %%
curated_links = [file for file in links if file.startswith('202')]

# %%
filtered_by_date = [file for file in curated_links if int(file[0:8])>20230812]

# %%
link_list = list(map(lambda x: url.replace('index.html','')+x, filtered_by_date  ))

# %%
filename = link_list[0].split('/')[-1]

# %%
for file in link_list:
    file_response = requests.get(file, verify=False)
    print(file)
    year = str(filename[0:4])
    month = str(filename[4:6])
    day = str(filename[6:8])
    print(year)
    print(month)
    print(day)
    if response.status_code == 200:
        file_content = file_response.content
        filename = file.split('/')[-1]
        
    s3 = boto3.client('s3', region_name=s3_region)
    s3.put_object(Bucket=s3_bucket_name, Key=f'raw/year={year}/month={month}/day={day}/{filename}', Body=file_content)




# Imports
import requests
from requests.auth import HTTPBasicAuth

import os
import json
import base64

import dotenv

class Mushroom_API_Request:
    
    dotenv.load_dotenv()
    api_key = os.getenv('MUSHROOM-API-KEY')
    
    url = 'https://mushroom.kindwise.com/api/v1/'
    headers = {
        'Content-Type': 'application/json',
        'Api-Key': api_key
    }
    
    def __init__(self, longitude_latitude=(0.0, 0.0)):
        
        self._longitude_latitude=longitude_latitude
        # Access token used for getting request detail
        self._id_access_token=''
        self._search_access_tokens=[]
        
    
    def create_identification(self, image_path):
        
        images = []
        
        # Encode image files as base64
        for path in os.listdir(image_path):
            
            filename = image_path + os.fsdecode(path)
            
            if filename.endswith(".jpg") or filename.endswith(".jpeg"): 
                with open(filename, 'rb') as image_file:
                    encoded_img = base64.b64encode(image_file.read())
                    # Append with image request format
                    images.append(f"data:image/jpeg;base64,{encoded_img.decode('utf-8')}",)

        # Create payload
        payload = json.dumps({
                "images": images,
                "latitude": self._longitude_latitude[0],
                "longitude": self._longitude_latitude[1]
                })
        
        id_url = f'{self.url}identification'
        
        # Make request
        try:
            response = requests.post(id_url, headers=self.headers, data=payload)
            response.raise_for_status()
        except requests.HTTPError as ex:
            # possibly check response for a message
            raise ex  # let the caller handle it
            return False
        except requests.Timeout:
            # request took too long
            return False
        
        self._id_access_token = json.loads(response.content)["access_token"]
        
        return True
        
        
    def retrieve_ID_data(self, details=''):
        print("In function", self._id_access_token)
        id_url = f'{self.url}identification/{self._id_access_token}?details={details}'
        try:
            response = requests.get(id_url, headers=self.headers)
            response.raise_for_status()
        except requests.HTTPError as ex:
            # possibly check response for a message
            raise ex  # let the caller handle it
            return False
        except requests.Timeout:
            # request took too long
            return False
        
        data = json.loads(response.content)
        
        return data
    
    
    def search_request(self, query):
        
        query_url = f'{self.url}kb/mushroom/name_search?q={query}'
        
        try:
            response = requests.get(query_url, headers=self.headers)
            response.raise_for_status()
        except requests.HTTPError as ex:
            # possibly check response for a message
            raise ex  # let the caller handle it
            return False
        except requests.Timeout:
            # request took too long
            return False
        
        self.set_search_access_tokens([entities["access_token"] for entities in json.loads(response.content)["entities"]])
        
        return True
    
    
    def retrieve_mushroom_detail(self, access_token, details=''):
        query_url = f'{self.url}kb/mushroom/{access_token}?details={details}'
        try:
            response = requests.get(query_url, headers=self.headers)
            response.raise_for_status()
        except requests.HTTPError as ex:
            # possibly check response for a message
            raise ex  # let the caller handle it
            return False
        except requests.Timeout:
            # request took too long
            return False
        
        data = json.loads(response.content)
        return data
    
    
    def retrieve_search_results(self, details=''):
        results = []
        for access_token in self._search_access_tokens:
            results.append(self.retrieve_mushroom_detail(access_token, details))
            
        return results
            
        
    
    '''
    Getters and Setters
    '''
    def set_details(self, details=''):
        old_details = self._details
        self._details = self._details
        return old_details
    
    def get_details(self):
        return self._details
    
    def set_long_lat(self, longitude_latitude):
        old_long_lat = self._longitude_latitude
        self._longitude_latitude = longitude_latitude
        return old_long_lat
    
    def get_long_lat(self):
        return self._longitude_latitude
    
    def set_id_access_token(self, access_token):
        old_id_access_token = self._id_access_token
        self._id_access_token = access_token
        return old_id_access_token
    
    def get_id_access_token(self):
        return self._id_access_token
    
    def set_search_access_tokens(self, access_tokens):
        old_search_access_tokens = self._search_access_tokens
        self._search_access_tokens = access_tokens
        return old_search_access_tokens
    
    def get_search_access_tokens(self):
        return self._search_access_tokens
    
    
all_details = 'common_names,url,description,edibility,psychoactive,characteristic,look_alike,taxonomy,rank,gbif_id,inaturalist_id,image,images'
details = 'common_names,url,description,edibility,psychoactive,characteristic,image'

if __name__ == "__main__":
    
    m = Mushroom_API_Request((0.0, 0.0))
    m.create_identification("./sample/")
    response = m.retrieve_ID_data(details=details)
    print(json.dumps(response, indent=2))
    
    with open("response.txt", 'w') as response_file:
        response_file.write(json.dumps(response, indent=2))
    
import requests
import json
import getpass  
import os
from datetime import datetime, timedelta, timezone
import json
import sys

def obtain_api_token(defectdojo_base_url, username, cred):
    url = f"{defectdojo_base_url}/api/v2/api-token-auth/"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "username": username,
        "password": cred
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        token = response.json().get("token")
        return token
    else:
        print(f"Failed to obtain API token. Status code: {response.status_code}")
        print(response.text)
        return None

def create_product(defectdojo_base_url, api_key, product_name):
    url = f"{defectdojo_base_url}/api/v2/products/"
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "name": product_name,
        "prod_type": 1, 
        "description": "product_name"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print(f"Product '{product_name}' created successfully.")
        return response.json().get("id")
    else:
        print(f"Failed to create product. Status code: {response.status_code}")
        print(response.text)
        return None

def check_product_exists(defectdojo_base_url, api_key, product_name):
    url = f"{defectdojo_base_url}/api/v2/products/"
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        products = response.json().get("results", [])
        for product in products:
            if product["name"] == product_name:
                print(f"Products Already Exist. Status code: {response.status_code}")
                return True
        return False
    else:
        print(f"Failed to fetch products. Status code: {response.status_code}")
        print(response.text)
        return False

 
def upload_scan(defectdojo_base_url, username,cred, scan_file_path, product_name, engagement_name, scan_type,api_key):
    #api_key = obtain_api_token(defectdojo_base_url, username, cred)
    if api_key:
        print(f"API token obtained: {api_key}")

        url = f"{defectdojo_base_url}/api/v2/import-scan/"

        headers = {
            "Authorization": f"Token {api_key}",
        }

        data = {
            "product_name": product_name,
            "engagement_name": engagement_name,
            "scan_type": scan_type
        }
        #print("__________Before File read________________") 
        with open(scan_file_path, "rb") as file:
           
            files = {"file": (scan_file_path, file, "application/json")}
            #print("__________Before File post____________")
            response = requests.post(url, headers=headers, data=data, files=files)
            #print("__________Afer  post____________")
        if response.status_code == 201:
            print("Scan uploaded successfully.")
        else:
            print(f"Failed to upload scan. Status code: {response.status_code}")
            print("Full Respose =",response.text)
    else:
        print("Failed to obtain API token.")
        
def create_engagement(defectdojo_base_url, api_key, product_id, engagement_name):
  url = f"{defectdojo_base_url}/api/v2/engagements/"
  target_start = datetime.utcnow().strftime("%Y-%m-%d")
  target_end = (datetime.utcnow() + timedelta(weeks=2)).strftime("%Y-%m-%d")
  headers = {
      "Authorization": f"Token {api_key}",
      "Content-Type": "application/json"
  }
  data = {
      "product": product_id,
      "name": engagement_name,
      "deduplication_on_engagement":	True,
      "target_start": target_start,
      "target_end": target_end
  }

  response = requests.post(url, headers=headers, json=data)

  if response.status_code == 201:
      print(f"Engagement '{engagement_name}' created successfully.")
      return response.json().get("id")
  else:
      print(f"Failed to create engagement. Status code: {response.status_code}")
      print(response.text)
      return None


def add_test_to_engagement(defectdojo_base_url, api_key, engagement_id, test_name, test_type):
  url = f"{defectdojo_base_url}/api/v2/tests/"
  target_start = datetime.utcnow().strftime("%Y-%m-%d")
  target_end = (datetime.utcnow() + timedelta(weeks=2)).strftime("%Y-%m-%d")
  headers = {
    "Authorization": f"Token {api_key}",
    "Content-Type": "application/json"
      }
  data = {
      "engagement": engagement_id,
      "name": test_name,
      "test_type": test_type,
      "target_start": target_start,
      "target_end": target_end
     
  }

  response = requests.post(url, headers=headers, json=data)

  if response.status_code == 201:
      print(f"Test '{test_name}' added to engagement successfully.")
  else:
      print(f"Failed to add test to engagement. Status code: {response.status_code}")
      print(response.text)


def create_or_get_product_and_engagement(defectdojo_base_url, api_key, product_name, engagement_name, test_name, test_type):
        product_id = get_or_create_product(defectdojo_base_url, api_key, product_name)
        if product_id:
          engagement_id = get_or_create_engagement(defectdojo_base_url, api_key, product_id, engagement_name)
          if engagement_id:
            add_test_to_engagement(defectdojo_base_url, api_key, engagement_id, test_name, test_type)

def get_or_create_product(defectdojo_base_url, api_key, product_name):
        product_exists = check_product_exists(defectdojo_base_url, api_key, product_name)
        if not product_exists:
            product_id = create_product(defectdojo_base_url, api_key, product_name)
            print("Product created. Product ID:", product_id)
        else:
            product_id = get_product_id(defectdojo_base_url, api_key, product_name)
            print("Product already exists. Product ID:", product_id)
        return product_id

def get_or_create_engagement(defectdojo_base_url, api_key, product_id, engagement_name):
    engagement_exists = check_engagement_exists(defectdojo_base_url, api_key, product_id, engagement_name)
    if not engagement_exists:
      engagement_id = create_engagement(defectdojo_base_url, api_key, product_id, engagement_name)
      print("Engagement created. Engagement ID:", engagement_id)
    else:
      engagement_id = get_engagement_id(defectdojo_base_url, api_key, product_id, engagement_name)
      print("Engagement already exists. Engagement ID:", engagement_id)
    return engagement_id

def check_engagement_exists(defectdojo_base_url, api_key, product_id, engagement_name):
    url = f"{defectdojo_base_url}/api/v2/engagements/"
    headers = {
      "Authorization": f"Token {api_key}",
      "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      engagements = response.json().get("results", [])
      for engagement in engagements:
        if engagement["name"] == engagement_name and engagement["product"] == product_id:
          print(f"Engagement '{engagement_name}' already exists.")
          return True
      return False
    else:
      print(f"Failed to fetch engagements. Status code: {response.status_code}")
      print(response.text)
      return False


def get_product_id(defectdojo_base_url, api_key, product_name):
  url = f"{defectdojo_base_url}/api/v2/products/"
  headers = {
      "Authorization": f"Token {api_key}",
      "Content-Type": "application/json",
  }

  response = requests.get(url, headers=headers)

  if response.status_code == 200:
      products = response.json().get("results", [])
      for product in products:
          if product["name"] == product_name:
              return product["id"]
      return None
  else:
      print(f"Failed to fetch products. Status code: {response.status_code}")
      print(response.text)
      return None

def get_engagement_id(defectdojo_base_url, api_key, product_id, engagement_name):
  url = f"{defectdojo_base_url}/api/v2/engagements/"
  headers = {
      "Authorization": f"Token {api_key}",
      "Content-Type": "application/json",
  }

  response = requests.get(url, headers=headers)

  if response.status_code == 200:
      engagements = response.json().get("results", [])
      for engagement in engagements:
          if engagement["name"] == engagement_name and engagement["product"] == product_id:
              return engagement["id"]
      return None
  else:
      print(f"Failed to fetch engagements. Status code: {response.status_code}")
      print(response.text)
      return None


def check_json_severity(json_data):
    if "severity" in json_data and json_data["severity"].lower() in ["critical", "high"]:
        return True, json_data.get('name', 'Unknown Issue')

    for key, value in json_data.items():
        if isinstance(value, dict):
            result, issue_name = check_json_severity(value)
            if result:
                return result, issue_name

        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    result, issue_name = check_json_severity(item)
                    if result:
                        return result, issue_name
    return False, None

if __name__ == "__main__":
    
    
    if len(sys.argv) != 8:
        print("Usage: python defectdojo_integration.py <defectdojo_base_url> <username> <cred> <product_name> <engagement_names> <scan_types> <scan_file_paths>")
        #sys.exit(1)

    defectdojo_base_url, username, cred, product_name, engagement_names, scan_types, scan_file_paths = sys.argv[1:8]
    # Print debugging information 


    defectdojo_base_url = os.getenv("DEFECTDOJO_BASE_URL")
    username = os.getenv("DEFECTDOJO_USERNAME")
    cred = os.getenv("DEFECTDOJO_CRED")

    # Convert comma-separated strings to lists
    product_name = product_name.split(',')
    engagement_names = engagement_names.split(',')
    scan_types = scan_types.split(',')
    scan_file_paths = scan_file_paths.split(',') 

    print("defectdojo_base_url:", defectdojo_base_url)
    print("username:", username)
    print("cred:", cred)
    print("product_name:", product_name)
    print("engagement_names:", engagement_names)
    print("scan_types:", scan_types)
    print("scan_file_paths:", scan_file_paths)
    
    defectdojo_base_url = "http://54.170.174.80:8080/"
    username = "admin" 
    cred = "DevSecOps@24"
    product_name = "CoffeeShop_GitHub"
    # api_key = obtain_api_token(defectdojo_base_url, username, cred)
    # engagement_names = ["Snyk"]
    # scan_types = ["Snyk Scan"]
    # scan_file_paths = ["/home/runner/work/DevSecOps/DevSecOps/snyk-artifact/snyk-report.json"]
    api_key = obtain_api_token(defectdojo_base_url, username, cred)
    if api_key:
        print(f"API token obtained: {api_key}")
        for i in range(len(engagement_names)):
          create_or_get_product_and_engagement(defectdojo_base_url, api_key, product_name, engagement_names[i], engagement_names[i], scan_types[i])
    else:
        print("Failed to obtain API token.")

    
    for i in range(len(engagement_names)):
      print("__________________________________====____________________________________________",scan_file_paths[i])
      upload_scan(
          defectdojo_base_url,
          username,
          cred,
          scan_file_paths[i],
          product_name,
          engagement_names[i],
          scan_types[i],
          api_key
      )

      # Check for critical or high-severity issues in the uploaded scan report
      try:
        with open(scan_file_paths[i], 'r') as file:
          json_data = json.load(file)
      except FileNotFoundError:
        print(f"Error: File not found - {scan_file_paths[i]}")
        #sys.exit(1)
      except json.JSONDecodeError:
          print(f"Error: Invalid JSON format in file - {scan_file_paths[i]}")
          #sys.exit(1)

      has_critical_or_high_severity, issue_title = check_json_severity(json_data)

      if has_critical_or_high_severity:
          print(f"Build failed due to critical or high severity issue in {engagement_names[i]} scan:")
          print(f"Issue Title: {issue_title}")
          sys.exit(1)
      else:
          print(f"{engagement_names[i]} scan passed. No critical or high severity issues found.")    

# content of test_sysexit.py
import pytest
import requests
import logging
import json

invalid_user_id=123
user_id=3360
update_success_code_list=[200,204]
delete_success_code_list=[200,202,204]
UsersURL="https://gorest.co.in/public-api/users"
new_user= {'name':'Mono1235','email':'Hello2@hacett.com','gender':'female','status':'active'}
element= {'name':'Ghorbel123','email':'Hello1@hacett.fr','gender':'female','status':'unactive'}
my_headers = {'Authorization' : 'Bearer fa5ba154859da3b436a7a416571fc579ca8413aa828afa6b14522098fa810af4'}

logging.basicConfig(filename='Syslog.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('This message will get logged on to a file')

def GetNoeudElements(URL):
     res = requests.get(str(URL))
     print("All availble lists in Noeud:\t"+str(URL)+"\n")
     print("Nbr of Elements availble is:\t"+str(len(res.json()["data"])))
     for x in res.json()["data"]:
          print(x)
     return res

def GetNoeudElementsByID(URL,ID):
     url=str(URL)+"/"+str(ID)
     print("The Element with ID equal to\t"+str(ID)+"\t is: \n")
     res = requests.get(url)
     print(res)
     print(res.json())
     print(res.content)
     return res

def AddElement(URL,Element,Auth):
     """ Create new Element """
     post_response = requests.post(str(URL), data = Element, headers=Auth)
     print(post_response)
     print(post_response.json())
     print(post_response.content)
     return post_response

def DeleteElement(URL,ID,Auth):
     """ Delete Element """
     url=str(URL)+"/"+str(ID)
     delete_response = requests.delete(url, headers=Auth)
     print(delete_response)
     print(delete_response.json())
     print(delete_response.content)
     return delete_response

def UpdateElement(URL,ID,Element,Auth):
     """ Update Element """
     response = GetNoeudElementsByID(URL,ID)
     Json = response.json()
     if Json["code"] == 200:
          logging.warning("The User ID\t"+ str(ID) +"passed in argument is Valid")
          logging.warning("User old content is \t"+ str(response.json()))
          new_url=str(URL)+"/"+str(ID)
          res=requests.put(new_url, data = Element, headers=Auth)
          if res.json()["code"] in update_success_code_list:
               logging.warning("User New content is \t"+ str(res.json()))
     return res
     
def test_get_all_users():
     response=GetNoeudElements(UsersURL)
     logging.warning(response.content)
     assert response.status_code == 200

def test_get_user_by_id():
     response = GetNoeudElementsByID(UsersURL,user_id)
     Json = response.json()
     logging.warning(Json)
     assert Json["code"] == 200

def test_get_user_with_fake_id():
     response = GetNoeudElementsByID(UsersURL,invalid_user_id)
     Json = response.json()
     logging.warning(Json)
     assert Json["code"] == 404     

def test_post_user():
     res=AddElement(UsersURL,new_user,my_headers)
     Json = res.json()
     if Json["code"] == 201:
          logging.warning("User added with success:"+str(Json))
     else:
          logging.warning("Unexpeted issue faced while adding user:"+str(Json))

     assert Json["code"] == 201   

def test_put_user():
     res=UpdateElement(UsersURL,user_id,element,my_headers)
     Json = res.json()
     assert Json["code"] in update_success_code_list

def test_delete_user():
     res=DeleteElement(UsersURL,user_id,my_headers)
     Json = res.json()
     assert Json["code"] in delete_success_code_list



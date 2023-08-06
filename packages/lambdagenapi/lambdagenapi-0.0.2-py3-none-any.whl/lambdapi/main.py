#https://api.community.lambdageneration.com/api/accounts/signin
#https://api.community.lambdageneration.com/api/hives/631f63ff1d4837c1fe3892b6/posts
#https://api.community.lambdageneration.com/api/posts/63cec00acc0c623f74f5c2f4/favoritepost


#b'{"success":true,"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwZGI0NmE5ZjY2NzA5M2FkZWFkOTM0OCIsInBlcnNvbmEiOiI2MGRiNDZhOWY2NjcwOTIzNWJhZDkzNDkiLCJpYXQiOjE2NzQ0OTMzMzAsImlzcyI6Imh0dHBzOi8vY29tbXVuaXR5LmxhbWJkYWdlbmVyYXRpb24uY29tIn0.iFFQ5WQU1uog6r8cGamtef9wRK12D7eZdTREmrYjdq0","account":{"_id":"60db46a9f667093adead9348","email":"lamba@felix-p.com","creationTime":"2021-06-29T16:13:29.478Z","prefFilterSensitiveContent":true,"personas":[{"hivesList":[{"_id":"631f649e1d483785e13892b9","displayName":"Black Mesa","hiveId":"doe0fggchqef","avatar":"https://media.cdn.community.lambdageneration.com/avatars/1663001799988DLCWBqFBCCbDfCAB.png","color":"3","customId":"black-mesa"},{"_id":"63cb0a7856521774c31bd220","displayName":"Entropy : Zero","hiveId":"g6dfsc4fzdje","avatar":"https://media.cdn.community.lambdageneration.com/avatars/1674334742654CdD5CBD15CtDUDND.png","color":"20","customId":"entropyzero"}],"followedPersonas":["6109760e715e9869081eda7f","6137dc17d8e2821faa920759","60bf229eab387b64b9b673e8"],"_id":"60db46a9f66709235bad9349","displayName":"zhuz","personaId":"dbjghceyd2by","customId":"zhuz","hivesJoinedCount":3,"avatar":"https://media.cdn.community.lambdageneration.com/avatars-default/shephard-op4.jpg","color":7}],"emailNotificationSettings":{"responsesPosts":true,"responsesResponses":true},"defaultPersona":"60db46a9f66709235bad9349"}}'

# These are Hives, basically the backend name of the catagories

# half-life - "60bba930a54990cba2a445c8"
# portal - "631f62061d4837f44b3892ac"
# tf2 - "631f62df1d483792cb3892b0"
# sfm - "631f65831d4837f2183892bc"
# valve - "631f63811d4837e3d03892b3"
# black mesa - "631f649e1d483785e13892b9"
# lambdagen - "631f63ff1d4837c1fe3892b6"
# sven-coop - "631f65b01d483794713892bf"
# entropy-zero - "63cb0a7856521774c31bd220"

# this would make a request to thhe 

#https://api.community.lambdageneration.com/api/hives/60bba930a54990cba2a445c8/posts
#https://api.community.lambdageneration.com/api/personas/60db46a9f66709235bad9349


#{
#  "reactionsCount": 0,
#  "authorReactionsCount": 0,
#  "responsesCount": 0,
#  "authorResponsesCount": 0,
#  "_id": "63ceddeecc0c62f2bbf5c3cf",
#  "author": "60db46a9f66709235bad9349",
# "hive": "60bba930a54990cba2a445c8",
# "sensitive": false,
# "text": "what if the real freeman, was the friends we made along the way",
# "tags": [],
# "creationTime": "2023-01-23T19:20:14.298Z",
# "reposts": [],
# "postId": "dgrcpgyf",
# "__v": 0
#}

import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

class LambdaGen:
    def __init__(self, mail, password):
        self.s = requests.Session()
        self.login(mail, password)

    def login(mail, password):
        s = requests.Session()
        payload = {
            'email': mail,
            'password': password
        }
        res = s.post('https://api.community.lambdageneration.com/api/accounts/signin', json=payload)
        response_content = json.loads(res.content)
        s.token = response_content["token"]
        s.default_persona = response_content["account"]["defaultPersona"]
        s.headers.update({'authorization': s.token})
        print(s.default_persona)
        print(s.token)

    def update_persona(self, updatedFields):
        headers = {"authorization": "Bearer " + self.s.token}
        form_data = {'updatedFields': json.dumps(updatedFields)}
        try:
            r = self.s.patch('https://api.community.lambdageneration.com/api/personas/' + self.s.default_persona,headers=headers, json=form_data)
            r.raise_for_status()
            return r.content
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("Something Else:",err)

    def post_message(self, text, hive):
        if hive == 'half-life':
            hive_id = '60bba930a54990cba2a445c8'
        elif hive == 'portal':
            hive_id = '631f62061d4837f44b3892ac'
        elif hive == 'tf2':
            hive_id = '631f62df1d483792cb3892b0'
        elif hive == 'sfm':
            hive_id = '631f65831d4837f2183892bc'
        elif hive == 'valve':
            hive_id = '631f63811d4837e3d03892b3'
        elif hive == 'black-mesa':
            hive_id = '631f649e1d483785e13892b9'
        elif hive == 'lambdagen':
            hive_id = '631f63ff1d4837c1fe3892b6'
        elif hive == 'sven-coop':
            hive_id = '631f65b01d483794713892bf'
        elif hive == 'entropy-zero':
            hive_id = '63cb0a7856521774c31bd220'
        else:
            raise ValueError(f"Invalid hive name: {hive}")

        form_data = {'text': text}
        multipart_data = MultipartEncoder(fields=form_data)
        headers = {'Content-Type': multipart_data.content_type, "Authorization": "Bearer " + self.token}

        session = requests.Session()
        try:
            response = session.post(f'https://api.community.lambdageneration.com/api/hives/{hive_id}/posts', data=multipart_data, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print(f'HTTP error occurred: {error}')
        except requests.exceptions.ConnectionError as error:
            print(f'Error connecting: {error}')
        except requests.exceptions.Timeout as error:
            print(f'Timeout error: {error}')
        except requests.exceptions.RequestException as error:
            print(f'Something else went wrong: {error}')
        else:
            print(response.content)

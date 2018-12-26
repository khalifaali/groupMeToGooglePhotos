import requests
import json


class Gm_Parser:
    url = "https://api.groupme.com/v3"
    groups_url = url + '/groups'
    # messages_url = url +
    group_params = {'per_page': '6'}
    message_params = {'limit': '100', 'before_id': None}

    def __init__(self, token, user_agent):
        access_token = ''.join((i if ord(i) < 10000 else '\ufffd' for i in token))

        self.header = {'User-Agent': user_agent,
                       'Host': 'api.groupme.com',
                       'Accept': '*/*',
                       'X-Access-Token': access_token}

        self.group_ids = []
        self.message_results = dict
        self.oldest_message_id = None
        self.message_url = None

        # create these in the initialization

    def request(self, target_url, target_params=None):
        if target_params is None:
            target_params = self.group_params
        result = requests.get(url=target_url,
                              headers=self.header,
                              params=target_params)

        return result.json()['response']

    def get_groups(self):

        result = self.request(self.groups_url)

        for index in range(len(result)):
            self.group_ids.append({'name': result[index]['name'], 'id': result[index]['id']})

    '''
        for index in range(len(result)):
            # create new group ids that can be used later to save Name_of_Group : Group_Id
            result_group_ids = {}
            # make group selection easier on the user we can create a dictionary that uses group index to retrieve group
            #   id, and name

            result_group_ids[result[index]['name']] = result[index]['id']
            self.group_ids.append(result_group_ids)
'''

    def print_groups(self):

        if len(self.group_ids) == 0:
            return 'Group ids are empty please run get_groups method'
        for group in self.group_ids:
            print(group)

        # choose group

    def select_group_messages(self):
        if len(self.group_ids) == 0:
            return 'groups are empty'

        print('Which Group Messages Would you like to see? \n')
        for index, value in enumerate(self.group_ids):
            print("Choice: ", index, " GroupChat ", value)

        choice = int(input('\n Select the appropriate index...'))
        group_message = self.group_ids[choice]

        print('Selected Group chat is ', group_message['name'])

        self.message_url = self.url + '/groups/' + group_message['id'] + '/messages'
        messages = self.request(self.message_url, target_params=self.message_params)
        self.message_params['before_id'] = messages['messages'][0]['id']

    def load_group_messages(self):
        chat_log = self.request(self.message_url, target_params=self.message_params)
        k = 0
        while (k < 6):
            # retrieve everything before the most recent message in the set
            # investigate the messages that are being ommitted
            # print message before issuing the new request
            oldest_message_id = self.message_params['before_id']

            print(json.dumps(chat_log['messages'][0]['text']))

            self.message_params['before_id'] = chat_log['messages'][0]['id']

            print(json.dumps(chat_log['messages'][0]['text']))
            chat_log = self.request(self.message_url, target_params=self.message_params)
            for message_index, message_text in enumerate(chat_log['messages'][:-1]):
                if len(message_text['attachments']) > 0 \
                        and message_text['attachments'][0]['type'] == 'image':
                    print('IMAGE FOUND!!')
                    print(json.dumps(message_text['text']))
                    print('IMAGE URL: ', message_text['attachments'][0]['url'])

import requests, json, urllib.request, os


class Gm_Parser:
    url = "https://api.groupme.com/v3"
    groups_url = url + '/groups'
    # messages_url = url +
    group_params = {'per_page': '6'}
    message_params = {'limit': '100', 'before_id': None}

    def __init__(self, token):
        access_token = ''.join((i if ord(i) < 10000 else '\ufffd' for i in token))

        self.header = {'User-Agent': 'bot',
                       'Host': 'api.groupme.com',
                       'Accept': '*/*',
                       'X-Access-Token': access_token}

        self.group_ids = []
        self.message_results = dict
        self.oldest_message_id = None
        self.message_url = None
        self.selected_group_name = None

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
        self.selected_group_name = group_message['name']

    def load_group_messages(self, txts_per_page=None):

        if txts_per_page is None or txts_per_page < '0' or txts_per_page > '100':
            txts_per_page = '100'

        self.message_params['limit'] = txts_per_page

        '''
         We need to set a variable so that we can refresh the page with an  certain amount of 
         messages without intervention
         
         we may be able to solve this by using an optional argument  
        '''

        chat_log = self.request(self.message_url, target_params=self.message_params)

        # while text_loads < 2:
        # retrieve everything before the most recent message in the set
        # investigate the messages that are being ommitted
        # print message before issuing the new request
        # print(json.dumps(chat_log['messages'][0]['text']))

        self.message_params['before_id'] = chat_log['messages'][0]['id']
        # print(json.dumps(chat_log['messages'][0]['text']))
        cwd = os.getcwd()
        try:
            save_folder = cwd + '\\' + self.selected_group_name
            os.mkdir(save_folder)
        except FileExistsError:
            # if we can't create the folder then we know it already exists
            save_folder = cwd + '\\' + self.selected_group_name

        for message_index, message_text in enumerate(chat_log['messages'][:-1]):
            print(json.dumps(message_text['text']))
            if len(message_text['attachments']) > 0 \
                    and message_text['attachments'][0]['type'] == 'image':
                phrase = json.dumps(message_text['text'])

                phrase_id = message_text['id']
                image_url = message_text['attachments'][0]['url']
                # save_folder = '\\Pictures\\'
                # phrase id is a particular text id
                # urllib.request.retrieve will save the remote file for us
                save_file = save_folder + '\\jpeg' + str(phrase_id) + '.jpeg'
                urllib.request.urlretrieve(image_url, filename=save_file)
                print('text: ', phrase, 'image url: ', image_url)


        self.message_params['before_id'] = chat_log['messages'][-1]['id']

import requests, json, urllib.request, os, re

'''
Per GroupMe API documentation
List the authenticated user's active groups.
page defualts to 1


The response is paginated, with a default of 10 groups per_page.

example
{page:1,per_page:10}

'''


class Gm_Parser:
    url = "https://api.groupme.com/v3"
    groups_url = url + '/groups'
    # messages_url = url +
    group_params = {'per_page': '10'}
    # group response is paginated with a default of 10, no max was given in GroupMe API documentation
    # GroupMe Default message limit is 20 . The max is 100. I use the max in the script
    # NOTE this message limit is used to control how many messages are pulled back
    # the messages will be displayed using load_group_messages()

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
        self.limit_for_pictures = None
        self.amount_pictures_seen = 0

        # create these in the initialization

    def set_pix_limit(self, amount):
        self.limit_for_pictures = amount

    def increment_amount_pix_seen(self):
        self.amount_pictures_seen += 1

    def is_pix_limit_met(self):
        return self.amount_pictures_seen == self.limit_for_pictures

    def set_groups_per_page(self, amount):
        if amount == -1:
            self.group_params['per_page'] = ''
        else:
            self.group_params['per_page'] = str(amount)

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
            self.group_ids[index]['name'] = self.scrub_filename(self.group_ids[index]['name'])

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
            print(group['name'])

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

    def scrub_filename(self, filename):
        return re.sub('[<>:?*\\\/]', '', filename)

    def is_chat_end(self, chat_log):
        # chat_log['messages'][0]['id'] is the most recent chat
        # chat_log['messages'][-1]['id'] is the oldest chat
        # if they are equal that means we have reached the end of the chat long
        # thus we just return the result of that comparison
        # I negated it because if its true we want to stop, if false we want to continue so we can negate it and use
        # it in a loop
        return not (chat_log['messages'][0]['id'] == chat_log['messages'][-1]['id'])

    def load_group_messages(self, txts_per_page=None):

        if txts_per_page is None or txts_per_page < 0 or txts_per_page > 100:
            txts_per_page = '100'

        self.message_params['limit'] = str(txts_per_page)

        '''
         We need to set a variable so that we can refresh the page with an  certain amount of 
         messages without intervention
         
         we may be able to solve this by using an optional argument  
        '''
        try:
            chat_log = self.request(self.message_url, target_params=self.message_params)
        except:
            return False

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

        for message_text in chat_log['messages']:
            # print(json.dumps(message_text['text']))

            if len(message_text['attachments']) > 0 \
                    and message_text['attachments'][0]['type'] == 'image':
                # use json.dumps because the text will have emojis so we do this to ignore them
                phrase = json.dumps(message_text['text'])
                phrase_id = message_text['id']
                image_url = message_text['attachments'][0]['url']
                # save_folder = '\\Pictures\\'
                # phrase id is a particular text id
                # urllib.request.retrieve will save the remote file for us
                save_file = save_folder + '\\jpeg' + str(phrase_id) + '.jpeg'
                urllib.request.urlretrieve(image_url, filename=save_file)
                # print('text: ', phrase, 'image url: ', image_url)

                if self.limit_for_pictures is not None:
                    self.increment_amount_pix_seen()
                    if self.is_pix_limit_met():
                        return False

        self.message_params['before_id'] = chat_log['messages'][-1]['id']

        # Return true so that we can continue parsing to the next message
        return True

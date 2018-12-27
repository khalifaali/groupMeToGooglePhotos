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

    def select_group_messages(self):
        if len(self.group_ids) == 0:
            return 'groups are empty'

        print('Which Group Messages Would you like to see? \n')
        for index, value in enumerate(self.group_ids):
            print("Choice: ", index, " GroupChat ", value['name'])

        choice = int(input('\n Select the appropriate index...'))
        group_message = self.group_ids[choice]

        print('Selected Group chat is ', group_message['name'])

        self.message_url = self.url + '/groups/' + group_message['id'] + '/messages'
        self.selected_group_name = group_message['name']

    def scrub_filename(self, filename):
        return re.sub('[<>:?*\\\/]', '', filename)

    def load_group_messages(self, txts_per_page=None):

        if txts_per_page is None or txts_per_page < 0 or txts_per_page > 100:
            txts_per_page = '100'

        self.message_params['limit'] = str(txts_per_page)

        # if we can't request the previous message we have reached the end of all historical messages so abort function
        # by returning False
        try:
            chat_log = self.request(self.message_url, target_params=self.message_params)
        except:
            return False

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

        # save_file_types is an object that will choose the format to save depending on the attachment type in GM
        save_file_types = {'image': '.jpeg', 'video': '.mp4'}
        for message_text in chat_log['messages']:
            # print(json.dumps(message_text['text']))

            if len(message_text['attachments']) > 0 \
                    and (message_text['attachments'][0]['type'] == 'image'
                         or message_text['attachments'][0]['type'] == 'video'):

                attachment_type = message_text['attachments'][0]['type']
                # use json.dumps because the text will have emojis so we do this to ignore them

                phrase_id = message_text['id']
                image_url = message_text['attachments'][0]['url']
                # save_folder = '\\Pictures\\'
                # phrase id is a particular text id
                # urllib.request.retrieve will save the remote file for us
                save_file = save_folder + '\\' + str(phrase_id) + save_file_types[attachment_type]
                urllib.request.urlretrieve(image_url, filename=save_file)
                print(message_text['attachments'][0])
                # print('text: ', phrase, 'image url: ', image_url)

                if self.limit_for_pictures is not None:
                    self.increment_amount_pix_seen()
                    if self.is_pix_limit_met():
                        return False

        self.message_params['before_id'] = chat_log['messages'][-1]['id']

        # Return true so that we can continue parsing to the next message
        return True

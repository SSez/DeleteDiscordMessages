import requests, json, argparse

DISCORD_API_URL = 'https://discord.com/api/v9'

class Messages:
    def __init__(self, args):
        self.headers = { 'authorization': args['token'] }
        self.url = DISCORD_API_URL +'/channels/{}/messages'.format(args['channel'])

    def getMessages(self):
        def getLastMessages(message):
            messages = []
            r = requests.get(self.url + '?before=' + message + '&limit=50', headers=self.headers)
            if r.status_code == 200:
                messages = json.loads(r.text)
            return messages

        r = requests.get(self.url + '?limit=50', headers=self.headers)
        messages = json.loads(r.text)

        last_message = messages[-1]['id']
        while True:
            lm = getLastMessages(last_message)
            if lm:
                last_message = lm[-1]['id']
                messages.extend(lm)
            else:
                break
        return messages

    def deleteMessage(self, id):
        r = requests.delete(self.url + '/' + id, headers=self.headers)
        return r.status_code

def main(args):
    try:
        m = Messages(args)
        def delete(id):
            while True:
                if m.deleteMessage(id) == 204:
                    print('DELETED MESSAGE:', id)
                    break

        for msg in m.getMessages():
            if args['user']:
                if msg['author']['id'] == args['user'] or msg['author']['username'] == args['user']:
                    delete(msg['id'])
            else:
                delete(msg['id'])
    except:
        pass

if __name__ == '__main__':
    args_list = {}
    parser = argparse.ArgumentParser(description='[*] Discord message removal tool.')
    parser.add_argument('--token', metavar='<token>', help="Discord token", required=True)
    parser.add_argument('--channel', metavar='<channel>', help="Channel / Chat id", required=True)
    parser.add_argument('--user', metavar='<user>', help="User id", required=False)
    args = parser.parse_args()

    args_list['token'] = args.token
    args_list['channel'] = args.channel
    args_list['user'] = args.user

    main(args_list)

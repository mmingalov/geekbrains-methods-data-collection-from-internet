# ID приложения   7308366
# Защищенный ключ aprF938fcdB8R9KrhoLo
# Сервисный ключ доступа  134464c3134464c3134464c351132be08d11344134464c34d7e56ba71e7144c295bab1c

#05 Feb 2020
# https://vk.com/dev/first_guide
# https://oauth.vk.com/blank.html#access_token=b26c3fdb5c61ffc4772367e026b45544964f5e61f78b7e495f76aa6aa973b569b4ddc2e73ea9f44cbdb94&expires_in=86400&user_id=6244012

import requests

def get_username_by_id(user: int):
    url = 'https://api.vk.com/method/users.get?v=5.52&access_token=' + access_token
    url = url + '&user_id=' + str(user)
    response = requests.get(url)
    return response.json()

def get_users(user: int):
    url = 'https://api.vk.com/method/friends.get?v=5.52&access_token=' + access_token
    url = url + '&user_id=' + str(user)
    response = requests.get(url)
    return response.json()

def search(user: int, level: int):
    if level <= DEPTH_LEVEL:
        response = get_users(user)
        try:
            user_friends = response["response"]["items"]
        except KeyError as e:
            print(f'ERROR: {e.__class__}, level: {level}, processed_user: {user}, last_name: {get_username_by_id(user)["response"][0]["last_name"]}, is_private: TRUE')
            return None
        level += 1
        graph.append(None)
        for idx, item in enumerate(user_friends):
            print(f'level: {level}, level_persons: {len(user_friends)}, processed_user: {item}')
            graph[level] = item
            if item == user2_id:
                # graph_completed = True
                # graph.append(item)
                return True #graph_completed
            else:
                # graph[level] = item
                search(item,level)

graph_completed = False

if __name__ == '__main__':
    DEPTH_LEVEL = 2
    USER1 = 'https://vk.com/id6244012'
    # USER2 = 'https://vk.com/id30870147' #doroga_katya - связь прямая
    USER2 = 'https://vk.com/id7704548'  #runnaflow - связь через doroga_katya
    user1_id = int(USER1.replace('https://vk.com/id','').replace('https://vk.com/',''))
    user2_id = int(USER2.replace('https://vk.com/id', '').replace('https://vk.com/', ''))
    access_token = 'b26c3fdb5c61ffc4772367e026b45544964f5e61f78b7e495f76aa6aa973b569b4ddc2e73ea9f44cbdb94'
    graph_completed = False
    graph = []  #текущий граф
    graphs = [] #все возможные графы
    response1 = get_users(user1_id)
    response2 = get_users(user2_id)
    user1_friends = response1["response"]["items"]
    user2_friends = response2["response"]["items"]

#todo проверяем наличие прямой связи
    graph.append(user1_id)
    for idx, item in enumerate(user1_friends):
        if item == user2_id:
            graph_completed = True
            graph.append(user2_id)
            graph[0] = {
                "id": user1_id,
                "first_name": get_username_by_id(user1_id)["response"][0]["first_name"],
                "last_name": get_username_by_id(user1_id)["response"][0]["last_name"]
            }
            graph[1] = {
                "id": user2_id,
                "first_name": get_username_by_id(user2_id)["response"][0]["first_name"],
                "last_name": get_username_by_id(user2_id)["response"][0]["last_name"]
            }
            graphs.append(graph.copy())
    if graph_completed == False:
        print('Прямая связь отсутствует!')
#todo основной цикл
    while graph_completed == False:
        graph = []
        graph.append(user1_id)
        graph.append(user2_id)
        for idx, item in enumerate(user1_friends):
            level = 1
            print(f'level: {level}, level_persons: {len(user1_friends)}, processed_user: {item}, last_name: {get_username_by_id(item)["response"][0]["last_name"]}, idx: {idx}')
            if search(item, level):
                graph[level] = {
                    "id": item,
                    "first_name": get_username_by_id(item)["response"][0]["first_name"],
                    "last_name": get_username_by_id(item)["response"][0]["last_name"]
                }
                graphs.append(graph.copy())
                print('Bingo!', graph)
                pass
                # break
        graph_completed = True

    # graph[0] = {
    #     "id": user1_id,
    #     "first_name": get_username_by_id(user1_id)["response"][0]["first_name"],
    #     "last_name": get_username_by_id(user1_id)["response"][0]["last_name"]
    # }
    print(graphs, sep = '\n')
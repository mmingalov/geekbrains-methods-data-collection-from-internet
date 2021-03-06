# Рессурс на выбор или VK, или FB
#
# Ваша задача на старте паука принять 2 сслыки на странички пользователей (людей)
# Найти самую короткую цепочку рукопожатий именно составля ее из общих друзей
# https://ru.wikipedia.org/wiki/Теория_шести_рукопожатий
#
# В результате у вас должна быть база данных в которой примерно такая структура ( это не принципиально):
# {
# "person_a": "url", # ссылка на персону A
# "person_b":"url", # ссылка на персону B
# chain: [<url>, <url> ....] # цепочка (список) из ссылок
# }



# ID приложения   7308366
# Защищенный ключ aprF938fcdB8R9KrhoLo
# Сервисный ключ доступа  134464c3134464c3134464c351132be08d11344134464c34d7e56ba71e7144c295bab1c

#05-07 Feb 2020
# https://vk.com/dev/first_guide
# https://oauth.vk.com/authorize?client_id=7308366&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.52
# https://oauth.vk.com/blank.html#access_token=b26c3fdb5c61ffc4772367e026b45544964f5e61f78b7e495f76aa6aa973b569b4ddc2e73ea9f44cbdb94&expires_in=86400&user_id=6244012
# https://oauth.vk.com/blank.html#access_token=a1ff3cbff9d54f3d0c8383b51955b449fb63fb0f06fb11d00f315c2643326cc14d716346fb449663c483f&expires_in=86400&user_id=6244012
# https://oauth.vk.com/blank.html#access_token=bd6e284e05cd008ab187f5d9b2b3febf295114c66ea9f4da3aec3ecfee3182614fe3f4a4edd558f6784b9&expires_in=86400&user_id=6244012
# https://oauth.vk.com/blank.html#access_token=913cbd317b158a61a30b4844eadab0671b7cf5e55fa6331e0745edd44e45f8cfc0780d9044983e6bd25e5&expires_in=86400&user_id=6244012
import requests

def get_user_info_by_id(user: int):
    url = 'https://api.vk.com/method/users.get?v=5.52&access_token=' + access_token
    url = url + '&user_id=' + str(user)
    response = requests.get(url)
    return response.json()

def get_username(user: int):
    try:
        info = get_user_info_by_id(user)

        first_name = info["response"][0]["first_name"]
        last_name = info["response"][0]["last_name"]
        username = first_name + ' ' + last_name
    except:
        username = None
    return username

def get_users(user: int):
    url = 'https://api.vk.com/method/friends.get?v=5.52&access_token=' + access_token
    url = url + '&user_id=' + str(user)
    response = requests.get(url)
    return response.json()

def search(user: int, level: int, graph: list):
    if level < DEPTH_LEVEL:
        response = get_users(user)
        try:
            user_friends = response["response"]["items"]
            uf_set = set(user_friends)
            level += 1
        except Exception as e:
            print(f'ERROR: {e.__class__}, level: {level}, processed_user: {user}, user_name: {get_username(user)}, is_private: TRUE')
            return None

        if uf_set.__contains__(user2_id):
            graph_completed = True
            return True
        else:
            for idx, item in enumerate(user_friends):
                # print(f'level: {level}, level_persons: {len(user_friends)}, processed_user: {item}')
                if search(item, level,graph):
                    graph[level] = item
                    print(f'Совпадение на idx: {idx}')
                    graph_completed = True
                    return True

# graph_completed = False

if __name__ == '__main__':
    DEPTH_LEVEL = 3 #ограничение глубины поиска. Единица соответствует прямой связи, двойка -- связи через 1-го человека, тройка -- связи через двух человек.
    USER1 = 'https://vk.com/id6244012'
    # USER2 = 'https://vk.com/id30870147' #связь прямая
    USER2 = 'https://vk.com/id7704548'  #Александра Бегун, через 1-го -- три разных графа
    # USER2 = 'https://vk.com/id9787523' #Евгения Леонтьева, через 1-го -- три разных графа, через 2-их три разных графа

# main
    user1_id = int(USER1.replace('https://vk.com/id','').replace('https://vk.com/',''))
    user2_id = int(USER2.replace('https://vk.com/id', '').replace('https://vk.com/', ''))
    access_token = '913cbd317b158a61a30b4844eadab0671b7cf5e55fa6331e0745edd44e45f8cfc0780d9044983e6bd25e5'
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
            graphs.append(graph.copy())

    if graph_completed == False:
        print('Прямая связь отсутствует!')
#todo основной цикл
    # graph = [None] * (DEPTH_LEVEL + 2)  # текущий граф
    while graph_completed == False:
        # graph[0] = user1_id #.append(user1_id)
        # graph[1] = user2_id  #append(user2_id)
        # user1_friends = [4921405,6182129,278075880] #гегельская, берсенев, рыжова
        # user1_friends = [4921405, 6182129, 278075880, 560056, 803898]  # [гегельская, берсенев, рыжова] - Уровень 1, [зейбель, тимшин] - Уровень 2

        for idx, item in enumerate(user1_friends):
            graph = [None] * (DEPTH_LEVEL + 2)  # текущий граф
            graph[0] = user1_id
            level = 1
            print(f'level: {level}, level_persons: {len(user1_friends)}, processed_user: {item}, last_name: {get_user_info_by_id(item)["response"][0]["last_name"]}, idx: {idx}')
            if search(item, level,graph):
                graph[level] = item
                graph_ = list(filter(lambda x: x!=None, graph))
                graph_.append(user2_id)
                graphs.append(tuple(graph_))   #graph_.copy())
                print('Bingo!', graph_)
                pass
                # break
        graph_completed = True

    # graph[0] = {
    #     "id": user1_id,
    #     "first_name": get_user_info_by_id(user1_id)["response"][0]["first_name"],
    #     "last_name": get_user_info_by_id(user1_id)["response"][0]["last_name"]
    # }
    print(f'Найдено графов: {len(graphs)}')
    for i in graphs:
        print(i)
        t_graph = ''
        for j in i:
            t_graph = t_graph + get_username(j) + ' -- '
        print(t_graph[:-4])

#todo сохраним коллекцию в MongoDB
    from pymongo import MongoClient
    try:
        conn = MongoClient()
    except:
        print("Could not connect to MongoDB")
    # database
    db = conn.VK_graphs
    collection = db.Recursion

    for i in graphs:
        t_graph = ''
        for j in i:
            t_graph = t_graph + get_username(j) + ' -- '

        t_graph2 = t_graph[:-4]
        item = {
            "user1": {
                "link": USER1,
                "id": user1_id,
                "username": get_username(user1_id)
            },
            "user2": {
                "link": USER2,
                "id": user2_id,
                "username": get_username(user2_id)
            },

            "graph_id": i,
            "graph_username": t_graph2,
        }
        rec_id1 = collection.insert_one(item)
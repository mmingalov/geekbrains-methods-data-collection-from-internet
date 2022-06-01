VK.com social network

On start Spider gets 2 links on VK user accounts. Algorithm task is: to find the shortest chain of handshakes by composing it from mutual friends
https://ru.wikipedia.org/wiki/Теория_шести_рукопожатий

В результате у вас должна быть база данных в которой примерно такая структура ( это не принципиально):
{
"person_a": "url", # link to person A
"person_b":"url", # link to person B
chain: [<url>, <url> ....] # chain (list) of links
}
----------------------------------------------------------------------------------------------
TASK was solved in two different ways

1.
Implementation via Scrapy Spider

2.
Implementation via recursion without spider (see vk_recursion.py)
Here the logic of work has the following nuance:
- the search depth DEPTH_LEVEL is set as a natural positive number, where:
for example, the number 1 corresponds to a direct connection, the number 2 corresponds to a connection through one person, the number three corresponds to a connection through two people.
- the algorithm will find and save all possible graphs in MongoDB, and will not be limited to only the optimal one. In this case, graphs can be with a different number of handshakes. It was interesting to implement it in this vein.

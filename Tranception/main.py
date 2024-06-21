import asyncio
from tranception import Tranception

def main():
    evokation = Tranception()
    asyncio.run(evokation.induce())

    for agent in evokation.reflectors:
        
        print(f"Node {agent.idx} has {agent.transceivers}")

    # asyncio.create_task(node_list[0].rcv(440))
    # asyncio.create_task(node_list[0].snd(node_list[1]))

if __name__ == '__main__':
    main()
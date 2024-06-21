import asyncio
from tranception import Tranception

def main():
    print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(" ~ Tranception ~ (Cognitive Computing)")
    print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    "The process of evoking a trance-like state in a subject to explore the concept of the unconscious mind."
    print("")
    evokation = Tranception()
    
    print("")
    for agent in evokation.reflectors:
        print(f"Node{agent.idx}.transceiver<[{agent.transceivers}]>")
    
    print("")
    asyncio.run(evokation.induce())


    # asyncio.create_task(node_list[0].rcv(440))
    # asyncio.create_task(node_list[0].snd(node_list[1]))

if __name__ == '__main__':
    main()
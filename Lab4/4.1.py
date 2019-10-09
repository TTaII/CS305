#encoding:GBK
'''
Created on 2019��10��02��

@author: lct
'''
import asyncio

Fail = "Connection closes!"
async def dispatch(reader, writer): 
    while True: 
        data = await reader.read(100)
        d = data.decode()
        client = writer.get_extra_info('peername')  # �����׽������ӵ�Զ�̵�ַ
        print('Received from {}: {}'.format(client, d))  # �ڿ���̨��ӡ��ѯ��¼ 
        if d[-4:] == 'exit' or not d: 
            writer.write(Fail.encode())
            break 
        writer.write(data)
        await writer.drain()
    writer.close()
if __name__ == '__main__': 
    loop = asyncio.get_event_loop() 
    coro = asyncio.start_server(dispatch, '127.0.0.1', 5555, loop=loop) 
    server = loop.run_until_complete(coro)
# Serve requests until Ctrl+C is pressed 
    print('Serving on {}. Hits Control+C to end the connection'.format(server.sockets[0].getsockname()))
    try: 
        loop.run_forever() 
    except KeyboardInterrupt: 
        pass
# Close the server server.close() 
    loop.run_until_complete(server.wait_closed()) 
    loop.close()
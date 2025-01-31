import time
import asyncio, telnetlib3

async def shell(reader, writer):
    while True:
        # read stream until '?' mark is found
        outp = await reader.read(1024)
        if not outp:
            # End of File
            break
        elif 'Enter password' in outp:
            # reply all questions with 'y'.
            writer.write('adept\r\n')
        else:
            writer.write('doTaskInstant playInstant vineboom.wav\r\n')
            #time.sleep(3)
            writer.write('say test test\r\n')
            time.sleep(1)

        # display all server output
        print(outp, flush=True)

    # EOF
    print()


loop = asyncio.get_event_loop()
coro = telnetlib3.open_connection('10.38.4.171', 7170, shell=shell)
reader, writer = loop.run_until_complete(coro)
loop.run_until_complete(writer.protocol.waiter_closed)
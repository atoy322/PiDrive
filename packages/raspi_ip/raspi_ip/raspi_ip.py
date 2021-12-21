from socket import AF_INET, getaddrinfo


HOST = "raspberrypi.local"

while True:
    try:
        IP = getaddrinfo(HOST, None, AF_INET)[0][-1][0]
        break

    except Exception as e:
        continue

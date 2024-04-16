from eventbus import State, hello_connected, hello_no_gateway, hello_timeout, ping

events = [ping, hello_connected, hello_no_gateway, hello_timeout]
print([e.to_dict() for e in events])
# print(Event.from_dict([e.to_dict() for e in events]))

temp = State(entity="temp", value=22)

print(temp.to_dict())
print(State.from_dict(temp.to_dict()))

temp = State(entity="temp", value={"temp": (1, 2, 3, "55")})

print(temp.to_dict())
print(State.from_dict(temp.to_dict()))

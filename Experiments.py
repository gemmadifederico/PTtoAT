import TraceCheck as tc
import uuid

a = 299
for x in range(a):
    code = str(uuid.uuid4())[-5:]
    tc.main(code,30,30,50)

b = 299
for x in range(b):
    code = str(uuid.uuid4())[-5:]
    tc.main(code,50,50,100)

c = 399
for x in range(c):
    code = str(uuid.uuid4())[-5:]
    tc.main(code,150,150,300)


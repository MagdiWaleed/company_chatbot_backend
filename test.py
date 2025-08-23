import http.client
import json

import threading
from agents.chatbot_agent.agent import getChatbotAgent
agent = getChatbotAgent()
# def dietAgent(token):
#     sio = socketio.Client()
#     reply_event = threading.Event()

#     @sio.event
#     def message(response):
#         print(f"Ai: {response}")
#         reply_event.set()

#     sio.connect('http://localhost:5000',
#                     auth={"token": token})
#     while True:
#         userinput = input("('exit' to exit) You: ")
#         if userinput == "exit":
#             break
#         reply_event.clear()
#         sio.emit(data={"text":userinput,"token":token}, event="diet_messages")

#         if not reply_event.wait(timeout=30):
#             print("⚠️ No response from server within 30 seconds")
#     sio.emit("disconnecting", {"token": token})
#     sio.disconnect()

# def informationAgent(token):
#     sio = socketio.Client()
#     reply_event = threading.Event()

#     @sio.event
#     def message(response):
#         print(f"Ai: {response}")
#         reply_event.set()

#     sio.connect('http://localhost:5000',
#                     auth={"token": token})
#     while True:
#         userinput = input("('exit' to exit) You: ")
#         if userinput == "exit":
#             break
#         reply_event.clear()
#         sio.emit(data={"text":userinput,"token":token}, event="information_messages")

#         if not reply_event.wait(timeout=30):
#             print("⚠️ No response from server within 30 seconds")
#     sio.emit("disconnecting", {"token": token})
#     sio.disconnect()

# def sign_in():
#     conn = http.client.HTTPConnection("localhost", 5000)
#     email = input(" -   Enter your email: ")
#     password = input(" -   Enter your password: ")
#     data = {
#         "email": email,
#         "password": password
#     }
#     json_data = json.dumps(data)
#     headers ={
#         "Content-Type": "application/json",
#         "Content-Length": str(len(json_data))
#     }
#     conn.request("POST", "/sign-in/",body= json_data,headers=headers)
    
#     response = conn.getresponse()
    
#     data =json.loads(response.read().decode())
#     conn.close()
#     if response.status == 404 or response == 401:
#         print("error message: ", data['error'])
#     else:
#         return data['token']


# def sign_up():
#     conn = http.client.HTTPConnection("localhost", 5000)
#     email = input(" -   Enter your email: ")
#     password = input(" -   Enter your password: ")
#     name = input(" -   Enter your name: ")

#     data = {
#         "email": email,
#         "password": password,
#         "name": name
#     }
#     json_data = json.dumps(data)
#     headers ={
#         "Content-Type": "application/json",
#         "Content-Length": str(len(json_data))
#     }
#     conn.request("POST", "/sign-up/",body= json_data,headers=headers)
    
#     response = conn.getresponse()
    
#     data =json.loads(response.read().decode())
#     conn.close()

#     if response.status == 404 or response.status == 400:
#         print("error message: ", data['error'])
#     else:
#         print(data['message'])
        
        




# if __name__ == "__main__":
#     user_token = None

#     while True:
#         print("     1)  Sign in")
#         print("     2)  Sign up")
#         user_input =int(input("     -   Choose option: "))
#         if (user_input == 1):
#             print("\n"*200)
#             token =sign_in()
#             if token is not None:
#                 user_token = token
#                 while True:
#                     print("     1)  Personal Information Agent")
#                     print("     2)  Diet planner Agent")
#                     print("     3)  Log out")
                    
#                     user_input =int(input("     -   Choose option: "))
#                     if user_input == 1:
#                         informationAgent(token)

#                     elif (user_input== 2):
#                         dietAgent(token)
#                     elif user_input ==3:
#                         token = None
#                         break
#                     else:
#                         print("enter valid option")
#                         print("\n"*200)



#         elif (user_input== 2):
#             sign_up()
#         else:
#             print("enter valid option")
#             print("\n"*200)

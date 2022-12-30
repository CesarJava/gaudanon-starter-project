import time
import datetime
import json
import awsiot.greengrasscoreipc
from awsiot.greengrasscoreipc.clientv2 import GreengrassCoreIPCClientV2
from awsiot.greengrasscoreipc.model import (
    BinaryMessage,
    PublishMessage,
    JsonMessage,
    SubscriptionResponseMessage,
    UnauthorizedError
)
import sys
import traceback

class IPCComm:
    
    #ipcClient = awsiot.greengrasscoreipc.connect()
    
    #TIMEOUT = 10
    
    def __init__(self, clientId, topic=None):
        self.topic = topic
        
        if clientId :
            self.clientId = clientId
        else:
            raise Exception("Please specify a client Id")
        
        try:
            self.ipcClient = GreengrassCoreIPCClientV2()
        except Exception:
            print('Exception ocurred')
            traceback.print_exc()
    
    #@classmethod
    #def Publisher(cls, publisherId, topicToPublish):
    #    ipcComm = cls(publisherId, topicToPublish)
    #    return ipcComm
   
    #@classmethod        
    #def Subscriber(cls, subscriberId, topicToSubscribe):
    #    ipcComm = cls(publisherId, topicToPublish)
    #    return ipcComm
            
    
    def setTopic(self, topic):
        self.topic = topic
    
    def getTopic(self, topic):
        return self.topic
    
    def setMessage(self, message):
        messageSchema={
            "timestamp": str(datetime.datetime.now()),
            "clientId": str(self.clientId),
            "body": message 
        }
        self.messageToPublish = self.__buildPubMessage(messageSchema)
        
        
    def getMessage(self):
        return self.messageToPublish.json_message.message

    def publishMessage(self, message=None):
        messageToPublish = None
        if message:
            messageToPublish = self.__buildPubMessage(message)
        elif self.messageToPublish :
            messageToPublish = self.messageToPublish
        else:
            raise Exception("No message specified")
        
        try:
            self.ipcClient.publish_to_topic(topic=self.topic, publish_message=messageToPublish)
        except Exception:
            traceback.print_exc()
                        
        print("Message Published")
    
    def subscribeToTopic(self, topicToSubscribe=None):
        topic = None
        if topicToSubscribe :
            topic = topicToSubscribe
        elif self.topic :
            topic = self.topic
        else:
            print("Please specify a topic")
            return 
        
        try:
            # Subscription operations return a tuple with the response and the operation.
            response, operation = self.ipc_client.subscribe_to_topic(topic=topic, on_stream_event=self.__on_stream_event,
                                                        on_stream_error=self.__on_stream_error, on_stream_closed=self.__on_stream_closed)
            try:
                while True:
                    time.sleep(10)
            except InterruptedError:
                print('Subscribe interrupted.')

            # To stop subscribing, close the stream.
            operation.close()
        except UnauthorizedError:
            print('Unauthorized error while subscribing to topic: ' + topic)
            traceback.print_exc()
        except Exception:
            print('Exception occurred')
            traceback.print_exc()
        
        print('Successfully subscribed to topic: ' + topic)

    
    
    def __on_stream_event(self, event: SubscriptionResponseMessage) -> None:
        try:
            message = str(event.binary_message.message, 'utf-8')
            self.subCallbackMethod(message)
        except:
            traceback.print_exc()

    def __on_stream_error(self, error: Exception) -> bool:
        print('Received a stream error.')
        traceback.print_exc()
        return False  # Return True to close stream, False to keep stream open.

    def __on_stream_closed(self) -> None:
        print('Subscribe to topic stream closed.')
    
    def subscribeCallbackMethod(self, methodToCall):
        self.subCallbackMethod = methodToCall
        
    def __buildPubMessage(self,message):
        binaryMessage = BinaryMessage(message=bytes(message, 'utf-8'))
        return PublishMessage(binary_message=binaryMessage)



    
    
    
    
    
    
    
    
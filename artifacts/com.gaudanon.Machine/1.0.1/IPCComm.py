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
        print("Message set to: ", json.dumps(messageSchema))
        self.messageToPublish = self.__buildPubMessage(json.dumps(messageSchema))
        
        
    def getMessage(self):
        return self.messageToPublish.json_message.message

    def publishMessage(self, message=None, topicToPublish=None):
        messageToPublish = None
        
        topic = self.__topicInterpreter(topicToPublish)
        
        if message:
            messageToPublish = self.__buildPubMessage(message)
        elif self.messageToPublish :
            messageToPublish = self.messageToPublish
        else:
            raise Exception("No message specified")
        
        try:
            self.ipcClient.publish_to_topic(topic=topic, publish_message=messageToPublish)
        except Exception:
            traceback.print_exc()
                        
        print("Message Published")   
    
    def subscribeToTopic(self, topicToSubscribe=None, streamEventCallback=None, streamErrorCallback=None, streamClosedCallback=None):
        topic = self.__topicInterpreter(topicToSubscribe)
        
        onStreamEventCallback = streamEventCallback if streamEventCallback != None else self.__on_stream_event
        onStreamErrorCallback = streamErrorCallback if streamErrorCallback != None else self.__on_stream_error
        onStreamClosedCallback = streamClosedCallback if streamClosedCallback != None else self.__on_stream_closed
        
        try:
            # Subscription operations return a tuple with the response and the operation.
            response, operation = self.ipcClient.subscribe_to_topic(topic=topic, on_stream_event=onStreamEventCallback,
                                                        on_stream_error=onStreamErrorCallback, on_stream_closed=onStreamClosedCallback)
            #try:
            #    while True:
            #        time.sleep(10)
            #except InterruptedError:
            #    print('Subscribe interrupted.')

            ## To stop subscribing, close the stream.
            #operation.close()
        except UnauthorizedError:
            print('Unauthorized error while subscribing to topic: ' + topic)
            traceback.print_exc()
            operation.close()
        except Exception:
            print('Exception occurred')
            traceback.print_exc()
            operation.close()
            
        print('Successfully subscribed to topic: ' + topic)

    def __topicInterpreter(self, topicInput=None):
        topic = None
        
        if topicInput :
            topic = topicInput
        elif self.topic :
            topic = self.topic
        else:
            print("Please specify a topic")
            return 
        
        return topic
        
    
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
    
    def publishToIoTCore(self, topicName, qos, payload):
        self.ipcClient.publish_to_iot_core(topic_name=topicName, qos='1',payload=payload)
    
    @staticmethod
    def returnEventMessage(event: SubscriptionResponseMessage) -> None:
        try:
            message = str(event.binary_message.message, 'utf-8')
            return message
        except:
            traceback.print_exc()
    
    @staticmethod
    def streamEventMessage(self, error: Exception) -> bool:
        print('Received a stream error.')
        traceback.print_exc()
        return False  # Return True to close stream, False to keep stream open.

        

    
    
    
    
    
    
    
    
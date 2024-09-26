"""The Python implementation of the GRPC game of life server."""

from concurrent import futures
import logging
from game_of_life_service import game_of_life_service
from game_exceptions import *

import grpc
import game_pb2
import game_pb2_grpc


class Game(game_pb2_grpc.GameServicer):
    def __init__(self):
        super().__init__()
        self.game_service = game_of_life_service()
        

    def SayHello(self, request, context):
        print('SayHello received. Replying to ' + request.name)
        return game_pb2.HelloReply(message="Hello, %s!" % request.name)
    
    def NewGame(self, request, context):
        try:    
            metadata = str(context.invocation_metadata())
            size = (request.size_x, request.size_y)
            
            print(f'New session requested with size={size} ')
            session_id = self.game_service.new_session(size_x=request.size_x, 
                                        size_y=request.size_y, 
                                        p=request.p, 
                                        metadata=metadata)
            print(f'New session created with size={size}, metadata={metadata}, session_id={session_id}')
            return game_pb2.NewGameReply(data=f'New session requested with {size} with {session_id} with metadata {metadata}')
        except Exception as e:
            print(e)

    def ShowAllSessions(self, request, context):
        try:
            print(f'Showing all sessions with metadata={str(context.invocation_metadata())}')
            for session in self.game_service.show_all_sessions():
                yield game_pb2.SessionDetailsReply(
                    session_id=session['session_id'],
                    date=str(session['date']),
                    metadata=session['metadata'],
                    steps=session['steps'],
                    last=str(session['last'])
                )
        except Exception as e:
            print(e)

    def GetCurrentSession(self, request, context):
        try:
            session = self.game_service.get_current_session_details()
            return game_pb2.SessionDetailsReply(
                    session_id=session['session_id'],
                    date=str(session['date']),
                    metadata=session['metadata'],
                    steps=session['steps'],
                    last=str(session['last'])
            )
        except NoSessionIdSelectedException:
            print('No session ID selected')
            # TODO: Implement response
            pass
        except SessionIdNotExistsException:
            print('Session ID does not exist')
            # TODO: Implement response
            pass
        except Exception as e:
            print(e)
            # TODO: Implement response
            pass

    def SetCurrentSession(self, request, context):
        try:
            session_id=request.session_id
            print('Session ID to be set:', session_id)
            session = self.game_service.set_current_session_details(session_id=session_id)
            return game_pb2.SessionDetailsReply(
                    session_id=session['session_id'],
                    date=str(session['date']),
                    metadata=session['metadata'],
                    steps=session['steps'],
                    last=str(session['last'])
            )
        except SessionIdNotExistsException:
            print('Session ID does not exist')
            # TODO: Implement response
            pass
        except Exception as e:
            print(e)
            # TODO: Implement response
            pass
    
    def GetState(self, request, context):
        try:
            step = request.step
            data = self.game_service.get_state(step=step)
            return game_pb2.GetStateReply(
                    data = data
            )
        except Exception as e:
            print(e)
            # TODO: Implement response
            pass

    def Step(self, request, context):
        try:
            self.game_service.step()
            return game_pb2.StepReply()
        except Exception as e:
            print(e)
            # TODO: Implement response
        



def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    game_pb2_grpc.add_GameServicer_to_server(Game(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()

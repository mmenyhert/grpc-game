# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC game of life client."""

from __future__ import print_function

import logging
import argparse

import grpc
import game_pb2
import game_pb2_grpc


from game_of_life_globals import *
from json import loads

def create_parser():
    parser = argparse.ArgumentParser(prog='Game of Life client',
                    description='Sends gRPC requests to the Game of Life server.'
                    )
    subparsers = parser.add_subparsers(dest='subcommand', help='Subcommands')

    name_parser = subparsers.add_parser('say_hello', help='Say hello to someone.')
    name_parser.add_argument('--name', type=str, help='Name to be greeted')
    name_parser.set_defaults(func=say_hello)

    new_parser = subparsers.add_parser('new_game', help='Request a new Game of Life')
    new_parser.add_argument('--size_x', type=int, help='Size X', default=DEFAULT_SIZE_X)
    new_parser.add_argument('--size_y', type=int, help='Size Y', default=DEFAULT_SIZE_Y)
    new_parser.add_argument('--p', type=int, help='Initial probability', default=INITIAL_PROBABILITY)
    new_parser.set_defaults(func=new_game)

    new_parser = subparsers.add_parser('show_all_sessions', help='Request to show all sessions')
    new_parser.set_defaults(func=show_all_sessions)

    new_parser = subparsers.add_parser('get_current_session', help='Get the current session ID with some details')
    new_parser.set_defaults(func=get_current_session)

    new_parser = subparsers.add_parser('set_current_session', help='Set the current session ID.')
    new_parser.add_argument('--session', type=str, help='Session ID', )
    new_parser.set_defaults(func=set_current_session)

    new_parser = subparsers.add_parser('get_state', help='Gets the state at step index for the current session ID.')
    new_parser.add_argument('--step', type=int, help='Index of the step. Accepts negative indexing.')
    new_parser.set_defaults(func=get_state)

    new_parser = subparsers.add_parser('step', help='Step the current session ID')
    new_parser.set_defaults(func=step)

    return parser


def run(args):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = game_pb2_grpc.GameStub(channel)

        while True:
            try:
                prompt = input("Game of Life >> ")
                if prompt.lower() in ['exit', 'quit']:
                    break
                args = parser.parse_args(prompt.split())
                # Run the appropriate function based on the subcommand
                if hasattr(args, 'func'):
                    args.func(args=args, stub=stub)
                else:
                    print("No valid subcommand provided")
            except Exception as e:
                print(f"Error: {e}")
            

def parse_game_string(data_string):
    return loads(data_string)

def pretty_print_game(data):
    s = ''
    for line in data:
        for c in line:
            if c == 1:
                s += '■'
            elif c == 0:
                s += '□'
        s += '\n'
    print(s)
    


def new_game(args, stub):
    response = stub.NewGame(game_pb2.NewGameRequest(size_x=args.size_x, size_y=args.size_y, p=args.p))
    print("NewGameRequest sent. Received new game and game ID set.")
    print(response.data)

def say_hello(args, stub):
    response = stub.SayHello(game_pb2.HelloRequest(name=args.name))
    print("Greeter client received: " + response.message)   

def show_all_sessions(args, stub):
    response = stub.ShowAllSessions(game_pb2.ShowAllSessionsRequest())
    print("All sessions are the following.\n")
    print(*response,sep='\n',end='\n\n')

def get_current_session(args, stub):
    response = stub.GetCurrentSession(game_pb2.GetCurrentSessionRequest())
    print(response,sep='\n',end='\n\n')

def set_current_session(args, stub):
    session_id = args.session
    response = stub.SetCurrentSession(game_pb2.SetCurrentSessionRequest(session_id=session_id))
    print('Current session set to')
    print(response,sep='\n',end='\n\n')

def get_state(args, stub):
    response = stub.GetState(game_pb2.GetStateRequest(step=args.step))
    data = parse_game_string(response.data)
    pretty_print_game(data)

def step(args, stub):
    response = stub.Step(game_pb2.StepRequest())
    print('Stepped', response)


if __name__ == "__main__":
    logging.basicConfig()
    parser = create_parser()
    args = parser.parse_args()
    run(args)

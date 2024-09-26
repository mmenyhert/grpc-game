from game_of_life import game_of_life
from game_database import game_database
from uuid import uuid4
from game_exceptions import *
from json import loads

class game_of_life_service:
    def __init__(self):
        # TODO: refactor so that every relevant field is stored as state
        self.database = game_database()
        self.current_session_id = None
        

    def show_all_sessions(self):
        return self.database.show_all_sessions()

    def get_current_session_details(self):
        if self.current_session_id is None:
            raise NoSessionIdSelectedException

        if not self.session_id_already_exists(self.current_session_id):
            raise SessionIdNotExistsException
        
        return self.database.get_session_by_id(session_id=self.current_session_id)
    
    def set_current_session_details(self, session_id):
        if not self.session_id_already_exists(session_id=session_id):
            raise SessionIdNotExistsException
        
        self.current_session_id = session_id
        return self.database.get_session_by_id(session_id=self.current_session_id)
        
    def session_id_already_exists(self, session_id):
        return self.database.session_id_already_exists(session_id=session_id)

    def new_session(self, size_x, size_y, p, metadata):
        session_id = str(uuid4())
        while self.session_id_already_exists(session_id):
            session_id = str(uuid4())

        new_life = game_of_life.new_life(size_x=size_x, size_y=size_y, probability=p, )
        new_life_string = str(new_life)

        self.database.new_life(session_id=session_id, metadata=metadata, new_life_string=new_life_string)
        
        self.current_session_id = str(session_id)

        return session_id
    
    def get_state(self, step):
        if self.current_session_id is None:
            raise NoSessionIdSelectedException
        
        states = self.database.get_states(session_id=self.current_session_id)

        data = states[int(step)][0]

        return data
    
    def step(self, ):
        if self.current_session_id is None:
            raise NoSessionIdSelectedException
        
        states = self.database.get_states(session_id=self.current_session_id)
        
        next_state_idx = len(states)
        last_state = loads(states[-1][0])

        next_state = game_of_life.step(life=last_state)
        print('Next state', next_state)
        self.database.store_state(session_id=self.current_session_id, life_string=str(next_state), step=next_state_idx)
        print('Stored new state.')



    



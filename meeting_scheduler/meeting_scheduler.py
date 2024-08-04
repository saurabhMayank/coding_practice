from enum import Enum
import time
from abc import ABC, abstractmethod

from datetime import datetime, timedelta


class MeetingModel:
    def __init__(self, name, time, duration):
        self.id = time.time()
        self.name = name
        self.time = time
        # duration in hrs
        self.duration = duration


class RoomModel:
    def __init__(self, name):
        self.id = time.time()
        self.name = name


class UserModel:
    def __init__(self, name, email):
        self.id = time.time()
        self.email = email
        self.name = name


class MeetingSchedulerModel:
    total_meeting_transaction = []

    # signify row in the DB
    def __init__(self, user: UserModel, meeting: MeetingModel, room: RoomModel):
        self.id = time.time()
        self.user = user
        self.meeting = meeting
        self.room = room

    @staticmethod
    def add_meeting_transac_to_total(meeting_transac_obj: MeetingSchedulerModel):
        MeetingTransactionModel.total_meeting_transaction.append(meeting_transac_obj)


"""
Services
"""


class MeetingService:
    def __init__(self):
        pass

    def get_meeting_list(self, meeting_id: int):
        """
        Function api to get meeting by meeting id
        """

        # valdiation of meeting_id
        
        meeting_list = []
        for meeting_sch_obj in MeetingSchedulerModel.total_meeting_transaction:
            if meeting_sch_obj.meeting.id == meeting_id:
                meeting_list.append(meeting_sch_obj.meeting)
        
        return meeting_list


class UserService:
    def __init__(self):
        pass

    def get_meeting_list(self, user_name: str):
        """
         Function api to get meeting by user_name
        """

        # valdiation of user_name
        
        meeting_list = []
        for meeting_sch_obj in MeetingSchedulerModel.total_meeting_transaction:
            if meeting_sch_obj.user.name == user_name:
                meeting_list.append(meeting_sch_obj.meeting)
        
        return meeting_list



class RoomService:
    def __init__(self):
        pass

    def get_meeting_list(self, room_name: int):
        """
        Function api to get meeting by room_name
        """

        # valdiation of meeting_id
        
        meeting_list = []
        for meeting_sch_obj in MeetingSchedulerModel.total_meeting_transaction:
            if meeting_sch_obj.room.name == room_name:
                meeting_list.append(meeting_sch_obj.meeting)
        
        return meeting_list



class MeetingSchedulerService:
    def __init__(self):
        pass

    def schedule_meeting(
        self,
        user_list: List[UserModel],
        room: RoomModel,
        time: datetime,
        duration: int,
        meeting_name: str,
    ):
        """
        Functional API to schedule meeting
        Checks
        -> Check if at that time -> room available or not
        -> check if all users available at that time
        -> if there is any conflict -> suggest another time slot
        -> Else schedule the meeting

        -> Extension -> Suggest another slot if conflict (not implemented)
        """

        # check if room available
        for meeting_sch_obj in MeetingSchedulerModel.total_meeting_transaction:
            if (
                room.id == meeting_sch_obj.room.id
                and meeting_sch_obj.meeting.time == time
            ):
                raise Exception("Room is not available in that time")

        # check if all users are free
        for meeting_sch_obj in MeetingSchedulerModel.total_meeting_transaction:
            if (
                meeting_sch_obj.user in user_list
                and meeting_sch_obj.meeting.time == time
            ):
                raise Exception(
                    f"User {meeting_sch_obj.user.name} not available at the defined, pls choose another time"
                )

        # schedule the meeting
        meeting_obj = Meeting(name, time, duration)
        for user_obj in user_list:
            meeting_sch_obj = MeetingSchedulerModel(user_obj, room, meeting_obj)
            MeetingSchedulerModel.add_meeting_transac_to_total(meeting_sch_obj)

        
        print("Meeting is scheduled")


"""
Api Handler
"""
class ApiHandler:
    def __init__(self):
        pass
    

    def schedule_meeting(self, user_list, room, time, duration, meeting_name):
        meeting_sch = MeetingSchedulerService()
        meeting_sch.schedule_meeting(user_list, room, time, duration, meeting_name)


def main():
    """
    """
    pass


if __name__ == "__main__":
    main()

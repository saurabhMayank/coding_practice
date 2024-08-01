"""
Router page, all the APIs for the limited time deal application
will be listed here

"""
# use timestamp for unique identifier
import time

from datetime import datetime, timedelta


"""
Models Section
"""
class ProductModel:
    """
    Product Model 
    """
    def __init__(self, name: str, price: int):
        self.id = time.time()
        self.name = name
        self.price = price

    def get_name(self):
        return self.name


class DealsModel:
    """
    Model to store data of deal
    """
    def __init__(self, item_object: ProductModel, item_count: int, time_limit: int, start_time: datetime):
        self.id = time.time()
        self.item_object = item_object
        self.item_count = item_count
        self.time_limit = time_limit
        self.start_time = start_time
        self.deal_active = True

    def update_time(self, new_time_limit: int):
        """
        Function responsibilty is to update the deal time_limit in model object
        """
        self.time_limit = new_time_limit
    
    def update_item_count(self, new_item_count: int):
        """
        Function responsibilty is to update the deal item_count in model object
        """
        self.item_count = new_item_count

    def make_deal_inactive(self):
        self.deal_active = False


class UserModel:
    def __init__(self, name: str, email: str):
        self.id = time.time()
        self.name = name
        self.email = email
        # initially user has not claimed a deal
        self.deal_claimed = False




class DealService:
    def __init__(self):
        pass

    def create_deal(self, item_object: ProductModel, item_count: int, time_limit: int, start_time: int):
        """
        API to create a deal for a specific item
        Function responsibilty is to create the deal
        """

        if not isinstance(item_object.name, str):
            raise Exception("item_name should be string")

        if not isinstance(item_count, int):
            raise Exception("item_count should be integer")

        
        if not isinstance(item_object.price, int):
            raise Exception("item_price should be integer")

        
        # timelimit should always be in mins
        if not isinstance(time_limit, int):
            raise Exception("time_limit should be integer")
        
        if not isinstance(start_time, datetime):
            raise Exception("start_time should be an instance of date time")


        # deals Model object in response
        deals_model_obj = DealsModel(item_object, item_count, time_limit, start_time)

        self.curr_deal_model = deals_model_obj

        return self
    
    def get_deal(self):
        """
        Utils model to get create deal_data dict from deals_model_instance
        """
        deal_data = {}
        deal_data["deal_id"] = self.curr_deal_model.id
        deal_data["item_name"] = self.curr_deal_model.item_object.name
        deal_data["item_price"] = self.curr_deal_model.item_object.price
        deal_data["item_count"] = self.curr_deal_model.item_count
        deal_data["time_limit"] = self.curr_deal_model.time_limit
        deal_data["start_time"] = self.curr_deal_model.start_time

        return deal_data
        

    # item count & time_limit will be passed as optional query params
    # by default value is -1
    # value of both of these vars should be +ve integer
    # so the default value is passed as -ve
    def update_deal(self, item_count=-1, time_limit=-1):
        """
        API to update the deal
        Function responsibilty is to update the deal
        """
        
        if item_count != -1 and isinstance(item_count, int):
            self.curr_deal_model.update_item_count(item_count)
        

        if time_limit != -1 and isinstance(time_limit, int):
            self.curr_deal_model.update_time(time_limit)
        
        return self

    
    def claim_deal(self, user_obj: UserModel):
        """
        Api to claim the deal
        Function responsibilty is to claim the deal for the User
        Check if all constraints satisfied before claiming the deal
        """

        if not self.curr_deal_model.deal_active:
            raise Exception("Deal has already ended")


        if user_obj.deal_claimed:
            raise Exception("User has already claimed the deal")
        
        curr_time = datetime.now()

        deal_time_limit = self.curr_deal_model.start_time + timedelta(seconds=self.curr_deal_model.time_limit)

        if curr_time > deal_time_limit:
            raise Exception("Deal time is already over")
        

        # check if count of product in deal left
        if self.curr_deal_model.item_count == 0:
            raise Exception("Item of product in deal is finished")

        self.curr_deal_model.update_item_count(self.curr_deal_model.item_count-1)

        # user has claimed the deal
        user_obj.deal_claimed = True

        return self
    

    def end_deal(self):
        """
        Api to end the deal
        Single responsibility of the function to facilitate end of deal
        """
        self.curr_deal_model.make_deal_inactive()
        print("---deal has ended---")


"""
Api handler
"""
        
class ApiHandler:
    """
    API handler which contains API signatures
    """
    def __init__(self):
        pass
    
    def create_deal(self, item_object: ProductModel, item_count: int, time_limit: int, start_time: datetime):
        """
        """
        deal_service_obj = DealService()

        response = deal_service_obj.create_deal(item_object, item_count, time_limit, start_time)
        return response
    
    def update_deal(self, curr_deal_obj, item_count=-1, time_limit=-1):
        
        response = curr_deal_obj.update_deal(item_count, time_limit)
        return response
    
    def claim_deal(self,curr_deal_obj,  user_obj: UserModel):
        response = curr_deal_obj.claim_deal(user_obj)
        return response

    def end_deal(self, curr_deal_obj):
        curr_deal_obj.end_deal()



"""
Run script section
"""

def main():
    print("hello from limited time deals app")

    print("\n")

    api_handler = ApiHandler()

    # product on which the deal is
    product = ProductModel("samsung_phone", 1000)
    print("---product on deal---")
    print(product.name)

    # deal start time
    start_time = datetime.now()

    print("\n")

    print("----current deal-----")
    # time is in seconds
    deals_object = api_handler.create_deal(product, 2, 60, start_time)

    print(deals_object.get_deal())

    print("\n")

    print("----update count of items & deal time---")
    item_count = 3
    time_limit = 80 # in seconds
    deals_object= api_handler.update_deal(deals_object, item_count, time_limit)

    print(deals_object.get_deal())

    print("\n")

    print("-----user-----")
    user_obj = UserModel("mayank", "mayank@abc.com")

    print(user_obj.name)

    print("\n")

    print("---claim deal by the user 1----")
    deals_object = api_handler.claim_deal(deals_object, user_obj)
    print(deals_object.get_deal())

    print("\n")
    print("----claim deal by User 2")
    print("\n")

    user_obj_2 = UserModel("saurabh", "saurabh@abc.com")
    print(user_obj_2.name)
    print("\n")

    deals_object = api_handler.claim_deal(deals_object, user_obj_2)
    print(deals_object.get_deal())

    # user 1 trying to claim the deal again
    # print("\n")
    # deals_object = api_handler.claim_deal(deals_object, user_obj)
    # print(deals_object.get_deal())
    
    # Pause execution for 100 seconds
    # time.sleep(100)
    # print("100 seconds have passed")

    # print("\n")
    # print("----claim deal by User 3")
    # print("\n")


    # user_obj_3 = UserModel("ms", "ms@abc.com")
    # print(user_obj_3.name)
    # print("\n")

    # deals_object = api_handler.claim_deal(deals_object, user_obj_3)
    # print(deals_object.get_deal())

    print("\n")
    print("--------End the deal------")
    print("\n")
    api_handler.end_deal(deals_object)

    print("\n")
    user_obj_4 = UserModel("tikku", "tikku@abc.com")
    print(user_obj_4.name)

    print("---claim deal by the user 4 after deal has ended----")
    deals_object = api_handler.claim_deal(deals_object, user_obj_4)
    print(deals_object.get_deal())




# API Running Section

if __name__ == "__main__":
    main()
    
    






from opsdroid.skill import Skill
from opsdroid.matchers import match_regex
from trello import TrelloClient

import yaml
with open("/Users/fre3x/project/Docker/opsdroid/trello-skill/config_trello.yaml",'r') as stream :
    config = yaml.load(stream)

class myskill(Skill):

    client = TrelloClient(
        api_key=config['trello-api']['api_key'],
        api_secret=config['trello-api']['api_secret'],
        token=config['trello-api']['token'],
        token_secret=config['trello-api']['token_secret']
    )
    
    @match_regex(r'trello board|trello board (?P<board>.*)',matching_condition="fullmatch")
    async def trello_board(self, message):
        """List trello board or choose your board for next command"""
        remember_board = message.regex.group("board")

        if remember_board != None: 
            remember_board_isdigit = False

            for chara in remember_board:
                if chara.isdigit():
                    remember_board_isdigit = True
                else:
                    remember_board_isdigit = False
                    break
            
            if remember_board_isdigit == False:
                await message.respond("board is not digit")
            else:
                await self.opsdroid.memory.put("board", remember_board)
                await message.respond("OK I'll remember that")
                
        all_boards = self.client.list_boards()
        mes = "Choose your board : "
        
        for board in all_boards:
            index_board = all_boards.index(board)
            ind = index_board.__str__()
            mes += "\n" + ind + "- " + board.name 

        
        await message.respond(mes)
    
    @match_regex(r'trello lists|trello lists (?P<lists>.*)',matching_condition="fullmatch")
    async def trello_lists(self, message):
        """List your list in trello board or choose your list for next command """ 
        remember_lists = message.regex.group("lists")

        board_memory = await self.opsdroid.memory.get("board")
        list_in_my_board = None 

        if board_memory == None:
            await message.respond("Please choose board")  
        else:
            board = int(board_memory)
            all_boards = self.client.list_boards()
             
            try: 
                my_board = all_boards[board]
                list_in_my_board = my_board.list_lists()
                mes = "\n Please choose lists :"
                for list in list_in_my_board:
                    index_list = list_in_my_board.index(list)
                    ind = index_list.__str__()
                    mes += "\n" + ind + "- " + list.name
                       
                await message.respond(mes)
            
            except IndexError:
                await message.respond("board doesn't exist")
        
        # Verify type of remember list 
        if remember_lists != None: 
            remember_lists_isdigit = False

            for chara in remember_lists:
                if chara.isdigit():
                    remember_lists_isdigit = True
                else:
                    remember_lists_isdigit = False
                    break
            
            if remember_lists_isdigit == False:
                await message.respond("lists is not digit")
            else:
                
                # Remember list id in database 
                c_list = list_in_my_board[int(remember_lists)]
                await self.opsdroid.memory.put("list", c_list.id)
                await message.respond("OK I'll remember list : " + c_list.name)

    @match_regex(r'trello list', matching_condition="fullmatch")
    async def trello_list(self, message):
        """List your cards in trello list"""

        board_memory = await self.opsdroid.memory.get("board")
        list_memory = await self.opsdroid.memory.get("list")

        # Control inputs in database 
        if board_memory == None:
            await message.respond("Please choose board") 
        if list_memory == None:
            await message.respond("Please choose list")     
        else: 
            index_board = int(board_memory)
            all_boards = self.client.list_boards()
            
            try:
                c_board = all_boards[index_board]
                c_list = c_board.get_list(list_memory)
                          
                for card in c_list.list_cards():
                    
                    # labels card : 
                    if card.labels != None : 
                        for label in card.labels :
                            label_card += label.__str__()
                    
                    # show card 
                    await message.respond("card : " + card.name + "\n labels : " + label_card)
            except IndexError:
                await message.respond("list in board doesn't exist")
    
    @match_regex(r'trello add card (?P<title>.*)', matching_condition="fullmatch")
    async def trello_add_card(self,message):
        """Add card in trello """

        title_card = message.regex.group("title")
        board_memory = await self.opsdroid.memory.get("board")
        list_memory = await self.opsdroid.memory.get("list")

        # Control inputs in database 
        if board_memory == None:
            await message.respond("Please choose board") 
        if list_memory == None:
            await message.respond("Please choose list")
        else:
            index_board = int(board_memory)
            all_boards = self.client.list_boards()
        
            c_board = all_boards[index_board]
            c_list = c_board.get_list(list_memory)
                          
            new_card = c_list.add_card(name=title_card,position="top")
            
            # save id new_card
            await self.opsdroid.memory.put("new_card", new_card.id) 
            
            await message.respond("new card create :" + new_card.name)
               





            
    

        


        
    
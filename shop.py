# a class for making simple shops for my text rpg, under testing.
from menu import Menu   

class Shop:
	def __init__(self, name=None, items={}, maxitems=5, tagline=None,main_options={}):
		self.name = name
		self.items = items
		self.maxitems = maxitems # per page
		self.current_page = 0
		self.pages = []
		self.menus = []
		self.main_menu = Menu({'title':self.name,'extra':tagline,'options':main_options})
		self.temp = None

		
	def openShop(self, div=True, blankitem=True):
		# add extra options on startup and make menus for every page
		self.setupShop(div, blankitem)

		# run main menu, a is returned through runMenu.
		a = self.main_menu.runMenu(end=False)

		# if user chooses to enter shop
		if a[0] == 'continue':
			a, self.current_page = 0, 1
			while True:

				# load up menu				
				menu = self.menus[a]
				choice = menu.printMenu(end=False)

				# check if choice is number or text
				if choice.isdigit() == True: 
					menu.runFunc(menu.returnChoice(choice))
				else: 
					index_list = menu.returnCustomText_KeyIndexes() # the indexes of options with custom text, prolly useless

					# for every option which has a custom option eg. [inv] inventory
					for index in index_list: 
						try:
							if choice != menu.options[list(menu.options.keys())[index]][2]: # if choice is not the same as custom option
								continue
						except IndexError:
							if choice != menu.options[list(menu.options.keys())[index]][1]:									
								continue						
						
						menu_num = self.changeMenuNumber(choice, a)
						if menu_num is False: break
						else:							
							a = menu_num
							continue

				if choice == 'e':
					print('you exited the shop')
					break

		# if exit from main menu 					
		else: print('you exited the shop')
			

	def changeMenuNumber(self, choice,a):
		if choice == 'n':
			if self.current_page<=len(self.pages)-1:				
				a+=1 				
				self.current_page+=1
			else:
				Menu.clean()
				print('cant go any further')			
		elif choice == 'p':
			if self.current_page!=1:
				a-=1
				self.current_page-=1
			else:
				Menu.clean()
				print('cant go any further back')
		elif choice == 'e':
			return False
		return a

	def setupShop(self,div=True,blankitem=True):
		self.fillPages(self.maxitems)
		for page in self.pages:

			# if last page, add blank items for filling empty space
			if len(page.keys())<self.maxitems:
				left_items = int(self.maxitems-len(page.keys()))

				# add blank for every left item
				for i in range(0,left_items):

					if blankitem is True:        # if blank item is set to default display blank
						a = 'blank'+str(i)
						page.update({a:'blank'})

					elif type(blankitem) is str: # if blank item is custom text display custom text
						a = blankitem+' '*i
						page.update({a:['custom']})

					else:                        # if blank item is set to False display line
						a = 'line'+str(i)					
						page.update({a:'blank'})

			# add extra options
			page.update({
							'div':'div',
							'next page':[None,'n'],
							'previous page':[None,'p'],
							'exit shop':[None,'e']

							})

			# if divider set to false
			if div is False: del page['div']

			# make menu for page and add to menus list
			menu = Menu({'title':self.name,'extra':f'Page {self.pages.index(page)+1}/{len(self.pages)}','options':page})
			self.menus.append(menu)



	def fillPages(self,maxitems=5):
		items = self.items
		total_items = len(list(self.items.keys()))
		total_pages = total_items/maxitems
		if total_pages > int(total_pages): total_pages = int(int(total_pages) + 1)
		else: total_pages = int(total_pages)

		for page_num in range(0,total_pages):
			items_for_page = self.sliceDict(items,maxitems)
			self.pages.append(items_for_page)
			for item in items_for_page.keys():
				items.pop(item)			

	@staticmethod
	def sliceDict(dictionary,index):
		sliced_dict = {}
		for i in range(0,index):
			try: key = list(dictionary.keys())[i]				
			except IndexError: continue				
			val = dictionary[key]
			sliced_dict[key] = val
		return sliced_dict



	def buyItem(self, item_and_cost): # default buyitem function, you can use your own if you want to
		cost = item_and_cost[0]
		item = item_and_cost[1]
		print('CURRENTLY BUYING:',item,'INDIVIDUAL COST:',cost)
		print('-----------------------------------')
		quantity = int(input('enter quantity to buy: '))
		cost = quantity*cost
		print('-----------------------------------')
		print('buying',item.upper(),', quantity:',quantity,', cost:',cost)
		print('-----------------------------------')

		choice = input('y/n: ')
		if choice == 'y':
			pass
		else:
			pass
		Menu.clean()

	@staticmethod
	def cont_loop(): return ['return', 'continue']		

	@staticmethod
	def exit_shop(): return ['return', 'stop']		

	@staticmethod
	def clean(): Menu.clean()
		





if __name__ == '__main__':

  shopkeeper_lines = [
              'Welcome, to my shop!, How can I help you today?',
              'A traveller I see! Where are you off to now?',
              'I make the best weapons around here, try them if you like!',
              'Quit dawdling around, get a move on!'
              ]

  def printshoplines(args): # a function to randomly print shopkeeper lines
    type_ = args[0]
    if type_ is 'talk':
      print(random.choice(shopkeeper_lines))
      pause = input('...')
      print(random.choice(shopkeeper_lines))
      pause = input('...')
      Menu.clean()

  a = Shop(	
        name="Mira's Weapon Shop'",
        items={
            'sword   - 10':[Shop().buyItem,(10,'sword')], # buyItem is just an example function, replace with your own buy function
            'bow     - 12':[Shop().buyItem,(12,'bow')],
            'hammer  - 14':[Shop().buyItem,(14,'hammer')],
            'axe     - 16':[Shop().buyItem,(16,'axe')],
            'dagger  - 18':[Shop().buyItem,(18,'dagger')],
            'mallet  - 12':[Shop().buyItem,(12,'mallet')],
            'arrows  - 14':[Shop().buyItem,(14,'blade')],
            'polearm - 16':[Shop().buyItem,(16,'saw')]
            },
        main_options={
                'Talk to the Shopkeeper':[printshoplines,('talk',None)], # ('talk',None) are the args for the function, you can add anything instead of the None, the args should be a tuple
                'Enter the Shop!':Shop.cont_loop,
                'Exit Shop':Shop.exit_shop
                },
        tagline="   Take a look around, we have the best weapons!",
        maxitems=6 # per page

      )

  a.openShop(blankitem='[]')


# kardsens

# a class to make easier menus
from os import system, name

class Menu:
	def __init__(self,info={}):
		self.info = dict(info)
		self.fill_spaces() 
		self.title = self.info['title'] 
		self.options = self.info['options'] 
		

	def fill_spaces(self):
		for missing in ['title','extra','options','start','repeat']:
			try: a = self.info[missing]
			except KeyError:
				if missing == 'options': self.info[missing] = {None:None}
				if missing == 'start' or missing == 'repeat': self.info[missing] = None
				else: self.info[missing] = ''
					

	def returnCustomText_KeyIndexes(self):
		# this returns a list with indexes of options with custom number text eg. 'inv' in '[inv] inventory' is custom number text
		index_list = []
		# check every option
		for option in self.options.keys():
			if type(self.options[option]) is list:
				try:
					a = self.options[option][2]
					index_list.append(list(self.options.keys()).index(option))
				except IndexError:
					try:
						if type(self.options[option][1]) is str: index_list.append(list(self.options.keys()).index(option))
					except IndexError:
						pass
						
		return index_list


	def returnChoice(self,choice): 

		# CHOICE RETURNED IS FUNCTION, AND ARGS ARE ARGUMENTS IN TUPLE FORM
		# CHOICE RETURNED IS NONE, IF GIVEN CHOICE WAS A STRING AND DID NOT MATCH ANY CUSTOM NUMBER TEXTS
		# CHOICE RETURNED IS FALSE, IF GIVEN CHOICE IS A NUMBER BUT BEYOND THE LIMITS OF THE LIST



		# create copy of options since we dont want to change it in any way
		options = dict(self.options)
		args = None

		# set choice to 1 if 0 because if you dont then if choice is 'p' you go to last page
		if choice == 0: choice +=1

		# remove dividers, blanks, custom texts out of options so that choosing an option is accurate
		for option in self.options.keys():
			if self.options[option] == 'div': del options[option]				
			elif self.options[option] == 'blank': del options[option]
			# if key value is a list	
			elif type(self.options[option]) is list:
				try:
					if type(self.options[option][2]) is str: del options[option]	# item 2, if it exists is always custom number text
				except IndexError:
					if type(self.options[option][1]) is not tuple: del options[option] # item 1, if list should be tuple with arguments for function, if its not then its obviously a custom number text [inv] inventory
					elif self.options[option][0] == 'custom': del options[option] # if instead of function its 'custom' its custom text

		# check if choice is not number, check if choice matches custom number text
		if choice.isdigit() is False:

			# check if each key value is a list
			for option in self.options.keys():
				# check if list contains a custom number text
				if type(self.options[option]) is list:
					# item 2 is always custom number text, if equal then change function and argument values
					try:
						if choice == self.options[option][2]:
							choice = self.options[option][0]
							args = self.options[option][1]
							return choice, args

					# if no item 2, check if choice is equal to item 1, if equal then change function value, since item 1 was not arguments dont change argument values
					except IndexError:
						if choice == self.options[option][1]:
							choice = self.options[option][0]
							return choice, args				

			# if choice matches none of custom number texts, it can safely be said that there is no choice like that
			# runMenu will check if choice is None and print 'no such option like that'
			choice = None
			return choice, args

		# if choice is number conver to int
		else:
			choice = int(choice)

		# if choice is a number, check if list even goes that far
		try: choice = list(options.keys())[choice-1]	

		# if choice is past list's limits choice is False. runMenu will check if choice is False and print 'invalid option'
		except IndexError: 
			choice = False
			return choice, args


		# if choice is a number and is in the list we can safely say that we have narrowed it down
		choice = options[choice]
		# if the option is a list then choice is then item 0 is the function and item 1 are the arguments		
		if type(choice) is list:
			args = choice[1]
			choice = choice[0]

		# if option was not list then no arguments for the function have been provided and arguments remain None

		return choice, args
	

	
	def printMenu(self,end=True,title=True,choose=True,iters=90, char='-',clear=True,space=0): 
		
		# if end is True automatically add an exit option to exit program
		if end is True: self.options['Exit'] = quit
			
		# if title is True display title and extra title
		if title is True: 
			print(' '*space+char*iters) 
			print(' '*space+self.title,self.info['extra'])
		print(' '*space+char*iters)

		# n is the number displayed before each option and increments
		n = 1

		# print options after various checks
		for option in self.options.keys():

			# DIVIDER =================================================================================

			# if key value is 'div' that means instruction is to print a divider
			if self.options[option] == 'div': print(' '*space+char*iters)


			# BLANK =================================================================================

			# if key value is 'blank' that means instruction is to print a blank line
			elif self.options[option] == 'blank':

				# if key contains 'line' print a series of dashes to signify blank line
				if 'line' in option: print(' '*space+'----------------')					
				# if key contains 'blank' print a blank character
				elif 'blank' in option: print(' ')
				# if no type is specified in key then just print blank character by default	
				else: print(' ')


			# CUSTOM =================================================================================

			# if key value is a list and item 0 is 'custom' that means instruction is to print just the key without number i.e. 'hello' instead of '[n] hello'
			elif type(self.options[option]) is list and self.options[option][0] == 'custom':
				print(f'{option}')


			# CUSTOM NUMBER TEXT =================================================================================

			# if key value is a list check if any custom number texts have been specified i.e. 'inv' in '[inv] inventory' and not n in '[n] inventory'
			elif type(self.options[option]) is list:

				# item 2 is always a custom number text if it exists, it also means the arguments for the function have been specified
				try:
					a = self.options[option][2]
					print(' '*space+f'[{a}] {option}')

				# if item 2 does not exist
				except IndexError:
					try:
						a = self.options[option][1]
						# if item 1 is a tuple that means it contains arguments and is not a custom number text, print n with option and increment by one
						if type(a) is tuple:
							print(' '*space+f'[{n}] {option}')
							n+=1
						# if item 1 exists and is not a tuple containing arguments for function then assume it is a custom number text and print it with option instead of with n
						else: print(' '*space+f'[{a}] {option}')
					
					# item 1 does not exist, so no custom number texts have been specified, print n with item 0 and increment by one
					except IndexError:
						print(' '*space+f'[{n}] {option}')
						n+=1


			# NORMAL =================================================================================

			# if item is not a divider/line/blank/custom text/custom number text/list we can safely assume no arguments have been specified and its just a function
			# print n with option and increment by 1
			else:
				print(' '*space+f'[{n}] {option}')
				n+=1


		#=================================================================================

		# after all options have been printed out:
		print(' '*space+char*iters)
		# if choose is true take automatic input from user
		if choose is True: choice = input(' '*space+'> ')
		# else choice set to nothing			
		else: choice = ''
		# if clear is true clear screen after input, KEEP ON FALSE IF CHOOSE IS FALSE BECAUSE THEN IT WILL CLEAR THE PRINTED MENU
		if clear is True: self.clean()

		#=================================================================================

		# return choice without spaces in the front or back if user has entered it like that
		return choice.strip()
			
		
	@staticmethod
	# clear the screen
	def clean():
		if name == 'nt': _ = system('cls')			
		else: _ = system('clear')
			
	def runFunc(self,func,args=None):

		# ARGUMENTS SHOULD BE IN TUPLE FORM

		# if function is None dont run
		if not func: 
			print('choice has to be a number')
			a = None
		# if args are None no arguments, only run function
		elif not args: a = func()			
		# there are arguments so run function with arguments
		else: a = func(args)

		# return whatever value returned from function			
		return a

	def runMenu(self,clear=True,end=True,title=True,iters=90,char='-',args=None,space=0):  
		# if clear is true clear screen
		if clear is True: self.clean()
		# args are to be used as args for every function, store a copy in temp_args since they might get changed if different args have been specified for a function			
		temp_args = args
		if self.info['start']:
			self.info['start']()
		while True:
			if self.info['repeat']:
				self.info['repeat']()
			# after every choice set args back to normal
			args = temp_args
			# choose should ALWAYS BE ON TRUE in runMenu or it keeps looping print menu without taking input 
			choose = True    
			# printMenu returns user choice which is fed into return choice to return appropriate function and its arguments if any specified
			choice, func_args = self.returnChoice(self.printMenu(end,title,choose,iters,char,clear,space)) 

			# if arguments have been specified change args to whatever arguments were returned
			if func_args is not None: args = func_args				
			# if choice is exit automatically set arguments to None since exit() needs no arguments
			if choice is exit: args = None

			# if clear is true clear screen after every input				
			if clear is True: self.clean()		

			# if choice was a string and didnt match any custom number texts		
			if choice is None: print('choice has to be a number')		
			# if choice was a number but didnt exist in the list of options
			elif choice is False: print('no such option')		

			# if choice is valid we can assume a function and its arguments have been returned and we can now run the function
			else: 
				# run function with arguments and take the returned value as a
				a = self.runFunc(choice,args) 

				# if 'stop' was returned that means - BREAK LOOP
				if a == 'stop': break 
				# if 'back' was returned that means - BREAK LOOP AND RUN PREVIOUS FUNCTION AGAIN - function should have a mechanism to check if it is being run again to avoid returning 'back' again
				elif a == 'back': break 
				# if list with item 0 being 'return' is returned then - BREAK LOOP AND RETURN VALUES
				elif type(a) is list: 
					if a[0] == 'return': break
		
		# run function again if function returned 'back'
		if a == 'back': a = self.runFunc(choice,args)	

		# return item 1 values if function returned a list with item 0 'return' i.e. ['return',whatever_you_want_to_return]
		elif type(a) is list:
			if a[0] == 'return': return a[1:len(a)] 
				















if __name__ == '__main__':
	def load_game():
		print('load game run')

	def new_game():
		print('new game run')

	main = Menu({
			'title':'MAIN MENU',
			'options':{'New Game':[new_game],'Load Game':load_game}	
			#'extra':'',
			#'start':the_function_you_only_need_on_first_run,
			#'repeat':repeating_function
			})

	main.runMenu()






# HOW TO USE OPTIONS

'''
'options':{'Option title to be displayed':[function,(args),custom number text]} # args must be a tuple

'options':{'Option title to be displayed':[function,(args)]}

'options':{'Option title to be displayed':[function,custom number text]} # i.e. [inv] inventory

'options':{'Option title to be displayed':function}



'options':{'div':'div','div2':'div'} # you only need a 'div' in the value, used for divider

'options':{'blank1':None,'line1':None} # if you have line in key it displays '-------'' if you have blank in key it displays ' ', needs to have 'blank' in value

'options':{'custom text':['custom']} # doesnt show number, only custom text



all custom options for menu.RunMenu():
-----------------------------------------------------------------------------------
> clear : clear screen after every input [default:True]
> choose : if enabled, automatically asks for input (only for printMenu()) [default:True]
> end : if enabled automatically adds an exit option to existing options [default:True]
> title : if enabled displays title, if not only displays options [default:True]
> iters : length of divider [default:90]
> char : character used in divider [default:'-']
-----------------------------------------------------------------------------------


# kardsens

# used to generate random terrain and print the environment around the player of a certain radius
import random

class Location:
	def __init__(self,envlist,seed=1,location=[0,0]):
		self.location = location
		self.string = None
		self.envlist = envlist
		self.seed = seed
		self.convert_location()

	def convert_location(self,location=0):
		if location != 0:
			string = str(location[0]+self.seed)+str(location[0])+str(location[1]+self.seed)+str(location[1])
			return string
		else:

			self.string = str(self.location[0]+self.seed) + str(self.location[0]) + str(self.location[1]+self.seed) + str(self.location[1])

	def change_location(self, direction, magnitude=1,coordinates=None):
		if not coordinates:
			x = self.location[0]
			y = self.location[1]
		else:
			x = coordinates[0]
			y = coordinates[1]
		if direction == 'up': y+=magnitude
		elif direction == 'down': y-=magnitude			
		elif direction == 'left': x-=magnitude			
		elif direction == 'right': x+=magnitude
			

		return (x,y)

	def move(self,direction,magnitude=1):
		if type(direction) is not tuple:
			x,y = self.change_location(direction,magnitude)[0],self.change_location(direction,magnitude)[1]
		else:
			x = direction[0]
			y = direction[1]

		self.location[0] = x
		self.location[1] = y
		self.convert_location()

	def display(self):

		print('root seed:',self.seed)
		print('location:',self.location,'quadrant',self.find_quadrant())
		print('seed:',self.string)


	def generate(self, string=0):
		if string != 0:
			random.seed(string)
		else:
			random.seed(self.string)
		env = random.choice(self.envlist)
		return env

	def surroundings_dict(self,radius=7):
		
		all_points = {}
		all_points['y'] = {}
		for direction in ['up','down']:
			all_points['y'][direction] = {}
			for i in range(1,radius):			
				yaxis_point = self.change_location(direction,i)
				all_points['y'][direction][yaxis_point] = {}
		
		for ydir in ['up','down']:
			for point in all_points['y'][ydir].keys():
				for direction in ['left','right']:	
					all_points['y'][ydir][point][direction] = []

					for i in range(1,radius):
						all_points['y'][ydir][point][direction].append(self.change_location(direction,i,point))

		all_points['y']['center'] = {tuple(self.location):{}}
		
		for direction in ['left','right']:
			all_points['y']['center'][tuple(self.location)][direction] = []
			for i in range(1,radius):
				all_points['y']['center'][tuple(self.location)][direction].append(self.change_location(direction,i))
		
		


		return all_points

	def surroundings_table(self,radius=7):
		all_points = self.surroundings_dict(radius)
		table = []
		for axis in all_points.keys():
			rownum = 0
			for ydirection in ['up','center','down']:
				point_in_direction = all_points[axis][ydirection].keys()
				if ydirection=='up':
					point_in_direction = list(point_in_direction)
					point_in_direction.reverse()
				for point in point_in_direction:
					table.append([])
					#for direction in all_points[axis][ydirection][point].keys():
					left = all_points[axis][ydirection][point]['left']
					left.reverse()
					table[rownum].extend(left)
					table[rownum].append(point)
					table[rownum].extend(all_points[axis][ydirection][point]['right'])
					rownum+=1
		return table


	def surroundings(self,radius=7,show_coords=False):
		radius-=1
		table = self.surroundings_table(radius)
		name_table = []
		rownum = 0
		for row in table:
			name_table.append([])
			for col in row:
				name_table[rownum].append(self.generate(self.convert_location(col))) # generate environment and append
			rownum+=1
		
		index = (radius + (radius-1))//2
		name_table[index][index] = name_table[index][index].name.upper()

		if show_coords:
			print('       ',end='')
			for col in table[0]:
				length = 8-len(str(col[0]))
				print(col[0],end=' '*length)
			print()
		#print()
		for row in name_table:
			if show_coords:
				length = 5-len(str(table[name_table.index(row)][0][1]))
				print('',table[name_table.index(row)][0][1],end=' '*length)
			for col in row:
				try:
					print(col.name,end=' ')
				except:
					print(col,end=' ')
			print()
			print()

		return table


	def find_quadrant(self,location=False):
		if not location:
			x = self.location[0]
			y = self.location[1]
		else:
			x = location[0]
			y = location[1]

		quadrant = None

		if x<0 and y<0: quadrant = 3
		elif x<0 and y>0: quadrant = 2			
		elif x>0 and y<0: quadrant = 4			
		elif x>0 and y>0: quadrant = 1
			

		return quadrant
		












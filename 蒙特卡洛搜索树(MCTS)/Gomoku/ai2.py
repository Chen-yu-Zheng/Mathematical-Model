from status import *
import random
import math
from settings import *
import copy

PATH = set(range(1, SIZE * SIZE + 1))	#PATH代表全局的格点。有SIZE*SIZE大小的棋盘（二维列表）一一映射到一维集合

def game_end():
	"""
	棋局是否终结是判断是否执行完一次蒙特卡洛搜索的依据，本函数判断棋局是否终结。
	返回（是否终局，赢家）
	终局为True
	赢家为1代表人类玩家或AI玩家1
	赢家为2代表AI玩家2
	"""
	for i in range(1, SIZE - 3):
			for j in range(1, SIZE - 3):
				if (status_matrix[i][j] == 1 and status_matrix[i + 1][j] == 1 and status_matrix[i + 2][j] == 1 and status_matrix[i + 3][j] == 1 and status_matrix[i + 4][j] == 1) or \
					(status_matrix[i][j] == 1 and status_matrix[i][j + 1] == 1 and status_matrix[i][j + 2] == 1 and status_matrix[i][j + 3] == 1 and status_matrix[i][j + 4] == 1) or \
					(status_matrix[i][j] == 1 and status_matrix[i + 1][j + 1] == 1 and status_matrix[i + 2][j + 2] == 1 and status_matrix[i + 3][j + 3] == 1 and status_matrix[i + 4][j + 4] == 1):
					return True, 1

	for i in range(SIZE - 3, SIZE + 1):
		for j in range(1, SIZE - 3):
			if status_matrix[i][j] == 1 and status_matrix[i][j + 1] == 1 and status_matrix[i][j + 2] == 1 and status_matrix[i][j + 3] == 1 and status_matrix[i][j + 4] == 1:
				return True, 1

	for j in range(SIZE - 3, SIZE + 1):
		for i in range(1, SIZE - 3):
			if status_matrix[i][j] == 1 and status_matrix[i + 1][j] == 1 and status_matrix[i + 2][j] == 1 and status_matrix[i + 3][j] == 1 and status_matrix[i + 4][j] == 1: 
				return True, 1

	for i in range(1, SIZE - 3):
		for j in range(1, SIZE - 3):
			if (status_matrix[i][j] == 2 and status_matrix[i + 1][j] == 2 and status_matrix[i + 2][j] == 2 and status_matrix[i + 3][j] == 2 and status_matrix[i + 4][j] == 2) or \
				(status_matrix[i][j] == 2 and status_matrix[i][j + 1] == 2 and status_matrix[i][j + 2] == 2 and status_matrix[i][j + 3] == 2 and status_matrix[i][j + 4] == 2) or \
				(status_matrix[i][j] == 2 and status_matrix[i + 1][j + 1] == 2 and status_matrix[i + 2][j + 2] == 2 and status_matrix[i + 3][j + 3] == 2 and status_matrix[i + 4][j + 4] == 2):
				return True, 2

	for i in range(SIZE - 3, SIZE + 1):
		for j in range(1, SIZE - 3):
			if status_matrix[i][j] == 2 and status_matrix[i][j + 1] == 2 and status_matrix[i][j + 2] == 2 and status_matrix[i][j + 3] == 2 and status_matrix[i][j + 4] == 2: 
				return True, 2

	for j in range(SIZE - 3, SIZE + 1):
		for i in range(1, SIZE - 3):
			if status_matrix[i][j] == 2 and status_matrix[i + 1][j] == 2 and status_matrix[i + 2][j] == 2 and status_matrix[i + 3][j] == 2 and status_matrix[i + 4][j] == 2:
				return True, 2

	for i in range(1, SIZE - 3):
			for j in range(5, SIZE + 1):
				if status_matrix[i][j] == 1 and status_matrix[i + 1][j - 1] == 1 and status_matrix[i + 2][j - 2] == 1 and status_matrix[i + 3][j - 3] == 1 and status_matrix[i + 4][j - 4] == 1:
					return True, 1
	for i in range(1, SIZE - 3):
		for j in range(5, SIZE + 1):
			if status_matrix[i][j] == 2 and status_matrix[i + 1][j - 1] == 2 and status_matrix[i + 2][j - 2] == 2 and status_matrix[i + 3][j - 3] == 2 and status_matrix[i + 4][j - 4] == 2:
				return True, 2

	return False, 0


class TreeNode(object):
	"""
	蒙特卡洛搜索树的结点数据结构
	x为结点在棋盘上的横坐标
	y为节点在棋盘上的纵坐标
	parent为双亲结点，即上一步落子
	children为子节点,即下一步落子
	type为该节点的落子类型，分为1（人类或ai1）和2（ai2）
	n_win为该节点的历史获胜次数
	n_visit为该节点历史被访问次数
	C为UCT公式中的超参数，需要根据实际情况进行调参
	path为当前已经走过的路径
	"""
	def __init__(self, parent, x = 0, y = 0):
		
		self.parent = parent
		
		self.x = x
		self.y = y
			
		#root为当前落子前的局面，即蒙特卡洛搜索树初始化的根
		if self.is_root():
			self.type = 1
		else:
			if self.parent.type == 1:
				self.type = 2
			else:
				self.type = 1

		self.children = []
		self.n_visit = 0
		self.n_win = 0


		#记录每个节点下，棋盘上已经走过的地方，防止重复走位
		if self.is_root():
			#记录根节点情况已经下过的路径，即当前棋盘上已经落下的子
			self.path = set()
			for i in range(1,SIZE + 1):
				for j in range(1,SIZE + 1):
					if status_matrix[i][j] != 0:
						self.path.add(SIZE*(j-1) + i)
		else:
			#如果不是根节点，那么该节点记录的路径为双亲结点带有的路径和本节点的落子之和
			self.path = self.parent.path.union({SIZE*(self.y-1) + self.x})



	def get_value(self, C):
		"""
		获得每个节点的UCT值，用于选择阶段的扩展标准。
		UCT值越高，越优先被蒙特卡洛树选择
		"""
		root = self
		#递归找到获得根节点
		while  root.parent != None:
			root = root.parent

		UCB = C * math.sqrt(math.log(root.n_visit) / self.n_visit)

		#由极大极小原则，要分两种情况计算V
		#若为我方落子，则直接认为是 self.n_win / self.n_visit
		#否则，进行正向化，为V = 1 - 1.0* self.n_win / self.n_visit

		if self.type == 2:
			V = 1.0* self.n_win / self.n_visit
			return UCB + V

		elif self.type == 1:
			V = 1 - 1.0* self.n_win / self.n_visit
			return UCB + V
		else:
			print('Get value wrong')


	def select(self, C):
		"""
		选择阶段，从孩子列表中选择UCT值最高的节点
		"""
		maxindex = 0
		next_x, next_y = self.children[0].x, self.children[0].y
		for i in range(1, len(self.children)):
			if self.children[maxindex].get_value(C) < self.children[i].get_value(C):
				maxindex = i 
				next_x, next_y = self.children[i].x, self.children[i].y

		return maxindex, next_x, next_y 

		

	def expend(self,C):
		"""
		拓展阶段，即选出蒙特卡洛树下一步拓展的叶子节点
		分为两种情况：
		1.如果当前节点仍有能够拓展的子节点，那么随机选择一个进行拓展，加入当前节点的孩子列表
		2.当前节点的所有能拓展的子节点都被拓展过了，那么进行递归操作，利用UCT函数进行选择，知道遇到某个节点存在未拓展
		的子节点，转到1
		"""
		path_remain = PATH.difference(self.path)
		for i in range(len(self.children)):
			path_remain = path_remain.difference(self.children[i].path)


		#情况1
		if len(path_remain) == 0:
			nextindex, next_x, next_y = self.select(C)
			status_matrix[next_x][next_y] = self.children[nextindex].type
			return self.children[nextindex].expend(C)


		#情况2
		else:
			coor_expend = random.sample(path_remain,1)[0]
			path_remain.remove(coor_expend)


			#将一维数据转化成对应的二维坐标
			if coor_expend % SIZE == 0:
				y_expend = coor_expend // SIZE
				x_expend = SIZE
			else:
				y_expend = (coor_expend // SIZE) + 1
				x_expend = coor_expend % SIZE

			node_expend = TreeNode(self, x_expend, y_expend)
			self.children.append(node_expend)

			#模拟落子
			if node_expend.type == 1:
				status_matrix[x_expend][y_expend] = 1
			else:
				status_matrix[x_expend][y_expend] = 2 
			return node_expend


		

	def update(self, if_win):
		"""
		迭代更新
		历史访问次数加一
		如果获胜，胜利次数加一
		如果未获胜，则不加
		将模拟落下的子记录清空
		"""
		self.n_visit += 1
		self.n_win += if_win
		status_matrix[self.x][self.y] = 0


	def update_recursive(self, if_win):
		"""
		从拓展的子节点，到双亲结点，然后一直递归到根节点
		进行反向传播
		"""
		if self.parent != None:
			self.parent.update_recursive(if_win)
		self.update(if_win)
		

	def is_root(self):
		return self.parent == None

	def is_leaf(self):
		return self.children == []
		
		





def computer_strategy(C = C, n_playout = N_PLAYOUT):
	# 接口位于game.py第507行

	root = TreeNode(None)

	#测试使用
	# print("????????------------")
	# print('root path: ')
	# print(root.path)
	# print(PATH)
	path_can_choose = list(PATH.difference(root.path))

	#进行n_playout次模拟
	for n in range(n_playout):

		#拓展
		node_expend = root.expend(C)

		#记录当前下子者
		last_player = node_expend.type

		#开始模拟随机走子
		path_can_choose_after_expend = PATH.difference(node_expend.path)
		while True:

			#如果终局，那么结束
			end, winner = game_end()
			if end:
				break

			#棋盘未满时
			if len(path_can_choose_after_expend) > 0:
				coor_next = random.sample(path_can_choose_after_expend,1)[0]
				path_can_choose_after_expend.remove(coor_next)

				if coor_next % SIZE == 0:
					y_next = coor_next // SIZE
					x_next = SIZE
				else:
					y_next = (coor_next // SIZE) + 1
					x_next = coor_next % SIZE

				if last_player == 1:
					status_matrix[x_next][y_next] = 2
					last_player = 2
				else:
					status_matrix[x_next][y_next] = 1
					last_player = 1


			#和棋情况
			else:
				# print('Full')
				winner = 1
				break

		#记录胜负情况
		if winner == 2:
			if_win = 1
		else:
			if_win = 0


		#测试代码
		# print("if_win: " + str(if_win))
		# for i in range(1,SIZE + 1):
		# 	for j in range(1,SIZE + 1):
		# 		print(status_matrix[j][i], end= ' ')
		# 	print()
		# print()
		# print()


		#反向传播
		node_expend.update_recursive(if_win)


		#重建root时的状态，清除模拟落子
		for i in range(len(path_can_choose)):
			coor_i = path_can_choose[i]
			x_i = y_i = 0
			if coor_i % SIZE == 0:
				y_i = coor_i // SIZE
				x_i = SIZE
			else:
				y_i = (coor_i // SIZE) + 1
				x_i = coor_i % SIZE

			status_matrix[x_i][y_i] = 0



	#选择root子节点中被访问次数最多的子，他就是我们下一步落子，返回它
	maxindex = 0
	next_x, next_y = root.children[0].x, root.children[0].y
	for i in range(1, len(root.children)):
		if root.children[maxindex].n_visit < root.children[i].n_visit:
			maxindex = i 
			next_x, next_y = root.children[i].x, root.children[i].y

	return  next_x, next_y














import pygame
from game import *





if __name__ == '__main__':
	g = Game()
	# function to start the game
	g.show_start_screen()
	while g.running:
	    # start a new game
	    g.new()
	    
	    # function shows gmae over
	    g.show_go_screen()
	        
	    

	pygame.quit()






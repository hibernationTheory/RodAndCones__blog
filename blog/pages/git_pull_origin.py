import os

def main():
	CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
	os.chdir(CURRENT_PATH)
	os.system('git pull origin')

if __name__ == '__main__':
	main()
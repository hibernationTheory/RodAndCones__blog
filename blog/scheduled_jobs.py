import imp
import os

def main():
	CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
	tasks_data = [
		os.path.join(CURRENT_DIR, "pages/git_pull_origin.py"),
		os.path.join(CURRENT_DIR, "get_gists_from_user.py"),
		os.path.join(CURRENT_DIR, "get_images.py")
	]
	
	for i in enumerate(tasks_data):
		index = i[0]
		task_path = i[1]
		task = imp.load_source('module_' + str(i[0]), task_path)
		task.main()

if __name__ == '__main__':
	main()
# Modular Django

I am not a Django guru by any means but I have used it enough to get opinionated about certain aspects of it. One feature of Django that doesn’t cut it for me is the concept of 'apps'. For a concept that is there for the sake of modularity, I find it to yield solutions that are extremely coupled with your host project by default ( one reason being the horrendous directory structure that it creates). 

Recently I started to place all the static and template folders for a given app inside the root app folder which helps with creating self-contained - modular - apps but I wanted to take it to next step. I wanted to have an app that can function as a stand-alone project if I wanted it to. It was surprisingly easy to achieve what I was looking for.

Essentially, I just ended up moving my ‘app’ from the main project and create a new project that only contains this removed app. And then referenced this new project in the main project through a git ‘fake submodule’.

Here are some things to keep in mind:

- You need to make sure that you have references to the relevant folders of the app that is being inserted into the main project in the settings.py of the main project. This simply means that you will need to have variables that points to the static, template folders of the newly inserted external app. And also you need to refer to the app by it’s name in the installed_apps tuple.

- Similarly, the urls.py file will also need to point to the url file in the newly inserted file. 

- The static folders for this newly inserted project (and any other project to be clear) needs to be referenced inside your webserver too.

-  Making this newly inserted app to be in sync with it’s stand alone incarnation was maybe the most challenging aspect of it. It seems like there are many answers to this problem with 'git submodules' and 'git subtrees' are being two prominent ones. I opted for the simplest solution I can find which is a method called ‘fake git submodules’. You basically clone a project to a folder and add the folder to your existing git repo with the *trailing slash included*, such as:

```
$ cd my-project 
$ git clone <subproject-url> my-subproject 
$ git add my-subproject/
```
[Here is the link for this technique] (http://debuggable.com/posts/git-fake-submodules:4b563ee4-f3cc-4061-967e-0e48cbdd56cb)

This allows for git to track this `<my-subproject>` separately. It doesn’t offer any extra features but it was the easiest solution to get started with.

I am pretty sure this method comes with it's own limitations. For example I am not quite sure how you would manage the databases for each contained app at that point. But in my case I am not using databases anyway.

Here are some other random stuff I ended up learning:

- If you end up deciding to change the name of of your django project by simply changing folder names, there are couple of more places where you would need to update the references to this name. One of these is in manage.py file that others are in the wsgi and settings.py files in the settings folder.

- I am somewhat ashamed to admit that I didn't know this was a legit module import pattern in Python:
```
from . import x
```
where . imports from the current directory. I am wondering but yet to discover if a pattern like `from ../` would also work.

- requests is an excellent Python library that you should be using if you are interfacing with API’s or even just with internets. It made making API queries a breeze and helped me download files in a given url with great ease. I am hoping to use it for future projects: (http://www.python-requests.org/en/latest/) 
You can just send a get request and parse the resulting json like:
``` 
response = requests.get(url)
if response.ok:
	response.json()
#or to download a file:
chunk_size = 20
with open(file_path, ‘wb’) as fd:
	for chunk in response.iter_content(chunk_size):
		fd.write(chunk)
```

- I was convinced this was the way to get the current directory:
`os.getcwdu()`
I was mistaken. This seems to do the trick:
`os.path.dirname(os.path.realpath(__file__))`

- a relatively late epiphany I had: You can't just create folders inside your app like 'static', 'templates' and put your files in there. It might work for a single app, but if you are working with multiple projects, Django loaders won't be able to tell, say, which index.html you are looking among all the template paths that the host app might have. So you still need to create a root folder for your static and template files that would differentiate your path from the other ones that might be present in the host app. So in short, don't do this:
	- templates/index.html

	but do this:
	- templates/`<my_projects_name>`/index.html
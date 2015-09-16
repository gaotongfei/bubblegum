# bubble

bubble is a forum which is built by [Flask](http://flask.pocoo.org/).

v0.9 has been released, it's a pre-released version without a admin interface.

demo site: [http://bubble.gaotongfei.com](http://bubble.gaotongfei.com)

### How to run locally?

#### Dependencies(Ubuntu)
```
sudo apt-get install python python-pip virtualenv
```

```
git clone https://github.com/gaotongfei/bubble.git
cd bubble
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python manager.py runserver
```

### Tech Stacks
* bootstrap 
* flask
* mysql
* redis


### Features
* post topics of course
* create nodes(admin only)
* full text search(only for topics' title and body)
* markdown support
* save the topics you like

### Todos
* beautify front-end styles
* admin interface(for now, you can only delete topics by manually type `<yoursiteurl>/delete/<topic_id>`)
* more features, like, i don't know...


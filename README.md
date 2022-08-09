## PyPi [at specific date]

This tool allows you to reproduce the PyPi repository at a specific date.

### Why would you need this? 
Trying to run an old legacy code is no fun. Especially when its author is long gone, and dependencies aren't 
provided with specific versions.

Usually, it's pretty easy to find out the time the codebase was written. With this, you can use PipAT to install
needed packages in versions that would be the latest for that specific moment.

### How it works
Let's say you're dealing with code written on 24 Feb 2016. All you need is to run PipAT, and use it as an index:
```
docker run --env PORT=8000 -p 8000:8000 lvoloshyn/pipat:latest
pip install -i http://localhost:8000/2016-02-24/ -r requirements.txt
pip install -i http://localhost:8000/2016-02-24/ pandas
```

# Web Status Checker Agent

This project checks the HTTP status codes of all links found on a given webpage.
It uses a web crawler approach to extract and validate links 

## Getting started

To install this you can either use docker or just install all the dependencies for python and then run the code

### Set up BarkoAgent (Lalama)

Once you have done that, you will get an agent running in a websocket configuration. Now you need to:


1. Navigate to https://chat.barkoagent.com/ 
2. Press on the drop down for project
3. Click on `Create project`
4. Add project name, select Project Type = Custom Agent
5. Copy the `Agent WS URI endpoint` value to use it for the Custom Agent python command (add it to the .env file in the project)
6. add the system prompt (for this project there already is a prompt created in [here](system_prompt.txt))
7. Click save and publish and you will be all set to talk with your agent


### Run with docker

First add to the .env file the value from `Agent WS URI endpoint` that you got from point 5 during BarkoAgent setup.

then in simple-agent directory run:

<pre>
    docker-compose up
</pre>

### Run with python

Make sure you are using a Py-TestUI suported version python (3.9-3.12)

<pre>
    pip install -r requirements.txt
    python client.py
</pre>

It will not ask you to input the BACKEND_WS_URI from  `Agent WS URI endpoint` since it is already stored in .env file

## Your first prompt

You can test this custom agent by writing:

`run checker on this website https://www.testdevlab.com with internal crawling on and max depth 2, do not give each websites result just overall percentage of 200/400/500 or any other errors. Include statistics like total amount of links checked and percentage of those which got errors and which errors were most frequent.`
# BAwebStatusCheckerAgent

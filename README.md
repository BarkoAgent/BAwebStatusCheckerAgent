# Simple Agent

This is a simple agent that only gives the time, and has one single function defined

## Getting started

To install this you can either use docker or just install all the dependencies for python and then run the code

### Set up BarkoAgent (Lalama)

Once you have done that, you will get an agent running in a websocket configuration. Now you need to:


1. Navigate to https://stg-lalama.tdlbox.com/chat (for beta features) or https://lalama.tdlbox.com/chat
2. Press on the drop down for project
3. Click on `Create project`
4. Add project name, select Project Type = Custom Agent
5. Copy the `Agent WS URI endpoint` value to use it for the Custom Agent python command
6. add the system prompt (we have added sample system prompt for this project in [here](system_prompt.txt))
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

It will ask you to input the BACKEND_WS_URI from  `Agent WS URI endpoint`

## Your first prompt

You can test this custom agent by writing:

`Give me the time`
# BAwebStatusCheckerAgent

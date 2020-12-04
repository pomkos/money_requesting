# Table of Contents

1. [Description](#payme)
2. [How-To](#how-to)
    1. [Test it](#test-it)
    2. [Host it](#host-it)
3. [Screenshots](#screenshots)
    1. [Autofilled Venmo Request](#autofilled-venmo-request)
    2. [Default View with Inputs](#default-view-with-inputs)
    3. [Default View without Inputs](#default-view-without-inputs)
    4. [Expanded Page](#expanded-page)

# PayMe
Just a simple repo to calculate how much to request from people after a night out

# How-To
## Test it
To run in "dev" mode:

1. Clone this repo `git clone https://github.com/pomkos/payme`
2. Create a new conda environment with python 3.6, then install the libraries
  ```bash
  conda create --name tip_env python=3.6
  conda activate tip_env
  cd payme
  pip install -r recommendations.txt
  ```
3. Run within the environment, it will be accessible at localhost:8501
  ```bash
  streamlit run tip_script.py --server.port 8512 
  ```
  
## Host it
To run in dev mode, just in the background:

* Create the following script
```
#!/bin/bash

source ~/anaconda3/etc/profile.d/conda.sh

cd /dir/to/payme
conda activate tip_env # activate the new conda env

nohup streamlit run tip_script.py --server.port 8512 & # run in background
```
* Make it executable with `chmod +x payme.sh`
* You can exit the terminal and streamlit will continue serving the python file. 
* Cronjob to have the server start at each reboot:
```bash
crontab -e
@reboot /home/peter/scripts/payme.sh #add this line at the bottom
```

# Screenshots

## Autofilled Venmo Request
<img src="https://github.com/pomkos/payme/blob/main/images/venmo.png" width="620">

## Default View with Inputs
<img src="https://github.com/pomkos/payme/blob/main/images/yes_input.png" width="620">

## Default View without Inputs
<img src="https://github.com/pomkos/payme/blob/main/images/no_input.png" width="620">

## Expanded Page
<img src="https://github.com/pomkos/payme/blob/main/images/whole_page.png" width="620">


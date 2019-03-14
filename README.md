####Create an Virtual Environment

Create an virtual environment using below command

    virtualenv tv_venv
    
Activate virtual environment using below command

    source tv_venv/bin/activate
    
####Install Requirements

Install requirements using below command in activated virtual environemt.

    pip install -r requirements.txt


#### Run Application
##### Run the application using either of below commands

`Run with Twistd and with required port`

        python run_app.py -w twistd -p 5005 (runs on 5005 port)

`Run with Tornado and with required port`

        python run_app.py -w twistd -p 5005 (runs on 5005 port)

`Run with Python command`

        python run_app.py (by defaults runs on 1402 port)
        python run_app.py -p 6060 (runs on 6060 port)
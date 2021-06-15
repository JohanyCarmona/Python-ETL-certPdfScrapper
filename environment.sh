#Generate Virtual Environment
virtualenv -p python3 environment
source environment/bin/activate
pip3 install -r requirements.txt
deactivate

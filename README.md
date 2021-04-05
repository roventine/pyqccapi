# <h1> pyqccapi<sub><sub><sup>is a simple component for human to use qcc(企查查) api .</sup></sub></sub></h1><br>

### Installation

First of all we have to install it:
```Shell
pip install pyqccapi
```
I recommend using the parameter ``-i https://pypi.douban.com/simple`` via the the installation above in person.



### Requirements

1. python >= 3.6
2. requests
3. pywildcard
4. Logbook
5. PyYAML



### Sample  

Create a config.yaml :
```Shell
appkey:
    <your-appkey-here>
seckey:
    <your-seckey-here>
```

```Python
# setup config file

Environment(path_config_file)

# method_id could be found by using ApiConfig.to_instance().view_method_detail('*工商*')
method_id = '5a836c40-0888-40ad-99bc-5cf181f6a1f7'

# prepare parameters
params = {
    'keyword': '长风',
    'provinceCode': 'SH'
}

# initialize a task and invoke by 
task = task = ApiInvoker(Task(method_id, params)) \
        .invoke() \
        .to_task()

 # print result
if task.success:
  print(task.data)

```




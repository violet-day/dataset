
## install
* code in /data/quant
* supervisor config is /etc/supervisord.d

>>>
wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
https://googlechromelabs.github.io/chrome-for-testing/#stable
>>>

> kill $(ps aux | grep 'chrome' | awk '{print $2}')

> https://getwebdriver.com/chromedriver#stable
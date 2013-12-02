####add your own tumblr keys: 

- Create a file named `tumblrkeys.py` in root directory to these files

- Add keys from [tumblr api](http://www.tumblr.com/docs/en/api/v2) to file as:
```
	_CONSUMER =   <YOUR CONSUMER KEY>
	_SECRET =     <YOUR SECRET KEY>
	_TOKEN =      <YOUR TOKEN>
	_TOKEN_S =    <YOUR SECRET TOKEN>
```

- Only a few methods currently, run from command line, output will be a .csv file

- `stats_to_csv()` gets followed tumblr blogs posts and annotates based on their tags, outputs to a csv file.

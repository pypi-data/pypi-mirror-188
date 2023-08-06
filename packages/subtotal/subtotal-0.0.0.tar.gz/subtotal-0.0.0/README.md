# subtotal
Get subdomains for a url from virustotal.com without an api key. <br>
Install with:<br>
<pre>
pip install subtotal
</pre>

This package contains a cli tool called "subtotal".<br>
It uses selenium to gather a list of subdomains for a given website.<br>
You can use either Firefox or Chrome, but the appropriate webdriver
needs to be installed in your current working directory or in your PATH.<br>
Firefox runs headless, but Chrome has to run in a visible browser window.<br>
<br>
Usage:
<pre>
>subtotal -h
usage: subtotal.py [-h] [-o OUTPUT_FILE] [-b BROWSER] url

positional arguments:
  url                   The url to find subdomains for.

options:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Output file to dump subdomains to. If unspecified, a folder named "subtotals" will be created in your current working directory and the results will be saved to {url}-subdomains.txt
  -b BROWSER, --browser BROWSER
                        Browser for selenium to use. Can be "firefox" or "chrome". The appropriate webdriver needs to be installed in your current working directory or in your PATH.
</pre>
<h1>Nederland Weer</h1>

<h3>Install</h3>
<ol>
<li>Copy .env.example to .env and fill in the fields.</li>
<li>Make a virtual environment and install the requirements.</li>
<li>Add the data files to the data folder.</li>
<li>Run npm ci (with a global node and npm). When you are using PyCharm 
link the SCSS File Watcher and the UglifyJS File Watcher to the node_modules/.bin binaries. 
The files in static/scss must compile to minimized files in static/css 
and the scope of SCSS must be the scss folder. The files in static/js must compile to minimized files in static/dist 
and the scope of UglifyJS must be the js folder.</li>
<li>Run sudo locale-gen nl_NL.UTF-8</li>
<li>Run run-tests.sh to test.</li>
</ol>

## Usage
tbd

## Environment Setup
1. Install ``requirements.txt`` using ``pip install -r requirements.txt``
2. Install ``wkhtmltopdf``:

MacOS: 
```
curl -L https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-2/wkhtmltox-0.12.6-2.macos-cocoa.pkg -O
sudo installer -pkg wkhtmltox-0.12.6-2.macos-cocoa.pkg -target ~
```
Debian/Ubuntu:
```
apt-get install wkhtmltopdf
Windows: 
```
choco install wkhtmltopdf
```

create ``.env.json`` file with following template:

for ipv4 
```json
{
	"host": "0.0.0.0",
	"port": 8123,
	"debug": true
}
```

for ipv6
```json
{
	"host": "::",
	"port": 8123,
	"debug": true
}
```

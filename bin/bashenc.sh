
if [ "$1" -eq '1' ]; then
	openssl enc -rc4 -A -base64 -in "$2" -out "$4" -K "$3"
else
	openssl enc -rc4 -d -A -base64 -in "$2" -out "$4" -K "$3"
fi

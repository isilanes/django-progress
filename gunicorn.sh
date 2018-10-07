# Define variables:
PORT=$1
NAME=WebProgress
GUNICORN=gunicorn
DBDIR=$HOME/db/$NAME
ACCESS_LOG=$DBDIR/access.log

if [[ "x$1" == "x" ]]; then
    PORT=8081
fi

# Monitor log on screen:
tail -n 0 -f $ACCESS_LOG &

# Start Gunicorn server:
echo Starting Gunicorn...
exec $GUNICORN $NAME.wsgi:application \
    --name $NAME \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --log-level=info \
    --log-file=$DBDIR/gunicorn.log \
    --access-logfile=$ACCESS_LOG

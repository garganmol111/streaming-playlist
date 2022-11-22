if [ $# -ne 1 ]
then
    echo "usage: ./startserver.sh env_name";
    exit 1;
fi

pkill -f runserver
lsof -t -i tcp:8000 | xargs kill -9
conda run -n $1 --live-stream python manage.py runserver&
sleep 5
echo "Server Started";
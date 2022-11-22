if [ $# -ne 1 ]
then
    echo "usage: ./firsttime.sh env_name";
    exit 1;
fi

conda create -n $1 python=3.8 -y
conda run -n $1 --live-stream pip install -r requirements/local.txt
conda run -n $1 --live-stream python manage.py makemigrations
conda run -n $1 --live-stream python manage.py migrate
pkill -f runserver;
lsof -t -i tcp:8000 | xargs kill -9
conda run -n $1 --live-stream python manage.py runserver&
sleep 5
echo "Setup Completed";
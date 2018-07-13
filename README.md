# WNJ Wedding site for Nick and Juliette

This is a project of a website for the wedding of main character of the Grimm series: 
Nick Burkhardt and Juliette Silverton.

You can temporally see a demo [here](https://wnj.herokuapp.com/).


## How to set up the local environment?

1. Clone this repository.
2. Create a virtualenv with Python 3.6.
3. Activate the virtualenv.
4. Install the requirements.
5. Setup the instance with .env
6. Run the tests.

```console
git clone git@github.com/jrenato7/wnj.git wnj
cd wnj
python -m venv .wnj
source .wnj/bin/activate
pip install -r requirements.txt
cp contrib/env-sample .env
python manage.py test 
```

## How to deploy?

1. Create an instance on Heroku.
2. Send the settings to Heroku.
3. Set a secure SECRET_KEY to the instance.
4. Set DEBUG=False
5. Set the aws credentials.
6. Set the aws bucket.
7. Send the code to Heroku.


```console
heroku create my_instance
heroku config:push
heroku config:set SECRET_KEY=`python contrib/secret_gen.py`
heroku config:set DEBUG=False
heroku config:set AWS_USER=<your aws user IAM>
heroku config:set AWS_ACCESS_KEY_ID=<your aws key ID>
heroku config:set AWS_SECRET_ACCESS_KEY=<your aws secret access key>
heroku config:set S3_BUCKET_NAME=<the bucket name>
git push heroku master --force 

```
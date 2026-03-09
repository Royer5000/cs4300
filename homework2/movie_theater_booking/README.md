Project Name: movie_theater_booking
Created by: Jayden Royer

AI Disclosure:
I utilized Microsoft Copilot to assist with resolving errors in my project



Setup Instructions:
You can access the application through Render by using this link:

https://mysite-b2np.onrender.com

From here, you should be able to access the functionality of the application, selecting a movie, bookings seats, and viewing booking history.


You can also host the application yourself via Render by running the following commands:

git clone https://github.com/Royer5000/cs4300.git
cd cs4300/homework2/movie_theater_booking
python3 -m venv myenv --system-site-packages
source myenv/bin/activate
pip install -r requirements.txt

After running these commands, your local environment should be ready to be deployed through Render, using the render.yaml file. You can use this documentation to setup a Render Blueprint:
https://render.com/docs/deploy-django

You could also host your app locally using this command:
python -m gunicorn mysite.asgi:application -k uvicorn.workers.UvicornWorker
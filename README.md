# Beyond Test

###Installation
1.install/create virtualenv

2.install the modules(see requirements.txt)

3.activate virtualenv

4.check if everyhting is install using `pip freeze`

####Running the program

1. Change the database information in the following file `gen_data.py`, `main.py`, and in the modules folder `main_objs.py`

2. Change the url variable in `main.js` and `login.js` in the static directory with your `IP`.

3. Run `python gen_data.py`. This will create the database, tables and generate dummy data.

4. Run `pyhton main.py`

5. In your Browser, type the following address `http://localhost:5000/beyond_login` or `your_ip/beyond_login`. The website is currently running live (http://herbportal.ddns.net/beyond_login)

6. The login page should be loaded properly. If there are some problems check the step 1-3 is completed properly.

###Usage

1. User can create a battle and choose the start and end in the `View Hashtags` page

2. User can start/modify/delete a battle in the `Manage Battle` Page


###Notes

1. There are only two fixed users for this page. Therefore the hash tags battles are only between these users.

2. Token is being pass and validated in the url as a simple security besides the login. This can be improve by adding session expirations

3. Token table can be improved by adding a check in place to validated the token base on today's date

4. Battle table can be improved by adding a column that supports array where the typo hashtags can be inserted
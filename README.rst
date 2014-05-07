+++++++
WARNING - not yet implemented (in flask), so dont be dissapointed if you clone
+++++++

    ++++++++++++++
    flask-basehead
    ++++++++++++++


    -------------
     description
    -------------

    add features from basecamp-next api
    into your flask powered website with
    the basehead basecamp-api wrapper



    ======
    Usage:
    ======

    setup basecamp account:
    -----------------------
    from flask.ext.basehead.security import get_auth

    BASECAMP_ACCOUNT_NUMBER = 'your account number'
    BASECAMP_USERNAME = 'your login'
    BASECAMP_PASSWORD = get_auth() # this function keeps you from putting your pw in your
                                   # settings file, read the code to find out how to use it
                                   # or just put your pw

    
    create an app:
    --------------

    app = Flask(__name__) # or however
    app.config.from_object(__name__)

    then:
    ------

    from flask.ext.basehead import BaseCamp
    basecamp = BaseCamp(app)

    or
    ---

    basecamp = BaseCamp()
    
    then later:
    ------------

    basecamp.init_app(app)


    now:
    ====

    basecamp.get_me() or just basecamp.me
    --------------------------------------
    returns a dict with your accounts info

    basecamp.get_all_projects() 
    -------------------------------
    returns all active projects for account

    basecamp.get_my_projects(), basecamp.my_projects, or 
    me.get_my_projects(), me.my_projects 
    -------------------------------------------------
    returns all active projects for you



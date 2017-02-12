Online JavaScript Game Store Plan
=================================

## NOTE: ##

This was a school project.

## Team: ##

* Lauri Telama
* Joona Haavisto
* Eetu Vilkki

## Goal: ##

Our goal is to create a working, intuitive and seamless online javascript game store. The service will allow two types of users: players and developers. Players can buy games on our service and play bought games. Developers can add their games to the service and set a price for their game. The games are added to the store by giving an url to an html file that contains the game.

Three essential goals we strive to complete are strong security, high quality and excellent reusability.


## Plans: ##

The project will be done by using JavaScript, JQuery, HTML and CSS with Bootstrap library. In the backend we will use Django.

### Features: ###

User registration/login/logout (both as player and developer)

* Email validation
* Django auth
* We will use the built-in User model in Django and extend it if needed

Basic player functionalities

* Players can buy games. Payment is handled by a mockup service.
* Players can also play games on our service
* Players can only play games that they’ve purchased
* Players can search for games by their name
* The games will also be categorized

Basic developer functionalities

* Add a game (URL) and setting its price. Allow its removal and modification.
* Basic game inventory and sales statistics (with graphs etc)
* Security restrictions. Developers are only allowed to (add/remove/modify) their own games. Devs can only add games to their own inventory etc.

Game/service interaction

* The game uses predefined postMessages to communicate with our store. This works both ways.
* Scores are recorded to the players own scores as well as to global high score lists.

Quality of Work

* Quality of code
  * The structure of the application will be carefully planned and we will follow this plan. All functions will be commented and in the      backend we will make UnitTests for these functions.
  * We will pair review our code.
* Purposeful use of Django
  * We will follow the general guidelines when it comes to using Django (MVT-separation, Don’t repeat yourself etc.)
* The application will be developed for users. Therefore the user experience is a high priority and will get a lot of focus. Main goals           for achieving this:
  * Ease of use
  * User interface is intuitive and pleasant to look at
  * We will also use and test the app ourselves a lot to reduce bugs and ensure that it is genuinely functional

### Additional features: ###

1. Players are able to save and load games with the simple message protocol described in Game Developer Information
2. Players and developers are able to login also with Facebook
3. Social media sharing (in Facebook) with advertising in mind
4. Mobile friendly
  * The app should be responsive also on mobile phones
  *  Works on different screen sizes and on touch based devices

### Model Structure ###

![Model Structure](https://git.niksula.hut.fi/vilkkie1/wsd-2015-project/blob/master/wsd-models.png)

If image is not showing look at wsd-models.png in the root of repo.

## Testing: ##

For the backend django code, we will write unittests. We will try to cover all functionalities but we do not believe a static code covered percentage is a good way to validate that all code has been properly tested. Our focus regarding testing is more on the quality of tests rather than on code coverage itself.

We will also peer review all code. This has two functions. The first is that it most likely results in better overall code, but also it ensures that everyone is aware of what is happening in our project, especially because of our small group size.

The GUI will be extensively user tested. Our own game will be tested with unit tests.

# Sharing Work #

### Lauri Telama ###

I did a large part of the authentication and registration forms. I also did the authentication email system and the messaging system between the game and the server. I also did a few templates and changed bootsrap abit.

### Eetu Vilkki ###

Eetu did the facebook login and sharing, password change, adding games and changing them, logging in and part of the registration forms. Categorizing games and the search function. Creating the iframe for games as well as Heroku deployment. He also did many of the templates. Also implemented bootstrap and a majority of the tests.

### Joona Haavisto ###

Implemented the payment service as well as transaction history. He also did quite abit of bug fixing and an original mockup for our homepage / other pages.

# Instructions how to use your application #

The application is also hosted here:

http://morning-hollows-34668.herokuapp.com/

Note that if you want to run the server locally you need to use the command "python manage.py runserver --insecure" to serve the static files, because debug is set to false in the settings.

There shouldn't be a database in git so you need to create one yourself (with "python manage.py migrate") and then register as a developer and add the test game (URL: http://payments.webcourse.niksula.hut.fi/ ).

Using it is quite simple. You can sign in with Facebook or register as a player. If you register as a player you need to activate your email. Then you can login and purchase games. 

NOTE: I deleted the settings.py file because it contained sensitive information about the facebook app and heroku settings so no one can tamper with them. Running the program locally isn't possible, but you can check the code here. Also you can go to the heroku app if you want to try the website out.

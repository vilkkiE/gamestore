Online JavaScript Game Store Plan
=================================

## Team: ##

* 475758 Lauri Telama
* 478917 Joona Haavisto
* 428077 Eetu Vilkki

## Goal: ##

Our goal is to create a working, intuitive and seamless online javascript game store. The service will allow two types of users: players and developers. Players can buy games on our service and play bought games. Developers can add their games to the service and set a price for their game. The games are added to the store by giving an url to an html file that contains the game.

Three essential goals we strive to complete are strong security, high quality and excellent reusability.


## Plans: ##

The project will be done by using JavaScript, JQuery, HTML and CSS with Bootstrap library. In the backend we will use Django.

### Planned features: ###

We are planning to fulfill all the mandatory requirements. We will initially focus on doing the following features well before moving onto the extra features.

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
* Security restrictions. Developers are only allowed to (add/remove/modify) their own games. Devs can only add games to their own                    inventory etc.

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

### Planned additional features: ###

We are only doing these once we are confident in the quality and security of the mandatory features. These are prioritized in the following order.

1. Players are able to save and load games with the simple message protocol described in Game Developer Information
2. Players and developers are able to login also with Facebook
3. Social media sharing (in Facebook) with advertising in mind
4. Developing our own simple JavaScript game
5. Mobile friendly
  * The app should be responsive also on mobile phones
  *  Works on different screen sizes and on touch based devices

We are not planning to implement extra features that are not listed in the project description.

### Necessary views: ###

* Home page: domain
* List of all games: /games
* List of owned games for players: /users/{id}/games
* Page where a game can be played: /games/{id}
* List of developed games for developers: /devs/{id}/games
* Statistics for each developed game: /devs/{id}/games/{id}
* Account info page for users: /users/{id}
* Account info page for devs: /devs/{id}
* Registration page for users: /register
* Login page for users: /login
* Page for adding games to our service: /devs/{id}/add-game

### Model Structure ###

![Model Structure](https://git.niksula.hut.fi/vilkkie1/wsd-2015-project/blob/master/wsd-models.png)

If image is not showing look at wsd-models.png in the root of repo.

## Process and Time Schedule: ##

Below is a planned timetable for this project. For each feature, we have also assigned a risk value. The risk values used are L for low, M for medium and H for high.

Implementation order and risk analysis:

Start date: 04.01.16

1. Creating an initial GUI  > L
2. User registration, login and logout > L
3. Developers can add games to their inventory > M

End of week 1

4. Players can buy (payment not yet implemented) and play games > M
5. Developers can remove and modify their games and set prices for them > L

End of week 2

6. Developers can see statistics of game sales > M
7. Players can see high scores and record their score > M
8. Mockup payment service > H

End of week 3

9. Categorizing of games > M
10. Ability to search for games by their name > M
11. Polishing and styling of GUI >  H

End of week 4

12. Security restrictions for players > H
13. Security restrictions for developers > H
14. Ability to save and load games > M

End of week 5

15. 3rd party login > M
16. Social media sharing > M
17. Own game > M

End of week 6

18. Mobile functionalities > H
19. Finalisation > L

Deadline: 20.02.16

### How we plan to work: ###

For task management we are using Trello. Starting next year we will meet weekly. During the meetings we will decide the tasks that we will do and assign the tasks to each person. Additionally, we will attempt to have a coding session with all of us physically present. We are also using Telegram as a communication tool and will do some individual work outside the meetings.

We will use gitLab as version control.

## Testing: ##

For the backend django code, we will write unittests. We will try to cover all functionalities but we do not believe a static code covered percentage is a good way to validate that all code has been properly tested. Our focus regarding testing is more on the quality of tests rather than on code coverage itself.

We will also peer review all code. This has two functions. The first is that it most likely results in better overall code, but also it ensures that everyone is aware of what is happening in our project, especially because of our small group size.

The GUI will be extensively user tested. Our own game will be tested with unit tests.

# Point Self-Evaluation #

We mostly completed everything we planned to do. The following is a list of the tasks and the points we feel like we deserve.

Authentication (200/200). We have a proper authentication system using django auth. We also have a working email validation system using Gmail. There is a seperate registeration for Developers and Players.

Basic player functionalities (300/300). Players are able to buy games with the mockup payment system. They are able to play them and interact with the game. There are 2 highscore lists, one global and one the Users own. A user can not have duplicate scores of the same amount of points. This has been implemented on purpose. We also categorize the games and have a responsive search possibility.

Basic developer functionalities (200/200). Developers can add games to the store. There can not be two games with the same url. A Developer can activate /deactivate a game where is dissapears from the store but owners of the game can still play it. Sale amounts are shown to the developer as well as latest transactions.

Game/service interaction(200/200). The highscore list implementation is in the game and the lists update in realtime without having to refresh the page.

Quality of Work (80/100). In general we are confident about the quality of work. There is some repetition and maybe some bubble gum fixes but in general the code is good. We have never done web software development before, so there can be some un-optimal ways of doing stuff, as we are constantly learning.

Non-functional requirements (180/200). We think our original project plan was fairly good and we followed it well. We were constantly looking at our planned timetable and tried to follow it which worked suprisingly well. We have a constant strem of git commits from all members of the group and teamwork went well. We had alot of coding and planning sessions together and had active Telegram communications. We also used trello to record what we were doing. The link to Trello: https://trello.com/b/9uRoYrFs/wsd

## More Features ##

Save/load and resolution feature (100/100). We have a working save/load system so that users can save their games. Also the game can send out a setting message which sets the resolution to a desired value.

3rd party login(100/100) We have a working and well implemented Facebook login system.

Mobile Friendly (50/50) Our website is easy to use on as mobile device and looks great.

Social media sharing (50/50) We are able to share our games on facebook.

In addition we have added a feature where you are able to change your password for your users!

# Sharing Work #

### Lauri Telama ###

I did a large part of the authentication and registration forms. I also did the authentication email system and the messaging system between the game and the server. I also did a few templates and changed bootsrap abit.

### Eetu Vilkki ###

Eetu did the facebook login and sharing, password change, adding games and changing them, logging in and part of the registration forms. Categorizing games and the search function. Creating the iframe for games as well as Heroku deployment. He also did alot of the templates. Also implemented bootstrap and a majority of the tests.

### Joona Haavisto ###

Implemented the payment service as well as transaction history. He also did quite abit of bug fixing and an original mockup for our homepage / other pages.

# Instructions how to use your application #

The application is also hosted here:

http://morning-hollows-34668.herokuapp.com/

Note that if you want to run the server locally you need to use the command "python manage.py runserver --insecure" to serve the static files, because debug is set to false in the settings.

There shouldn't be a database in git so you need to create one yourself (with "python manage.py migrate") and then register as a developer and add the test game (URL: http://payments.webcourse.niksula.hut.fi/ ).

Using it is quite simple. You can sign in with Facebook or register as a player. If you register as a player you need to activate your email. Then you can login and purchase games. 

NOTE: I deleted the settings.py file because it contained sensitive information about the facebook app and heroku settings so no one can tamper with them. Running the program locally isn't possible, but you can check the code here. Also you can go to the heroku app if you want to try the website out.

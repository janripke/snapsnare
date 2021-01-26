* generate a uuid

postgres# create extension "uuid-ossp"

after installing the function uuid_generate_v4() is available for the super-user
postgres, but not for the user snapsnare_owner.

reference:
https://stackoverflow.com/questions/43685799/postgres-uuid-type-error

* add the field chord_progression/chord_schema (akkoorden schema) to the upload, not required.
* add replies to activities  
* convert audio to musical notes
* converted audio (to wav) does not play in firefox (linux) 

* activities
  * format the active timestamp to 12 December om 12:12

* browser language
  * retrieve the browser language
  * build language logic 

* language support
  * build in language support
  
* resolve beats per minute in audio files.
* remove uuid (postgresql) from insert scripts, should be protected, so we can commit to git
* remove the passwords from the test.
* remove the postgresql credentials from the db configuration, should be in .noora
* create smtp support
  https://www.digitalocean.com/community/tutorials/how-to-use-google-s-smtp-server
* create more log entries
* create activity entries from a user perspective. 
* create password_forgotten
* posting support multiple images
* posting check for uuid manipulation
* sections, make them dynamic, reflecting the highest level
* build-in, calendar functionality
  https://www.creative-tim.com/product/full-calendar
* synchronize postings with facebook using the facebook graph api.
* section, in_navbar (0/1), shows the section in the navbar.
* posting add suppress header option. Make it configurable as part of the section, that you can
  in the posting this option then becomes available.
* jamulus setup a headless server
  can be realised through a container too.
  https://jamulus.io/wiki/Choosing-a-Server-Type
  https://jamulus.io/wiki/Running-a-Private-Server
  https://jamulus.io/wiki/Server-Linux#running-a-headless-server   
* allow iframes for youtube
  
  the expected flow is : create a reset request, send an email containing an url and an activation key.
  when the key is valid the user allowed to change the password.


finished
* add the field chord_progression/chord_schema (akkoorden schema) to the upload, not required.
* footer aligned in the middle, use 3 sections as in the body.
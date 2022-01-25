# Version 0.0.14
- uses snapsnare-db 1.0.10
- translated navigation from Dutch to English. English is now the default language.
- added db log handler, log statements are now logged in the database.

# Version 0.0.13
- removed dependencies to 'aubio', 'google-api-python-client', 'oauth2client'
- added section Development and the role developer
- changed snapsnare logo, added ALPHA to it.
- added reply repository, and corresponding replies table.
- uses snapsnare-db version 1.0.9

# Version 0.0.12
- footer, link to snapsnare group on facebook
- typo: Registeren should be Registreren (in Dutch)

# Version 0.0.11
- replaced section_components with fragments
- send an activation e-mail for new users.
- users can activate their new account.
- added section allowed_roles for adding new content.  
- bug: new users can not login

# Version 0.0.10
- set limit to 1, when showing the current online jamulus jammers.

# Version 0.0.9
- Sections, To speed-up rendering the data is only loaded when component to retrieve the data for contains the
  specified section_component.
- Added sharing icon to my_samples and snaps
- Added chord_schema to my_samples and snaps, it was there, but now it is shown (again)
- Upload, set sharing default to public
- Sidebars, in settings and sections, added paragraph break.
- Added bookmark support to activities, snaps, my_snaps, settings.sections, settings.instruments and settings.genres
- Added file repository.

# Version 0.0.8
released 2021-05-12
- When an unknown sections is used, the Home section is assumed, as a result the Team section is shown in the sidebar
  Rendering of the sitebar is now connected to the section you are in. As the home section has no sidebar it will not
  be rendered.
- My samples, added My samples, shows the uploaded samples of a specific user.
- Upload, added genre, instrument and access_modifier dropdowns to the sample upload form.
  The access_modifier dropdown determines whether the sample is private and only shown in My samples, or public and shown 
  in My samples and the Sound bank.
- Added genres to settings, admins can add genres
- Added instruments to settings, admins can add instruments.

# Version 0.0.7
unreleased
Changelog
=========
Release |version|
-------------------------
Dependencies
    - - / -
Incompatible changes
    - - / -
Deprecated
    none
Features added
    - package and dependency management with Poetry
Bugs fixed
    - some
Testing
    - - / -
    
Release 22.10.29.17-email
-------------------------
Dependencies
    - - / -
Incompatible changes
    - new result layout
Deprecated
    none
Features added
    - new option 'email'
    - setup 
    - more JavaScript support
Bugs fixed
    - some
Testing
    - new test without gldnddlSearchString and option=email
    
Release 22.10.29-regex
----------------------
Dependencies
    - - / -
Incompatible changes
    none
Deprecated
    none
Features added
    - regex instead of re to fix look-behind problem
Bugs fixed
    - some
Testing
    - compare findings instead of findingElementsQuery with the option=regex-test

Release 22.10.23-regex-results
------------------------------
Dependencies
    - - / -
Incompatible changes
    none
Deprecated
    none
Features added
    - regex capturing group search
        - with 
        
        ```bash
        scrapy crawl recherchedechaîne_gldnddl -O ../../reports/findings.json -a gldnddlSearchString='(?<=mailto:)(.+?)(?=\?|"+)' -a option=regex -a start_urls=https://planet.gnome.org/
        ```
        Goldendoodle shall extract all E-mail adresses following this regex 
    - new argument option
Bugs fixed
    - some
Testing
    - tested with gldnddlSearchString='(?<=mailto:)(.+?)(?=\?|"+)' and option=regex

Release 22.08.26
----------------
Dependencies
    - - / -
Incompatible changes
    none
Deprecated
    none
Features added
    - dynamic websites
    - execute JavaScript with `Scrapy with Selenium <https://github.com/mrafee113/selenium_scrapy>`_
Bugs fixed
    - some
Testing
    - test folder added

Release 22.08.17
----------------
Dependencies
    - / -
Incompatible changes
    none
Deprecated
    none
Features added
    - version on index.html
    - README.md as project file
    - go public
Bugs fixed
    - / -
Testing
    - / -

Release 22.08.13
----------------
Dependencies
    - json
Incompatible changes
    none
Deprecated
    none
Features added
    - documentation within GitLab
Bugs fixed
    - parse start URL 
Testing
    - parse example.com

Release 22.08
-------------
Dependencies
    none
Incompatible changes
    none
Deprecated
    none
Features added
    - test and documentation build generalized
        -   The script ends when an error occurs with an incomplete command.
Bugs fixed
    none
Testing
    none

Release 22.07
-------------
Dependencies
    none
Incompatible changes
    none
Deprecated
    none
Features added
    - documentation with Sphinx, MyST, doctest
Bugs fixed
    none
Testing
    none


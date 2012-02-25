What is JqResources?
====================


JqResources is an Django application, which helps managing JavaScript and CSS resources, like jQuery and jQuery UI themes.

JqResources is meant to provide reusable static resources for applications within whole site.

It has an `admin interface`_ allowing to add resources, which can then be used by other applications.


Genesis and ideas
==================

It is a very common situation, when more than one application requires certain JavaScript library (eg. jQuery). Each of them could come with its own copy of the resource in *static* directory or require user (pron. developer) to obtain it themselves and provide applications with path or update their templates and/or settings. It’s getting event more complicated if it comes to updating version of the resource or its theme (eg. for jQuery UI).

It’s best explained with an example. Say you have two different applications which provide rich admin interface. It’s very likely that they would be using jQuery, jQuery UI or other similar libraries. As it was stated before, they both may come with their own version of needed resources or require user to provide it.
The first options is quite comfortable, as the resources would be installed with *collectstatic* command. But there some problems may arise. First of all, the user (developer) might not want to keep several copies of the same library as it’s hard to maintain them. The second problem may be the legal one: it is possible that the licence of used library won’t allow the author of the application to redistribute it.

Here comes JqResources to the rescue. It allows the authors of third party Django application to mark their products as dependant on certain resources. Back to example above, the first application may require jQuery and the second one jQuery and jQuery UI. And the application do not need to be distributed with those libraries. It will be up to the user to provide required resources in desired versions.


Usage
=====

Defining dependencies
---------------------

There are several ways of using JqResources. The first is by defining *ModelAdmin*. It is done in standard Django’s way – by using Media class.

Declaration (admin.py)::

    class CustomAppBaseAdmin(admin.ModelAdmin):
    
    class Media(JqResourceMedia):
        css = {
            "all": (
                jq("jquitheme"),
                "customapp/css/admin.css"
            )
        }
        js = [
            jq("jquery"),
            jq("jqueryui", "1.8.17"),
            jq("itemspicker"),
            "customapp/js/admin.js"
        ]

As one can see, there are several occurrences of *jq* objects. User is only required to provide the name of the resource and desired version (if version isn’t provided, the default version will be implied). JqResources will “translate” the occurrences of jq objects to the paths of said resources.

Another use case is in templates::

    {% resource "jquery" %}

Analogously, the above statement will be translated to full HTML tag with a proper path, depending on type of the resource (JavaScript, CSS, etc.)

Translating JqResources
-----------------------

Here is how JqResource knows the paths of the resources. The user needs to provide all the resources, name them and indicate their versions. It is done with an convenient `admin interface`_. Unlimited number of resources may be added and each of them may have unlimited number of versions. Each resource may have a default version, which will be used if none is explicitly desired.

.. _admin interface:

What it looks like?
===================


Everybody loves screenshots, right?

JqResource changelist:

.. image:: http://img21.imageshack.us/img21/5007/selectjqresourcetochang.png
  :alt: Select JqResource to change

JqResource:

.. image:: http://img52.imageshack.us/img52/562/changejqresource.png
  :alt: Change JqResource

JqResource Version:
  
.. image:: http://img821.imageshack.us/img821/1622/selectjqresourceversion.png
  :alt: Select JqResource Version to change


Installation
============

JqResources is installed just like any other Django application:

1. Put JqResources in any path, where python can find it
2. Run ```manage.py syncdb``` to create database tables for JqResources
3. Run ```manager.py collectstatic``` to copy (or link) static files used by JqResources itself
4. Register ModelAdmin classes found in ``jqresources/admin.py`` file in you admin site


Performance and security concerns
=================================

Users of JqResources must be warned, that incautious usage of the application may cause serious performance penalties and potential security risks.

Performance
-----------

As for now, there is one database hit generated for each ``jq`` object or ``resource`` template tag occurrence. Generally, it is not a problem for code in *ModelAdmin*’s *Media* because it is run only once – during cold start. There should be more attention paid to ``resource`` template tag usage, because if it’s not cached, one may end up with many unnecessary database hits.

Security
--------

Because resources’ paths are provided via admin forms, there is a potential risk that sensitive files will be exposed. Administrators must always double check their spelling and never give access inexperienced or untrusted users.

Moreover, there should be special attention paid to the configuration of the HTTP server to not allow paths to point beyond the root of the site’s static directory.


License
=======

Copyright 2012 Aleksander Zdyb

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see http://www.gnu.org/licenses/.

# README #

Try this entirely from VIM!

Blah


This is an example of what it takes to make the most out of the HANA2 Web-IDE when developing Multi-Target Applications (MTAs) that include one or more modules that are currently not supported by the HANA2 Web-IDE.

In this case the non-supported module type is a Python module.

NOTE:  This is not an ideal solution!  Once XS-Advanced supports a module type of python and the HANA2 Web-IDE is updated to support it, the methods described here should be considered obsolete.  However, you could draw inspiration from the following to support additional programming languages (like Swift!, anyone..., anyone...?)

### How do I get set up? ###

* Get access to a HANA2 system that has XS-Advanced installed with it. (HANA1 SP12 was NOT tested for this! YMMV)

* Make sure your XSA users are set up properly with the proper role collections etc.  I can't do this for you.  You have to figure it out by reading the appropriate documentation.

* Prerequisite Tools.  I like to work by SSH-ing into the server an running the xs command line tool on the server were the app will be deployed.  You can do this or work from your local workstation where you've installed the xs command line tool as well.  Either place you'll also need a functional git client in order to coordinate your source code and edit things apart from the Web-IDE.

```
git clone <this project's git url obtained above>
```

* Prerequisite Services.  Perform the following in your deploy space.

```
xs create-service xsuaa devuser my-uaa
```
 
good to go!

### The Recipe ###

1.. Find the Web-IDE url on your system and open the URL in Chrome browser.

```
xs target -s SAP
xs app webide --urls
```

2.. Right-click on the Workspace and select Git > Clone Repository. Enter the Git repo URL for this project.  Hit the tab key to fill in the rest of the fields.  Click the OK button at the bottom if the dialog box.

![webide_custom_3.png](https://bitbucket.org/repo/kpBjjq/images/3568154026-webide_custom_3.png)

We're going to use this cloned project as a reference and build another one manually to show the steps and the justification behind them.


3.. Create a new MTA project.

![webide_custom_r2d2_2.png](https://bitbucket.org/repo/kpBjjq/images/2478578727-webide_custom_r2d2_2.png)

Select Multi-Target Application Project and the Next button.

Name the project "mta_php2". Click Next.

Select the Space that you want to deploy into.  Click Finish.

![webide_custom_7.png](https://bitbucket.org/repo/kpBjjq/images/2072614440-webide_custom_7.png)

The new mta_php2 project isn't under Git revision control because we manually created it.  This poses a problem for us because we need to perform some operations from the command line on the server in order to do build and deploy tasks for our unsupported PHP module.  So we need to take the empty project and put it into Git as well.


4.. Putting the empty project in a Git repo.

I won't be able to give you explicit details on how to do this from the Git server side of things, but you'll need to have access to a Git server that's available on the public Internet and for which you have an account that enables you to create new Git repositories.  I'd suggest you use [GitHub](https://github.com/) or [BitBucket](http://bitbucket.org/).  You've probably noticed I'm using BitBucket.  I've gone ahead and created a new empty repository called mta_php2 in my account for this purpose.  I'm not going to show you the details because they vary depending on the service you use.

Now we're going to export the existing empty project to the local file system and then commit it's contents into our newly created repo.

Right-click on the mta_php2 project and Export the project.

![webide_custom_r2d2_4.png](https://bitbucket.org/repo/kpBjjq/images/1322524403-webide_custom_r2d2_4.png)

This will create a zip file in your browser's default download area.  Now expand the zip file and open up a terminal window and navigate to where that folder resides.  If you list this folder you'll only see a mta.yaml file.  List it again showing hidden files and you'll see a folder named .che.  This is where the Web-IDE project specific files are stored and it's important to make sure that it's commited to the Git repo as well.

![webide_custom_r2d2_6.png](https://bitbucket.org/repo/kpBjjq/images/4089682053-webide_custom_r2d2_6.png)

Initialize this folder as a Git repo.  Note:  You'll need a functional git program on your local machine to do this.  If you find that your system doesn't have one, you'll need to find one for your OS and get it.

```
git init
```

Now set up this local Git repo to connect to the server Git repo that you set up before.  These are my exact Git commands to do so, but yours will vary based on your Git server's specifics.

```
git remote add origin https://bitbucket.org/byol/mta_php2.git
git add --all .
git commit -m "Initial Commit"
git push -u origin master
```

At this point the empty project files are uploaded on the Git server.  You may want to check that they are there using whatever web-browsing function is available on your Git server.  For us, we'll assume it went well.

Now we need to go back to the Web-IDE and delete the manually created local mta_php2 and perform a Git Import of our project as we did above to import this Git project.

![webide_custom_r2d2_8.png](https://bitbucket.org/repo/kpBjjq/images/2810624887-webide_custom_r2d2_8.png)

![webide_custom_r2d2_10.png](https://bitbucket.org/repo/kpBjjq/images/1743252144-webide_custom_r2d2_10.png)

![webide_custom_r2d2_12.png](https://bitbucket.org/repo/kpBjjq/images/739220716-webide_custom_r2d2_12.png)

![webide_custom_r2d2_14.png](https://bitbucket.org/repo/kpBjjq/images/2205134248-webide_custom_r2d2_14.png)

OK, now we are effectively back to where we started only now we have a new project that's under Git revision control and this will be important to our situation.

![webide_custom_r2d2_16.png](https://bitbucket.org/repo/kpBjjq/images/2983390737-webide_custom_r2d2_16.png)


5.. Add a **Basic HTML5 Module** to the project and name it **web**.  This will act as our app router for HTTP requests.

![webide_custom_r2d2_18.png](https://bitbucket.org/repo/kpBjjq/images/1654434133-webide_custom_r2d2_18.png)


6.. Add an **HDB Module** to the project and name it **db**.  This is where the database artifact definition files will reside.

![webide_custom_r2d2_20.png](https://bitbucket.org/repo/kpBjjq/images/2754017281-webide_custom_r2d2_20.png) 

Accept the default Namespace as **mta_php2.db** and also, you can leave the Schema Name blank and check the "Build module after creation" checkbox.


7.. Now we're going to use the originally imported project to save some time and copy some data definition files.  Expand the original mta_php project and then the db folder and finally the src folder.  Left-click the first file and then Shift Left-click the last file and then Right-click on the select files and pick **Copy** from the context menu.

![webide_custom_r2d2_23.png](https://bitbucket.org/repo/kpBjjq/images/1300247914-webide_custom_r2d2_23.png)

Collapse the mta_php project and expand the mta_php2 project.  Expand the db folder and select the src folder.  Right-click on the selected folder and pick Paste from the context menu.

![webide_custom_r2d2_25.png](https://bitbucket.org/repo/kpBjjq/images/1693837236-webide_custom_r2d2_25.png)

Before doing anything else, go into each folder and edit any occurrence of mta_php with mta_php2.  Open With each file and select the Text or Code editors by Right-clicking on the file name.

When you are finished, Right-click on the Highlited db module and select Build.

![webide_custom_r2d2_27.png](https://bitbucket.org/repo/kpBjjq/images/3146289377-webide_custom_r2d2_27.png)

You'll likely get the following Build Failed context message.  This just means that the editor doesn't know which space to perform the build into.

![webide_custom_r2d2_29.png](https://bitbucket.org/repo/kpBjjq/images/1309986521-webide_custom_r2d2_29.png)

Right-click on the mta_php2 project and select "Project Settings".

![webide_custom_r2d2_31.png](https://bitbucket.org/repo/kpBjjq/images/3401790163-webide_custom_r2d2_31.png)

Then click Space.

![webide_custom_r2d2_33.png](https://bitbucket.org/repo/kpBjjq/images/1054630191-webide_custom_r2d2_33.png)

And select the space you want.  Click on the Save button.  Then Cancel.

![webide_custom_r2d2_35.png](https://bitbucket.org/repo/kpBjjq/images/3560394137-webide_custom_r2d2_35.png)

Now when you Build the db module you should get a completed successfully message.

![webide_custom_r2d2_37.png](https://bitbucket.org/repo/kpBjjq/images/2282159251-webide_custom_r2d2_37.png)


8.. Create a NodeJS module.

Normally we wouldn't need to do this if the Web-IDE could handle a module of type custom.  However, currently this isn't the case and we need a module that can stand in for our PHP module when it comes to providing a target route that the app-router module can understand.  So the NodeJS module acts as a sort of surrogate for the PHP module.


9.. Create a folder for the PHP module.

Again, normally we'd happily just right-click and pick New -> PHP Module, but the Web-IDE doesn't yet support this or event a Custom Module.  We'll place our index.php file here which the buildpack looks for in order to tell what kind of module this is when it's finally deployed.  It also it the main php file that's executed.  There is also a file called run_as_php which is a Bash script.  This script performs the steps that a Deploy or Run-As option would take if the Web-IDE would support this.  We'll run this script a the command prompt of the server, but we can at least edit it here if we want or just refer to it.


10.. Edit the Provides/Requires section of the mta.yaml file.

11.. Edit the app-router's xs-app.json file to add routes for each extension type.

12.. Build and run the js module.

13.. Build and run the web module.

14.. Sync the project on the server with Git.

15.. Execute the run_as_php script.

16.. Test each node directly.

17.. Test each note through the app-router.


99.. Need to rework this entirely...
 

### Contribution guidelines ###

* Anyone..., anyone...
* If this topic is of interest to you, please contact andrew.lunde@sap.com

### Who do I talk to? ###

* Again, this is an un-official work-around and no support is offered.
* However, if you must then andrew.lunde@sap.com

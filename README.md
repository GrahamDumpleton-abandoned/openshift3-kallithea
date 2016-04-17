# Kallithea for OpenShift 3

[Kallithea SCM](https://kallithea-scm.org) is an Open Source, source code management system that supports the two leading version control systems, Mercurial and Git, and has a web interface that is easy to use for users and admins.

This project repository contains all the files you need to deploy a Kallithea instance to OpenShift 3. This includes deployment of a database and the initialisation of that database for the Kallithea application.

An extension module is also installed for Kallithea which implements a web hook mechanism that can be linked up to OpenShift in order to automatically trigger a new build and deployment of your application within OpenShift whenever you push up changes to a Git repository managed by Kallithea.

![image](./docs/kallithea-overview.jpg "Kallithea Overview")

The reasons for developing this project are as follows:

1. To provide an easy way of deploying Kallithea to an OpenShift cluster, enabling you to manage the source code repositories, rather than needing to use a source code hosting service such as GitHub, BitBucket or GitLab. 
2. As a case study for how the building and deployment of a Python web application can be managed using [warpdrive](http://www.getwarped.org).
3. As a case study for how a complex web application, requiring persistent storage, a database, and other services, can be deployed to OpenShift.

Because the project is in large part being used as a test bed to illustrate how to use warpdrive and OpenShift, in depth documentation is provided here on not only how to deploy Kallithea to OpenShift, but also how the scripts and templates provided are implemented and work.

Although the primary target for deploying Kallithea is OpenShift, it is possible to also deploy to Docker. No pre built image is provided for this scenario, but instructions are provided for how you can create the required Docker image from this project repository using the [Source to Image](https://github.com/openshift/source-to-image) (S2I) tool.

## Deployment Options

Two different ways of deploying Kallithea are currently provided. These are:

**Default** - This option deploys a single instance of Kallithea along with an instance of the PostgreSQL database. The PostgreSQL database and the Git/Mercurial repositories are stored on a shared persistent volume. OpenShift life cycle hooks are used to automatically initialise the database on the first deployment, as well as manage database migrations on subsequent deployments when required. The Kallithea web application can be scaled up if necessary.

**Lite** - This option deploys a single instance of Kallithea, but rather than using PostgreSQL, uses a file based SQLite database stored within the persistent volume used to store the Git/Mercurial repositories. Initialisation of the database and subsequent database migrations are handled through action hooks executed within the Kallithea instance when it is being started. Although Kallithea can with this option still be scaled up, it is recommended the *Default* option be used if scaling is required, as PostgreSQL is likely to provide a more robust system than using SQLite.

There is an intention to eventually provide a third deployment option called *Ultimate*. This will deploy two separate instances of Kallithea. The first instance will be used to serve up the web interface. The second will be used to handle all Git/Mercurial client interactions. This will allow the separate instances to be scaled up independently based on usage, and web server configurations to be tuned for the different use cases. The *Ultimate* option will also deploy Celery worker instances to handle long running tasks such as cloning of repositories on initial project creation. Rather than sharing a persistent volume between the PostgreSQL database and storage for Git/Mercurial repositories, the *Ultimate* option will use separate persistent volumes for each.

## Installation Steps

In a hurry? Want to get Kallithea running and don't care about the details? If you are, you can run the following steps using the OpenShift ``oc`` command line tool.

**Create a new project within your OpenShift cluster.**

```
$ oc new-project scm
Now using project "scm" on server "https://10.2.2.2:8443".

You can add applications to this project with the 'new-app' command. For example, try:

    $ oc new-app centos/ruby-22-centos7~https://github.com/openshift/ruby-hello-world.git

to build a new hello-world application in Ruby.
```

**Load the application template for Kallithea.**

```
$ oc create -f https://raw.githubusercontent.com/GrahamDumpleton/openshift3-kallithea/master/template.json
template "kallithea-scm" created
template "kallithea-scm-lite" created
```

**Create the Kallithea application.**

```
$ oc new-app kallithea-scm
--> Deploying template kallithea-scm for "kallithea-scm"
     With parameters:
      Application instance name=kallithea
      Application admin user=admin # generated
      Application admin user password=EukS3fKWcXJWxRw1 # generated
      Application admin email=admin@example.com # generated
      Application memory limit=192Mi
      Application volume capacity=512Mi
      PostgreSQL database user=user0XV # generated
      PostgreSQL user password=Vjxhbn5nPmwXcBGP # generated
      PostgreSQL memory limit=192Mi
--> Creating resources with label app=kallithea ...
    imagestream "kallithea" created
    buildconfig "kallithea" created
    deploymentconfig "kallithea" created
    persistentvolumeclaim "kallithea-pvc" created
    service "kallithea" created
    route "kallithea" created
    deploymentconfig "kallithea-db" created
    service "kallithea-db" created
--> Success
    Build scheduled, use 'oc logs -f bc/kallithea' to track its progress.
    Run 'oc status' to view your app.
```

**Determine the exposed hostname for Kallithea.**

```
$ oc describe route kallithea
Name:			kallithea
Created:		60 seconds ago
Labels:			app=kallithea,template=kallithea-scm-template,web=kallithea
Annotations:		openshift.io/generated-by=OpenShiftNewApp
			openshift.io/host.generated=true
Requested Host:		kallithea-scm.apps.10.2.2.2.xip.io
			  exposed on router router 60 seconds ago
Path:			<none>
TLS Termination:	edge
Insecure Policy:	Allow
Service:		kallithea
Endpoint Port:		8080-tcp
Endpoints:		<none>
```

**Monitor the build and deployment process.**

```
$ oc status
In project scm on server https://10.2.2.2:8443

https://kallithea-scm.apps.10.2.2.2.xip.io (and http) to pod port 8080-tcp (svc/kallithea)
  dc/kallithea deploys istag/kallithea:latest <-
    bc/kallithea builds https://github.com/GrahamDumpleton/openshift3-kallithea.git#master with openshift/python:2.7
    deployment #1 deployed 30 seconds ago - 1 pod

svc/kallithea-db - 172.30.137.191:5432
  dc/kallithea-db deploys openshift/postgresql:9.4
    deployment #1 deployed 2 minutes ago - 1 pod

1 warning identified, use 'oc status -v' to see details.
```

**Access the Kallithea instance (when the build and deployment has completed).**

```
open https://kallithea-scm.apps.10.2.2.2.xip.io
```

**Login using the 'admin' user account (use the generated password output by 'oc new-app').**

```
Application admin user=admin # generated
Application admin user password=EukS3fKWcXJWxRw1 # generated
```

## All the Gory Details

Coming soon.


 






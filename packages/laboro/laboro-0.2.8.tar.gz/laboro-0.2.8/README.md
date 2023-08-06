---
gitea: none
include_toc: true
---
![Build Status](https://drone.mcos.nc/api/badges/laboro/laboro/status.svg) ![License](https://img.shields.io/static/v1?label=license&color=orange&message=MIT) ![Language](https://img.shields.io/static/v1?label=language&color=informational&message=Python)

# Laboro

## What is **Laboro** ?

**Laboro** is a **NO-Code / Low-Code** workflow automation tool that helps you to build and run automated tasks with the least amount of effort and technical knowledge:

- You don't need to know how to install a specific development environment to use **Laboro**.
- You don't need to have advanced system administration knowledge to run your **Laboro** automated tasks.

## How can **Laboro** help me ?

Busy developers and system administrators have many task automation needs, but often don't have enough time to write and maintain their scripts and, even worse, when there are scripts, they rarely are consistent with each other, which makes their maintenance tedious.

**Laboro** provides a unique way to **quickly** write and execute standardized, easy to maintain automated workflows without any need to install a specific environment or dependencies of any kind.

It also:
- [checks all given parameters consistency and validity](./README/modules.md#class-arguments-and-method-arguments) without having to code any *argparse* or equivalent
- [manages sensible data encryption](./README/secrets.md) such as login and password.
- [keeps trace of all executions of all *workflows*](./README/history.md) with start time, end time, execution time, all given parameters and exit code
- Outputs a per workflow execution [standardized, formatted and timestamped log](/README/logging.md) in both a file and the *standard output*.

Advanced users shall find **Laboro** as a mix between:
- A *CI/CD* tool such as *Gitlab CI*
- A *configuration provisioning* tool such as *Ansible*
- An *Extract Transform Load* tool such as *Talend*.

**Anyway, the main purpose of **Laboro** is to provide a tool to quickly write highly standardized and easy to maintain automation tasks with the least amount of effort and technical knowledge.**

## What does **Laboro** mean

**Laboro** is the latin expression for *"I am working"*.

Your time is valuable and tedious tasks are for robots. **Laboro** is always pleased to perform all your repetitive tasks for you while allowing you to stay focused on the part of your job where you bring real added value.

## Development status

**Laboro** is currently well tested and *"without known bug"* but is still in *beta* stage and will not be considered suitable for production until **Laboro-1.0.0** release.

## Status of this documentation

This documentation is a work in progress and changes may occur until the release of the **Laboro-1.0.0** version.


## Install **Laboro**

**Laboro** leverages modern container environments such as [*Podman*](https://podman.io/) or [*Docker*](https://www.docker.com/).

Follow the [quick installation guide](./README/install.md) for all needed details.


## Configuration

Since **Laboro** is run as a container, it does not require any configuration tweaks.

However, advanced users may have a look on [how to configure **Laboro**](./README/configuration.md) to suit specific needs.


## Concepts

**Laboro** lays on the following fundamental concepts:
- [*sessions*](./README/sessions.md)
- [*history*](./README/history.md)
- [*secrets and data encryption*](./README/secrets.md)
- [*logging*](./README/logging.md)
- [*workspaces*](./README/workspaces.md)
- [*workflows*](./README/workflows.md)
- [*packages and modules*](./README/packages.md)
- [*instances*](./README/instances.md)
- [*steps*](./README/steps.md)
- [*actions*](./README/actions.md)
- [*methods*](./README/methods.md)
- [*variables and iterables*](./README/variables.md)
- [*loops*](./README/loops.md)
- [*conditions*](./README/conditions.md)
- [*files and data files*](./README/files.md)


## Modules

**Laboro** capabilities are extended through *modules* delivered as *Python* packages.

All information about [available modules](./README/modules.md#laboro-modules) and [how to write you own module](./README/modules.md#how-to-write-your-own-module) are available [here](./README/modules.md).


## Configure your first workflow

Configuring a **Laboro** workflow is basically writing a *YAML* file.

You may want to first have a look at the [underlying concepts](#concepts) or if you feel brave enough go straight to step by step guide and [configure you first workflow](./README/first_workflow.md)


## Running your workflows

Once all your *workflows* [are configured](README/first_workflow.md) and saved in the `/path/to/local/workflowdir`, you can run them by issuing the following command:

Example:
```bash
podman run --name laboro \
           -e TZ=Pacific/Noumea \
           -v /path/to/local/workflowdir:/opt/laboro/workflows:Z \
           -v /path/to/local/workspacesdir:/opt/laboro/workspaces:Z \
           -v /path/to/local/logs:/opt/laboro/log:Z \
           mcosystem/laboro:latest \
           -w workflow_demo_1.yml workflow_demo_2.yml workflow_demo_3.yml
```

In this example the 3 workflows `workflow_demo_1.yml`, `workflow_demo_2.yml`, `workflow_demo_3.yml` will be run sequentially in the specified order within a container which time zone will be set to `Pacific/Noumea`.

The container also has three host directories mounted:
- `/path/to/local/workflowdir` mounted on `/opt/laboro/workflows`
- `/path/to/local/workspacesdir` mounted on `/opt/laboro/workspaces`
- `/path/to/local/logs` mounted on `/opt/laboro/log`

You may find more specific examples of [*how to run you workflow*](./README/run.md)


## Show me more !

This repository host all the necessary bits to install, configure and run **Laboro** for demonstration and testing purpose: https://codeberg.org/laboro/laboro_poc

You will find all needed instructions to install a *simulated basic infrastructure* based on 5 containers running the following services:

- A basic http ReST API server
- A FTP server with *TLS support*)
- A mailer host with full support of SMTP/IMAP/POP with *TLS* support
- A *Postgresql* relational database server
- An *openSSH* server with full *SFTP* support

The instructions will guide you through all steps to run a workflow using mostly all **Laboro** features such as [*loops*](./README/loops.md), [*variables and iterables*](/README/variables.md), [*conditional execution*](./README/conditions.md), [*split workflows*](./README/workflows.md#includes) and [*encrypted data*](./README/secrets.md#encrypted-data), [*data files*](/README/files.md#datafiles) etc.

A lot of fun to be discovered for whom would like to understand **Laboro** and wants its daily cumbersome tasks automated once for all 🙂

Example of a **Laboro** container running a real life workflow named `workflow_demo.yml`:
![Laboro demonstration](./media/demo.svg)


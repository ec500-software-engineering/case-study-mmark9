# Case Study - Mastodon

## Project Description

TODO: Add project description

## Installation

TODO: add installation steps here 

From the official page, installation assumes Ubuntu 18.04 but I have Ubuntu version 16.04 on my local machine.

## General Design Philosophy

Mastodon's codebase uses two languages for development: __ruby__ and __javascript__. Developers follow the typical
Model View Controller (MVC) design pattern.

- __Model__: In keeping with the __DRY__ principle each tables defined in the postgres sql database instance have their 
equivalent ruby class file in `app/models` 
- __View__: For templating, HTML abstraction markup language (Haml) is used instead of the standard Embedded Ruby (ERB)
templating. From looking at the process of converting ERB to Haml, it appears that Haml prefers a much less verbose
syntax that you will typically find in many templating frameworks. ERB implements a similar templating strategy that you
will find in many older languages (java, php, etc.). Once looking at Haml, one immediate characteristic is the influence
of CSS like syntax.
- __Controller__: Logic for navigating users across different endpoints are also implemented in Ruby. 

## Programming Language Usage 

### Ruby
Ruby is naturally used in the backend where they implement logic needed to complete tasks such as fetch data from the 
postgres database and render web pages for the frontend. Web pages are created using __Rails__ web application 
framework. Ruby code within the project follow typical Object Oriented (OO) style where all class properties or member
variables are private and can only accessed through getters and setters.

### Javascript

Javascript only counts for a small percentage of the source code base (TODO: add percentage here). Its usage is
strictly for interacting with `React` framework to drive the frontend logic.

## Testing

## Technology Stack
- __Ruby__: language used to implement the majority of backend functionality
- __Rails__: web application framework supporting MVC design pattern
   - Models are implemented as Active Records which are defined in the Object/Relational Mapping (ORM) layer. This 
   allows for a seamless mapping of tables to Ruby objects.
   - Controllers are a type of ApplicationController which handle routing, updating models, managing sessions, etc.
   - Rails supports views by parsing and interpreting Ruby statements embedded in html template files
- __React.js__: front end for managing UI elements
- __PostgresSQL__: relational database acting as the persistent store for the models used in mastodon.
- __Redis__: Redis is an in-memory data store applicable for several use cases. Mastodon primarily uses Redis as a 
cache which is accessed through the Rails controllers. 
- __Node.js__: Used to handle streaming media to clients.
- __yarn__: Alternative javascript package manager. I am not entirely sure why `npm` is not solely used in the project
but from `yarn`'s description, it aims to avoid the headaches of getting packages to install across different machines
and configurations.

Mastodon project utilizes two automated testing methods for coverage of both Ruby and javascript source code:

#### Ruby testing
Ruby testing is automated through
[rspec](rspec.info),  a testing framework applications developed in the Ruby programming language. The philosophy of
this framework is __Test Driver Development__ or (__TDD__). Canonical TDD emphasizes that tests be developed in parallel
with implementations. However, for many developers this is challenge because the additional overhead of maintaining both
application logic and testing logic can be burdensome. With TDD, the idea is to develop tests beforehand and let
__failing__ tests drive implementation. Despite this awkward indirection, following this paradigm can better garuntee
much higher testing code coverage than the conventional ad-hoc write-tests-after-implementation.

A nice feature of rspec is that it also provides a nice interface to view what percentage of your code tests cover.
rspec generates static web page with a single `.html` after running the ruby test suite defined in the `mastodon`
project directory. The figure below shows an example output after running the test suite.

![](assets/img/coverage_ex.png)

From closer inspection, its seems that defined tests have a healthy balance of coverage among the various modules/paths.
The two outliers are `jobs` and `libraries`. Some classes within these paths are deemed obsolete which can be one
explanation for lower code coverage.

#### javascript testing
javascript testing is automated through the use of `yarn` and `npm`. When executing `yarn run test` or `yarn test` in
the root project directory, `yarn` will ask `npm` to run a linter (`eslint`) for convention conformance checking and
more importantly run automated testing using [jest](https://jestjs.io/). Jest is a natural fit for mastadon because
they primarily use __React__ to manage the frontend on the client side. Like `rspec`, code coverage report is generated
if the `--coverage` flag is passed to `jest`. The figure below shows a snippet of testing mastodon javascript codebase
using `jest`.


![](assets/img/js_coverage_ex.png)

Although not as convenient as `rspec`html generated output, it does give a good idea what parts of code are touched the
most by the test cases with a quick glance.

#### Continuous Integration
TODO: add continuous integration section

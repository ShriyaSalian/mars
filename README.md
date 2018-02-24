## mars

## Introduction

mars stands for mostly abstract rest structures. It defines a storage architecture
that can be used to create universal data models.

One primary idea that separates mars from similar approaches to universal data models is that mars emphasizes decentralization, or denormalization, of models and entities. In traditional systems, such as SQL table entity models, topologies can quickly become unwieldy, poorly performant, and poorly understood due to the number of relationships and joins that are imposed. Once a relationship between entities is defined, that relationship must be maintained just as closely as the entities are - because as entity definitions change, they can have unintended side-effect consequences on their relationships as well. Adding more and more relationships, or more and more relationships of relationships, quickly ensures that systems become difficult to use.

mars attempts to mitigate this issue by removing join type relationships entirely. This is done by making it extremely easy and transparent to create, inspect, and modify entity definitions. These entities, and their records (instances), are then exposed directly in a highly stereotyped way to REST endpoints, making them searchable and comparable in a separate part of user code. To handle relationships, mars allows entities to define fields that point to other mars structures - these fields do not rely on computationally intense joins, but instead are stored as part of the entity definition itself. mars prevents recursive or circular reference to entities automatically in order to ensure system cohesion.

Also, mars consists of a very simple and relatively flat topological basis - there are only four orders of layout. The flat structure of mars storage allows a high level of distribution and very fast access to highly stereotyped data. User systems can take advantage of an automatic REST api that provides access to all of their data models and instances.

## Use Cases

mars was created to be able to quickly and easily create persistent data templates for systems that

* do not already have well defined structures of storing data
* would benefit from a ubiquitous system of data that can be passed between functions and objects
* would benefit from having easily accessible structures that can be searched based on groups, class, or attributes
* have large sets of data models
* have quickly changing data models
* have existing data models with many sets of complex relationships that are becoming unwieldy

## Layout

mars consists of several topological layers. Each layer is self contained against other members of its own layer, but holds a one to many relationship against layers below it. These layers, in order of increasing detail, are

* group
    * a mars deployment is a collection of groups
    * a group is the top level organizational unit of mars
    * a group holds collections of related structures
    * for example, a group might represent an 'office'
* structure
    * a structure is the second order collection of mars
    * a structure holds more deeply related models
    * for example, a structure might represent a 'chair', and is contained by the 'office' group
* template
    * a template is the third order collection of mars
    * templates hold closely related models that are similar in nature
    * for example, our 'chair' structure might hold 'executive', 'conference', 'standard' chairs
* field
    * a field is the fourth order mars collection
    * fields have a name, an order (singular or collection), and a datatype
    * field datatypes can be simple (number, string) or reference another complex entity (another template)

Other parts of mars

* record
    * all mars entities are domain model definitions. they should define what a domain consists of
    * domain models can be thought of as a 2d definition of a user space
    * records are the instances of these domain models - the '3d' part of the space
    * many records belong to a given part of a domain model
    * records are searchable through the rest interface based on their definition
    * for example, in our office example, we can ask the system to 'find us all executive or standard chairs that have leather armrests that cost over 100 dollars'
* translation
    * translations declare similar fields between templates - either on the same structure or on different structures
    * translations can be used to migrate records from one entity to another
    * translations can also be used to group certain things and perform faster searches against a broader group of things
* profile
    * profiles define users and permissions - they serve to manage owner and access of things in mars
    * a profile can be finely grained up to structure level. profiles can be assigned access to view/edit/delete groups, structures, templates, fields, etc.

## Status

Currently, mars is complete up to groups and profiles. Translations, records, fields, templates, and structures have all been implemented. The system currently uses mongodb to store data - however, the storage choice is decoupled from the processing layer of mars and could be extended to other storage backends.

The development plan currently is to complete groups and profiles and then add comprehensive unit testing to the package.

## License

MIT Standard

Copyright 2016-2020 Ryan Berkheimer

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

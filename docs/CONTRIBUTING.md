## Contribution guide

**Note:** 

1. Due to current low staffing on the core team, we are a bit slow reviewing and merging submitted pull requests, issues, etc. We do hope to add more contributors to the core team to process them sooner, but for the moment we need to ask for patience. Thanks!
 
2. Before you create an issue, please be sure you searched google, and this repository: there is no such issue you are going to report. If such an issue is found, consider adding a comment to it. If it is a related issue, mention the issue in the issue description please. If you are on an issue page, and you saw a similar issue somewhere in this repository, please tag that issue here.

---

This document provides guidance on Chkware contribution recommended practices. It covers what we're looking for in order to help set some expectations and help you get the most out of participation in this project.

### Areas of contribution

- Updating documentation, and examples
- Finding a bug, and reporting it
- Making a new feature request
- Fixing a bug, or adding a new feature
- Updating specifications

### Updating documentation, and examples

This is the most important kind of contribution someone can make at any stage of this software's growth. Like any other good open source project, Chkware is always looking for a good documentation engineer and information architect.
 
Ob-boarding new users is very important for any project. Keeping the documentation easy to find, and searchable along with advance use-case and example is one of the core area Chkware need continuous support on.
 
This product is, and always will be people's software. Meaning, there will always be user ranging from software developers, test engineers, product owners, and infrastructure engineers. When software engineers develops and API they need good documentation for how to use this tools to write *http* and *spec* files. Test engineers working on the same project need to extends those *http* and *spec* files to add more test criteria, and cases. Product owners involved in same project might need to define high-level *flow* for other stakeholders. Infrastructure engineers need their perspective of documentation to set up CI/CD, and network access for effective tests. So good documentation is needed from all perspectives.
 
So, after installation use Chkware, see example of case-by-case. If you find something lacking, 

1. Create an issue with `documentation` label.
2. Add what you want to add to which documentation. 

### Finding a bug, and reporting it

Actively using Chkware for different scenarios, and use-cases in your daily life is the goal for this project. While using it we might find something not working, or it is broken for a specific input, or case. We humbly request you to file an issue for such a case.
 
Confirm that you are adding the following things while creating an issue under `bug` label:
 
1. The operating system, and its version you are using.
2. Your specific python version. Run `python3 -V` to get it
3. Your `chk` command version. Just run `chk –help` to get the version
4. The specification file that you are trying to write, and the example you are using to write it.
 
### Making a new feature request

If you want to make a new feature request that also means Chkware is making great value to your everyday life, and you want to contribute to its growth. For such case kindly:
 
Create an issue under `enhancement` label and add following to it.
 
1. A good related, understandable, meaningful one-liner title
2. Details about how you are using it. What are closest solution to that you want to do. Are you talking about extending an existing feature, or completely new feature. Use-cases you can came across about the problems you are facing.
 
### Fixing a bug, or adding a new feature

This section generally defines how you can make code contribution. Please follow [these instructions](https://github.com/0hsn/HEAD/blob/master/README.md) to make code contributions.

### Updating specifications

If you have a good balanced knowledge of designing a DSL, or similar; you are a good candidate to contribute on spec definition. It needs a balance between education and experience to define a spec. Our primary focus is choosing meaningful and appropriate keywords, those can be used repeatedly in various scenarios, those are related and meaningful.
 
The process of creating specifications of a certain type is very much similar to the process of making a new feature request. Please follow the similar instructions to create an issue on the topic.

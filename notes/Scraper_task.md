## Part 2: Scraper
#### Tools
If this would be real project I would prefer to use Wikidata rather than Wikipeadia.
While Wikipedia is more comfortable to deal with for humans, Wikidata is designed for computers. It have a protocol describing structure of information in it and it have an API. But, I guess, this task is made to checking my scraping skills so I will use Wikipedia.

Chosen language for this task will be Python3, specifically version 3.7.3. I choose Python because I have most experience with it and it is very good fit for this type of task(simple parsing task).
I am going to use Beautiful Soup Python library for scraping. I have choose it because of its ease of use in comparision to other packages. It may be not suitable for heavier tasks, in that case I would use Scrappy or other scraping package.
I am going to use Pytest for testing. I wanted to use unittest, but most of its object-oriented structure will be left without use for this project.

#### Structure
My function structure is usual. I divided the whole process script must to perform on 5 parts:
 - Download page
 - Get strings of chosen parameters
 - Parse strings of chosen parameters
 - Convert value to another currency
 - Output

You may have noticed that first thing that done was not tests. Though I am familiar with TDD, I like to plan project structure first. Then I am working on one part of program at a time, both on tests and implementation.
Also I see no need in object-oriented structure for this project. In my opinion there is no strong abstraction we can select to be represented by our class.

####Things that did not go as expected:)
I have one test case that shows limitation of regular expression I had used:
`assert parse_param_string("US$21.+-461") == 21` 
If the function should return 21 in that case than it is correct, but if it needs to raise an exception than I dont have an easy way to fix it other than checking for end of string(what I dont want to add to be as much resistant to style changes on Wikipedia as possible) 
#### What else would I add
- Extend tests
- Add generic currency detection
- Add support for non financial parameters

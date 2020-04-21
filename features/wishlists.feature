Feature: The wishlist service back-end
    As a shopper
    I need a RESTful catalog service
    So that I can keep track of all my wishlists

Background:
    Given the following wishlists
        | name   | customer_email       |
        | A      | rudi@stern.nyu.edu   |
        | B      | tom@stern.nyu.edu    |
        | C      | isa@stern.nyu.edu    |
        | D      | becca@stern.nyu.edu  |
        | E      | becca@stern.nyu.edu  |
     
Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Wishlist Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Wishlist
    When I visit the "Home Page"
    And I set the "Name" to "E"
    And I set the "Customer_email" to "rofrano@nyu.edu"
    And I press the "Create" button
    Then I should see the message "Success"
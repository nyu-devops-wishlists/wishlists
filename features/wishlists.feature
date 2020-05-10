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

Scenario: List all wishlists
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "A" in the results
    And I should see "B" in the results
    And I should not see "X" in the results

Scenario: Create a Wishlist
    When I visit the "Home Page"
    And I set the "Name" to "E"
    And I set the "Customer_email" to "rofrano@nyu.edu"
    And I press the "Create" button
    Then I should see the message "Success"

Scenario: Read a Wishlist
    When I visit the "Home Page"
    And I set the "Name" to "A"
    And I press the "Search" button
    Then I should see "A" in the "Name" field
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "A" in the results

Scenario: Query a Wishlist by email
    When I visit the "Home Page"
    And I set the "customer_email" to "becca@stern.nyu.edu"
    And I press the "Search" button
    Then I should see "becca@stern.nyu.edu" in the "customer_email" field
    And I should not see "tom@stern.nyu.edu" in the "customer_email" field
    And I should not see "rudi@stern.nyu.edu" in the "customer_email" field
    And I should not see "isa@stern.nyu.edu" in the "customer_email" field

Scenario: Count Wishlists per user by email
    When I visit the "Home Page"
    And I set the "customer_email" to "becca@stern.nyu.edu"
    And I press the "Count" button
    Then I should see the message "Customer_email becca@stern.nyu.edu has 2 wishlists"
    When I set the "customer_email" to "isa@stern.nyu.edu"
    And I press the "Count" button
    Then I should see the message "Customer_email isa@stern.nyu.edu has 1 wishlists"
    When I set the "customer_email" to "rudi@stern.nyu.edu"
    And I press the "Count" button
    Then I should see the message "Customer_email rudi@stern.nyu.edu has 1 wishlists"
    When I set the "customer_email" to "tom@stern.nyu.edu"
    And I press the "Count" button
    Then I should see the message "Customer_email tom@stern.nyu.edu has 1 wishlists"

Scenario: Update a Wishlist
    When I visit the "Home Page"
    And I set the "Name" to "A"
    And I press the "Search" button
    Then I should see "A" in the "Name" field
    And I should see "rudi@stern.nyu.edu" in the "customer_email" field
    When I change "Name" to "Rudi"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "Rudi" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "Rudi" in the results
    Then I should not see "A" in the results

Scenario: Delete a Wishlist
    When I visit the "Home Page"
    And I set the "Name" to "A"
    And I press the "Search" button
    Then I should see "A" in the "Name" field
    When I copy the "Id" field
    And I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Wishlist has been deleted!"
    When I copy the "Id" field
    And I paste the "Id" field
    And I press the "Search" button
    Then I should see "B" in the "Name" field 
    And I should not see "A" in the results
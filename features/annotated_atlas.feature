Feature: Annotated Brain Atlas
  
  Scenario: Get Brain Region Name from Slice Image position
    Given a slice image has been loaded
    And a brain atlas has been loaded
    When I highlight a position on my registered slice
    Then the name of the brain region associaed with the atlas brain region appears

Feature: Allen Mouse Brain Atlas
  Load the Allen Mouse Brain Atlas for 3D registration

  Scenario: Load Atlas
    Given the 25um atlas is already on my computer
    When I ask for a 25um atlas
    Then a 3D volume of the 25um allen reference atlas appears onscreen.
    And it is set as the current atlas for the session.

  Scenario: Replace Atlas
    Given the 25um atlas is currently loaded
    When I ask for a 100um atlas
    Then a 3D volume of the 100um allen reference atlas appears.

  Scenario: List Available Brainglobe Atlases
    Given I am connected to the internet
    When I check brainglobe
    Then I see a list of bg-atlasapi's available atlases.
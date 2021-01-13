
Feature: Allen Mouse Brain Atlas
  Load the Allen Mouse Brain Atlas for 3D registration

  Scenario: Load Atlas
    Given the 25um atlas is already on my computer
    When I ask for a 25um atlas
    Then a 3D volume of the 25um allen reference atlas appears onscreen.


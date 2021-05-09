
Feature: Allen Mouse Brain Atlas
  Load the Allen Mouse Brain Atlas for 3D registration

  Scenario: Load Atlas
    When I load the 25um allen mouse atlas
    Then a 3D volume of the 25um allen reference atlas is loaded.
    Then a 3D annotation volume of the 25um allen reference atlas is loaded.

  Scenario: Replace Atlas
    Given the 25um atlas is currently loaded
    When I ask for a 100um atlas
    Then a 3D volume of the 100um allen reference atlas appears.

  Scenario: List Available Brainglobe Atlases
    When I refresh the brainglobe atlas list
    Then I see a list of bg-atlasapi's available atlases.

  Scenario: Load Atlas From File Using imio
    When I load the mock.tiff atlas with 10um resolution
    Then a 3D volume of the atlas appears onscreen

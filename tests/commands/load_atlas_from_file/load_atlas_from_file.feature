
Feature: Load Atlas From File
  Load Atlas from file for 3D registration

  Scenario: Load Atlas From NII File
    Given A file containing an atlas
    When I load the atlas NII file
    Then a 3D volume of the atlas appears onscreen
    And it is set as the current atlas for the session

#  Scenario: Replace Atlas
#    Given the 25um atlas is currently loaded
#    When I ask for a 100um atlas
#    Then a 3D volume of the 100um allen reference atlas appears.


Feature: Slice Import
  Users can load Multichannel OME-TIFFs into the program.

  Scenario: Single Slice Import
    Given I have a multichannel OME-TIFF file on my computer.
    And No sections have been loaded yet
    And No sections are onscreen
    When I load the file
    Then I should see the file image onscreen
    And it should have some default 3D transformation.

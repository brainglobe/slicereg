
Feature: Slice Import
  Users can load Multichannel OME-TIFFs into the program.

  Scenario: Single Slice Import
    Given I have a multichannel OME-TIFF file on my computer.
    And No sections have been loaded yet
    When I load the file
    Then I should see the slice image onscreen in 3D
    And The slice is centered on the image

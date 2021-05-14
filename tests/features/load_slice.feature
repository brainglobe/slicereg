
Feature: Slice Import
  Users can load Multichannel OME-TIFFs into the program.

  Scenario: Single Slice Import
    Given I have a multichannel OME-TIFF file on my computer.
    And No sections have been loaded yet
    And An atlas has been loaded
    When I load the file
    Then I should see the slice image onscreen in 3D
    And I should see the atlas image onscreen in slice view
    And The slice is centered on the image
    And The displayed resolution is set to the image's resolution


Feature: Section 3D Affine Registration
  # Enter feature description here

  Scenario: Move Section in 3D
    Given I have loaded a section
    When I ask for the section to be translated and rotated
    Then the image is updated with a new 3D transform
    And an atlas section image at that transform is shown.

  Scenario: Check Pixel Coordinate in Atlas Space
    Given I have loaded a section
    When I indicate a section image coordinate
    Then the coordinate's 2D position and 3D position should appear

